import lxml.html.clean as clean

# open up the latest manual
f = open("new_manual.html")
txt = f.read()
code = str(txt)
f.close()

# remove all attributes from html tags
safe_attrs = clean.defs.safe_attrs
cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset())
cleansed = cleaner.clean_html(code)

# cut everything before the body tag bc the style tag is out of control
cleansed = cleansed.split("<body>")[1]

# make a new file
a = open("cleaned_manual.html", "rw+")
a.write(cleansed)
a.close()
