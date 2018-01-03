f = open("cleaned_manual.html", "r")
txt = f.read()
f.close()

stuff = txt.replace("<span>", "").replace("</span>", "")

a = open("spanless.html", "rw+")
a.write(stuff)
a.close()


