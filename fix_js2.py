import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    html = f.read()

old_rec = '''        const recDDCValue = document.getElementById('recDDCValue');
        const recDDCDesc = document.getElementById('recDDCDesc');'''

new_rec = '''        const recDDCValue = recLabel.querySelector('#recDDCValue');
        const recDDCDesc = recLabel.querySelector('#recDDCDesc');'''

html = html.replace(old_rec, new_rec)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(html)
print("Fixed querySelectors")
