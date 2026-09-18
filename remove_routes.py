import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Remove the endpoints from app.py
pattern = r"@app\.route\('/manajemen_data'\)[\s\S]*?# END OF NEW ROUTES\n"
code = re.sub(pattern, '', code)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Routes removed")
