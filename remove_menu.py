import codecs
import re

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    code = f.read()

# Remove the menu item
pattern = r'<li>\s*<a href="/manajemen_data"[\s\S]*?</li>'
code = re.sub(pattern, '', code)

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(code)
print("Menu removed")
