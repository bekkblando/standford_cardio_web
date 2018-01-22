from bs4 import BeautifulSoup
import os
import re
import json
import copy

# Parse the HTML from file
raw_checklist = open("../stanford_checklist_assets/stanford_checklist.html", "r")

# BeautifulSoup Object
html = BeautifulSoup(raw_checklist, "html.parser")

# JSON object with 2 levels of hierarchy defined
empty_JSON = json.load(open('two_Layer_Empty_Checklist.JSON'))
JSON_obj = copy.deepcopy(empty_JSON)

def removeHTML(stringWithHtml):
	cleanedString = re.sub(r"<[^>]*>", "", str(stringWithHtml)).strip()
	cleanedString = re.sub(r'[\xe2]', '-', cleanedString)
	cleanedString = re.sub(r'[^\x00-\x7F]+', "", cleanedString)
	return cleanedString

listOfSections = []
def getListOfSections(JSON):
	if listOfSections:
		return listOfSections
	else:
		for key in JSON:
			if type(JSON[key]) is dict:
				for key2 in JSON[key]:
					listOfSections.append(str(key2).upper())
		return listOfSections

def isSectionTitle(aDiv):
	divString = removeHTML(aDiv)
	return divString in getListOfSections(empty_JSON)

def isEndOfSection(aDiv):
	divString = removeHTML(aDiv)
	return divString == "END"

def findCategoryOfSection(aSectionTitle):
	for key in empty_JSON:
		if type(empty_JSON[key]) is dict:
			if aSectionTitle in (title.upper() for title in list(empty_JSON[key].keys())):
				return key
	return ''

def parseSectionContent(someHTML):
	sectionDict = {}
	sectionDict['HTML_Blob'] = someHTML

	return sectionDict

pages = html.find_all(id=re.compile('pf[\d,a-f]*'))

# Iterate over the pages of the checklist, starting at page 4
# For each page, iterate over the each div with in it
# If the current div is a section, set the layer keys
# If the current div is a end of section, parse content of the section and add it to the JSON obj under the current layer keys and reset the keys
# If the layer keys are not empty and the cur div is not a section title or end of section add the cur div to beautiful soup obj to be parsed when the end of section is reached


first_layer = ''
second_layer = ''
section_content = ''

for page in pages:
    # Skip table of content and contact info
    if page["data-page-no"] in ['1','2','3']:
        continue

    # if page["data-page-no"] in ['7', '8']:
    page_content = page.find('div', {'class': 'pc'})
    
    for child in page_content.children:
    	# Special case
    	# Some section names do not match those found in the table of contents
    	textOfChild = removeHTML(child)
    	if textOfChild == 'PULSELESS ELECTRICAL ACTIVITY':
    		child = "PEA"
    	if textOfChild == 'SUPRAVENTRICULAR TACHYCARDIA - STABLE':
    		child = 'SVT - Stable Tachycardia'.upper()
    	if textOfChild == 'SUPRAVENTRICULAR TACHYCARDIA - UNSTABLE':
    		child = 'SVT - Unstable Tachycardia'.upper()
    	if textOfChild == 'VENTRICULAR FIBRILLATION VENTRICULAR TACHYCARDIA - PULSELESS':
    		child = 'VF/VT'
    	if textOfChild == 'BRONCHOSPASM (INTUBATED PATIENT)':
    		child = 'BRONCHOSPASM'
    	if textOfChild == 'DIFFICULT AIRWAY UNANTICIPATED':
    		child = 'DIFFICULT AIRWAY - UNANTICIPATED'
    	if textOfChild == 'HEMORRHAGE':
    		child = 'HEMORRHAGE - MTG'
    	if textOfChild == 'TRANSFUSION REACTIONS':
    		child = 'TRANSFUSION REACTION'

    	if isSectionTitle(child):
    		second_layer = removeHTML(child)
    		first_layer = findCategoryOfSection(second_layer)
    		continue

    	if isEndOfSection(child):
    		# Parse the content into different list ie. signs, details, etc...
    		# JSON_obj[first_layer][second_layer]['HTML_Blob'] = section_content
    		JSON_obj[first_layer][second_layer] = parseSectionContent(section_content)

    		# And reset layer keys
    		first_layer = ''
    		second_layer = ''
    		section_content = ''
    		continue

    	# if 'c' in child['class']:
    	# 	## print('c class', str(child), str(child['class']))
    	# 	continue

    	if first_layer and second_layer:
    		section_content += str(child)

# ---------------------
# Pretty # printfor JSON
json_contents = json.dumps(
    JSON_obj, sort_keys=True, indent=4, separators=(',', ': ')
    )

with open('checklist.JSON', 'w') as outfile:
    outfile.write(json_contents)




