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
#print(pageTableContents)

parsed_manual = {}
# Last tags
first_layer = ""
second_layer = ""

# If the first layer tag is
for tag in pageTableContents.descendants:
    # Don't count content
    if type(tag).__name__ == "NavigableString":
        continue
    # Clean Section names - TODO combine Regex
    cleaned = re.sub(r"<[^>]*>", "", str(tag))
    cleaned = re.sub(r"\S*\d", "", str(cleaned))
    cleaned = re.sub(r"I*V*\.", "", str(cleaned)).strip()

    # Get our tags classes
    classes = dict(tag.attrs)["class"]

    # If it's a first layer tag
    # class: (x2 || x4) && h3
    #print(cleaned, classes)
    if(("x2" in classes or "x4" in classes) and ("h3" in classes)):
        first_layer = cleaned
        parsed_manual[cleaned] = {}

    # If the first layer tag is set and it's a second layer tag
    # class: (x2 || x4) && h5 add it to the first layer tags JSON
    elif(("x2" in classes or "x4" in classes) and ("h5" in classes)):
        second_layer = cleaned
        parsed_manual[first_layer][cleaned] = {}

    # If the second layer tag is set and it's a third layer tag
    # class: (x2 || x4) && h4 add it to the second layer tags JSON
    elif(("x2" in classes or "x4" in classes) and ("h4" in classes)):
        # If the second layer doesn't exist then it's the first section
        # the first section adds third layers as though they are second layers
        # TODO - Checking for the Surgeon Preferences is not ideal
        if(not second_layer or cleaned == "Surgeon Preferences"):
            second_layer = ""
            parsed_manual[first_layer][cleaned] = {}
        else:
            parsed_manual[first_layer][second_layer][cleaned] = {}

# JSON Object
json_contents = json.dumps(
    parsed_manual, sort_keys=True, indent=4, separators=(',', ': ')
    )

# Pretty print yo
print(json_contents)
# Store the section names in a list

# Iterate through all the tags and if the tag's value is in the section list
# capture the content aside from tags that have a value in the section list

# Was thinking about going page by page and get the first layer id based on the span with class='ff8'
# pages = manual.find_all(id=re.compile('pf[\d,a-f]*'))

h2s = manual.findAll("div", {"class": "h2"})
for tag in h2s:
    cleaned = re.sub(r"<[^>]*>", "", str(tag))
    print cleaned


