import codecs

with codecs.open('templates/index.html', 'r', 'utf-8') as f:
    html = f.read()

html = html.replace('href="/cetak_stiker"', 'href="/input_buku"')
html = html.replace('Cetak Stiker</span>', 'Input Buku Baru</span>')

with codecs.open('templates/index.html', 'w', 'utf-8') as f:
    f.write(html)
