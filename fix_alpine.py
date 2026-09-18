import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    code = f.read()

old_alpine = "Alpine.data('inputBuku', () => ({"
new_alpine = "Alpine.data('inputBuku', () => {\n    const urlParams = new URLSearchParams(window.location.search);\n    const editId = urlParams.get('edit');\n    return {\n        editMode: !!editId,"
code = code.replace(old_alpine, new_alpine)

# Now find the end of the object to close the function
# Actually, the end of Alpine.data('inputBuku', () => ({ was just }));. Let's just find })); and replace it with };});
old_end = "}));"
new_end = "    };\n});"
code = code.replace(old_end, new_end)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(code)
print("Alpine syntax fixed")
