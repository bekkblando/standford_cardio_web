from bs4 import BeautifulSoup
#import urllib.request
import requests
import base64
import os


# Parse the HTML from file
raw_manual = open("new_manual.html", "r")

new_manual = BeautifulSoup(raw_manual)

# Get our image tags
style_tags = new_manual.findAll('style')

with open('test.css', 'w') as f:
    for style_tag in style_tags:
        for element in style_tag.contents:
            print(element)
            f.write(element)
