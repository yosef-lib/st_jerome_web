import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

app_code = app_code.replace("render_template('cetak_kartu.html',", "render_template('cetak_sirkulasi.html',")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
