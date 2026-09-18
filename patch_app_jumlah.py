import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Replace: if jumlah_eksemplar > 0: -> wait, does it already check?
# Look for # 2. Generate Barcodes
old_barcode = '''    # 2. Generate Barcodes (No Induk)
    import datetime
    current_year = datetime.datetime.now().strftime('%y') # e.g. '26'
'''

new_barcode = '''    # 2. Generate Barcodes (No Induk)
    if jumlah_eksemplar > 0:
        import datetime
        current_year = datetime.datetime.now().strftime('%y') # e.g. '26'
'''

# We also need to indent everything below it!
# It's easier to just use regex to indent the rest of the function until conn.commit()
def add_indent(match):
    block = match.group(1)
    indented = '\n'.join(['    ' + line if line.strip() else line for line in block.split('\n')])
    return '    if jumlah_eksemplar > 0:\n' + indented + '\n    conn.commit()'

code = re.sub(r'    # 2\. Generate Barcodes \(No Induk\)(.*?)conn\.commit\(\)', add_indent, code, flags=re.DOTALL)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Patched barcode generation")
