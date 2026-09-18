import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

old_biblio = """                if (res.status === 401) { alert('Sesi habis! Silakan refresh halaman dan coba lagi.'); return; }
                const data = await res.json();"""

new_biblio = """                if (res.status === 401) { alert('Sesi habis! Silakan refresh halaman dan coba lagi.'); return; }
                if (!res.ok) { const txt = await res.text(); console.error(txt); alert('Server Error ' + res.status + ': Silakan cek console browser (F12) untuk detailnya.'); return; }
                const data = await res.json();"""

code = code.replace(old_biblio, new_biblio)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("JS updated to catch 500 HTML errors")
