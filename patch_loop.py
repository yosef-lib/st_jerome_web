import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    html = f.read()

html = html.replace('this.loadBibliografi();', 'this.loadData(this.currentPage);')

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(html)
