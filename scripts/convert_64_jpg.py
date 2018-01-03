from bs4 import BeautifulSoup
#import urllib.request
import requests
from requests_file import FileAdapter
import base64
import os

# Parse the HTML from file
# TODO Absolute path not ideal - CHANGEME on other file systems
#r = urllib.request.urlopen('file:///Users/BekkBlando/Documents/github/Stanford-Web/scripts/outhandbook.html').read()
# rewoked it by using requests instead of urllib bc it was throwing me an error
url = "file://"  + str(os.getcwd()) + "/outhandbook.html"
s = requests.Session()
s.mount("file://", FileAdapter())
resp = s.get(url)
r = resp.text
#print r.text


old_manual = BeautifulSoup(r)

# Get our image tags
image_tags = old_manual.findAll('img')

# Generate Files and replace the src
for index, image in enumerate(image_tags):
    # Grab the Source
    temp_src = image['src']
    # Grab the base64 encoding
    temp_base64 = temp_src.split(',')[1]

    # Stipulate the appripriate html file path
    file_path = "assets/{}.jpg".format(index)

    # Open the image file path
    output_image = open(file_path, "wb")

    # Write to the file
    output_image.write(base64.b64decode(temp_base64))

    # Reset the image SRC
    image['src'] = file_path
    output_image.close()

# Save the New Manual fromt the modified old_manual
new_manual = open("new_manual.html", "w")
new_manual.write(str(old_manual))
new_manual.close()


# Get the Source Values from each image tag
# src_values = [image['src'] for image in image_tags]


# Get the base 64 encoding using split
# base64_encodings = [src_value.split(',')[1] for src_value in src_values]
