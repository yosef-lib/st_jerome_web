import codecs
import re

with codecs.open('templates/anggota.html', 'r', 'utf-8') as f:
    html = f.read()

m = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if m:
    print(m.group(1))
