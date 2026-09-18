import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    code = f.read()

old_return = "return {"
new_return = "const urlParams = new URLSearchParams(window.location.search);\n        const editId = urlParams.get('edit');\n        return {\n            editMode: !!editId,"
code = code.replace(old_return, new_return)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(code)
print("Fixed Alpine JS")
