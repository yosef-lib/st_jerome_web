import codecs
import re

with codecs.open('templates/anggota.html', 'r', 'utf-8') as f:
    html = f.read()
    
m = re.search(r'<dialog id="editModal".*?</dialog>', html, re.DOTALL)
if m:
    print(m.group(0))
else:
    print("Not found")
