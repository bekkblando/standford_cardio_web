# import firebase_admin
# from firebase_admin import auth
# default_app = firebase_admin.initialize_app()
# uid = 'IlQ8qxT4M8bUoeEe8guMgX4Tm9A3'
import re
from bs4 import BeautifulSoup

from firebase import firebase
firebase = firebase.FirebaseApplication('https://stanford-heart-surgery.firebaseio.com', None)

def transform_html(html):
    html = re.sub('<link rel="stylesheet" type="text/css" href="../../css/style.css" />', "", html)
    html = re.sub('(\.\.\/)', "/", html)
    parsed_html = BeautifulSoup(html, "html.parser")
    for table in parsed_html.findAll('table'):
        table['class'] = table.get('class', []) + ['table-responsive']
    return(str(parsed_html))

def html_transformations(link):
    for key, value in firebase.get(link, None).items():
        if(key == 'content'):
            print(link)
            firebase.patch(link, data={ 'content': transform_html(value) }, params={'print': 'pretty'})
        else:
            html_transformations(link + '/' + key)

html_transformations('/0/Manual')
