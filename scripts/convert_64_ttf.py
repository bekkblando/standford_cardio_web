from bs4 import BeautifulSoup
import urllib.request
import base64

# Parse the HTML from file
# TODO Absolute path not ideal - CHANGEME on other file systems
r = urllib.request.urlopen('file:///Users/BekkBlando/Documents/github/Stanford-Web/scripts/outhandbook.html').read()
old_manual = BeautifulSoup(r)

# Get our image tags
style_tags = old_manual.findAll('style')
print(style_tags)

# # Generate Files and replace the src
# for index, image in enumerate(image_tags):
#     # Grab the Source
#     temp_src = image['src']
#     # Grab the base64 encoding
#     temp_base64 = temp_src.split(',')[1]
#
#     # Stipulate the appripriate html file path
#     file_path = "./assets/{}.jpg".format(index)
#
#     # Open the image file path
#     output_image = open(file_path, "wb")
#
#     # Write to the file
#     output_image.write(base64.b64decode(temp_base64))
#
#     # Reset the image SRC
#     image['src'] = file_path
#     output_image.close()
#
# # Save the New Manual fromt the modified old_manual
# new_manual = open("new_manual.html", "w")
# new_manual.write(str(old_manual))
# new_manual.close()
