import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    html = f.read()

html = html.replace('{% block page_title %}Katalog & Cetak Stiker{% endblock %}', '{% block page_title %}Input Buku Baru{% endblock %}')
html = html.replace('{% block page_subtitle %}Input bibliografi buku baru dan kelola antrean cetak stiker{% endblock %}', '{% block page_subtitle %}Input bibliografi buku baru sebelum masuk antrean cetak{% endblock %}')

# Update UI to reflect all 3 printed by default
html = html.replace('<i class="fa-solid fa-file-pdf mt-1"></i> Unduh PDF Stiker A4', '<i class="fa-solid fa-file-pdf mt-1"></i> Cetak Lengkap (A4)')

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(html)
print("success input_buku")
