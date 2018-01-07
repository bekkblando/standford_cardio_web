from bs4 import BeautifulSoup
import base64
import os
import re
import json

# Parse the HTML from file
raw_manual = open("new_manual.html", "r")

# Parse to BeautifulSoup Object
manual = BeautifulSoup(raw_manual, "html.parser")

# Parse the table of contents into a JSON hierachy that captures the 3 sections
# Time for some sketchy stuff
# TODO there should be another way to grab two pages
firstPageTableContents = manual.find_all(id='pf1')
secondPageTableContents = manual.find_all(id='pf2')
# Make a string of both pages
contentString = str(firstPageTableContents) + str(secondPageTableContents)
# Make the BeautifulSoup object from the combined string
pageTableContents = BeautifulSoup(contentString, "html.parser")
# print(pageTableContents)

parsed_manual = {}
# Last tags
first_layer = ""
second_layer = ""
# Grab our keys for later use
first_layer_keys = []
second_layer_keys = []
third_layer_keys = []

# If the first layer tag is
for tag in pageTableContents.descendants:
    # Don't count content
    if type(tag).__name__ == "NavigableString":
        continue
    # Clean Section names - TODO combine Regex
    cleaned = re.sub(r"<[^>]*>", "", str(tag))
    #cleaned = re.sub(r"\S*\d", "", str(cleaned)) [^\w]\s*\d+
    cleaned = re.sub(r"(^|\s)\d+", "", str(cleaned)) 
    cleaned = re.sub(r'\s+', " ", str(cleaned))
    cleaned = re.sub(r"I*V*\.", "", str(cleaned)).strip().upper()

    # Get our tags classes
    classes = dict(tag.attrs)["class"]

    # If it's a first layer tag
    # class: (x2 || x4) && h3
    if(("x2" in classes or "x4" in classes) and ("h3" in classes)):
        first_layer = cleaned
        first_layer_keys.append(cleaned)
        parsed_manual[cleaned] = {}

    # If the first layer tag is set and it's a second layer tag
    # class: (x2 || x4) && h5 add it to the first layer tags JSON
    elif(("x2" in classes or "x4" in classes) and ("h5" in classes)):
        second_layer = cleaned
        second_layer_keys.append(cleaned)
        parsed_manual[first_layer][cleaned] = {}

    # If the second layer tag is set and it's a third layer tag
    # class: (x2 || x4) && h4 add it to the second layer tags JSON
    elif(("x2" in classes or "x4" in classes) and ("h4" in classes)):
        # If the second layer doesn't exist then it's the first section
        # the first section adds third layers as though they are second layers
        # TODO - Checking for the Surgeon Preferences is not ideal
        if(not second_layer or cleaned == "SURGEON PREFERENCES"):
            second_layer = ""
            second_layer_keys.append(cleaned)
            parsed_manual[first_layer][cleaned] = {}
        else:
            # print(first_layer, second_layer, cleaned)
            parsed_manual[first_layer][second_layer][cleaned] = {}
            third_layer_keys.append(cleaned)

# print first_layer_keys
# print second_layer_keys
# print third_layer_keys

# Store the section names in a list

# Iterate through all the tags and if the tag's value is in the section list
# capture the content aside from tags that have a value in the section list

first_layer = ""
second_layer = ""
third_layer = ""

# Get the individual pages of manual
pages = manual.find_all(id=re.compile('pf[\d,a-f]*'))

# Iterating over each page
# Pulling the first layer key from bottom of page
# Then checking each div with in page content (pc) to see if it is a new second layer key
# Adding content to dictionary
for page in pages:
    # Skip table of content and contact info
    if page["data-page-no"] in ['1','2','3']:
        continue

    # first layer(FL) spans, found at bottom of each page. Matches first layer keys
    FL_spans = page.find("div", {'class': "h1"})
    FL_spans = FL_spans.find_all("span")

    # Concatenate all spans together
    FL_title = ''
    for span in FL_spans:
        FL_title += str(span)

    # Clean first layer title
    FL_title = re.sub(r"<[^>]*>", "", str(FL_title)).strip()
    FL_title = re.sub(r"\d*", "", str(FL_title)).strip()
    FL_title = FL_title.split()
    FL_title = " ".join(sorted(set(FL_title), key=FL_title.index))

    # Check found key against keys in parsed manual
    if FL_title.upper() != first_layer and FL_title.upper() in first_layer_keys:
        first_layer = FL_title.upper()
        second_layer = ""
        third_layer = ""

    # Grab page content and iterate over looking for second layer keys
    page_content = page.find('div', {'class': 'pc'})
    for child in page_content.children:
        # """
        # If the tag doesn't have a section in it such as the second_layer
        # or third_layer then we want to add that tag to the
        # content of the last lowest level layer that it didn't have.
        # """
        # if the tag doesn't have the second or third layer in it and
        # the last one set was second_layer

        # Skip the footer divs
        if 'h1\'' in str(child['class']):
            continue

        # Checking if div is h2, and then if it contains a second and/or third layer key
        if 'h2\'' in str(child['class']):
            cleaned = str(child).strip()
            

            # Grade keys that span multiple divs
            siblining = child.next_sibling
            if siblining != None and 'h2' in str(siblining['class']):
                cleaned += str(siblining).strip()

            # Clean text to check if it is a key
            cleaned = re.sub(r"<[^>]*>", "", str(cleaned))
            cleaned = re.sub(r'\s+', " ", str(cleaned))
            cleaned = re.sub(r'[^\x00-\x7F]+', "", str(cleaned)).strip()
            #cleaned = re.sub(r'amp;', '', str(cleaned))

            # print('cleaned', cleaned)
            # print '****child*****'
            # print child

            # Check if the h2 div contained the second and third layer keys
            # Special cases
            #   SYSTOLIC ANTERIOR MOTION (SAM) = SYSTOLIC ANTERIOR MOTION (SAM) OF THE MITRAL VALVE
            #   GI BLEEDING = POST-OPERATIVE GI BLEEDING
            #   OBTAINING CONSENT PROCEDURE LIST = OBTAINING CONSENT/PROCEDURE LIST
            #   CARDIAC: TAVR is not a true section it is TRANSCATHETER AORTIC VALVE REPLACEMENT (TAVR) continued 
            if cleaned.count(':') == 1:
                index = cleaned.find(':')
                second_layer_holder = cleaned[:index]
                third_layer_holder = cleaned[index + 1:].strip()
                
                # Special Cases
                if third_layer_holder == 'POST-OPERATIVE GI BLEEDING':
                    third_layer_holder = 'GI BLEEDING'
                elif third_layer_holder == 'SYSTOLIC ANTERIOR MOTION (SAM) OF THE MITRAL VALVE':
                    third_layer_holder = 'SYSTOLIC ANTERIOR MOTION (SAM)'
                elif third_layer_holder == 'OBTAINING CONSENT/PROCEDURE LIST':
                    third_layer_holder = 'OBTAINING CONSENT PROCEDURE LIST'
                # print '****parsed :*******'
                # print(first_layer, second_layer_holder, third_layer_holder)

                if second_layer_holder in second_layer_keys and third_layer_holder.upper() in third_layer_keys:
                    second_layer = second_layer_holder.upper()
                    third_layer = third_layer_holder.upper()
                elif cleaned in second_layer_keys:
                    second_layer = cleaned
                    third_layer = ''
            # Someone decide the NEUROLOGIC headers should be formated different than all the other.... 
            elif cleaned.count(':') == 2:
                # Parse cleaned string in to layers
                index_one = cleaned.find(':')
                index_two = cleaned.rfind(':')
                second_layer_holder = cleaned[index_one + 1: index_two].strip()
                third_layer_holder = cleaned[index_two + 1:].strip()
                
                # Check that the layer exists
                if second_layer_holder in second_layer_keys and third_layer_holder.upper() in third_layer_keys:
                    second_layer = second_layer_holder.upper()
                    third_layer = third_layer_holder.upper()
                elif cleaned in second_layer_keys:
                    second_layer = cleaned
                    third_layer = ''
                
            else:
                if cleaned in second_layer_keys:
                    second_layer = cleaned.upper()
                    third_layer = ''

        else:
            # print '******' 
            # print child
            # print(first_layer, second_layer, third_layer)
            # Check to make sure we have all needed levels
            if first_layer != '':
                if second_layer != '':
                    # Add content lowest level dic under content key
                    if third_layer != '':
                        if 'content' in parsed_manual[first_layer][second_layer][third_layer]:
                            parsed_manual[first_layer][second_layer][third_layer]['content'] += str(child)
                        else:
                            parsed_manual[first_layer][second_layer][third_layer]['content'] = ""

                    else:
                        # print('layers',first_layer, second_layer)
                        if 'content' in parsed_manual[first_layer][second_layer]:
                            parsed_manual[first_layer][second_layer]['content'] += str(child)
                        else:
                            parsed_manual[first_layer][second_layer]['content'] = ""


# JSON Object
json_contents = json.dumps(
    parsed_manual, sort_keys=True, indent=4, separators=(',', ': ')
    )

with open('Content.JSON', 'w') as outfile:
    outfile.write(json_contents)


# Pretty print yo
# print(json_contents)