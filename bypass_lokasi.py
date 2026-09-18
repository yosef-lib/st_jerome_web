import codecs, re

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Replace return render_template('pilih_lokasi.html', mode=...) with redirects
def replacer(match):
    mode = match.group(1)
    if mode == 'dashboard':
        return "return redirect(url_for('dashboard', lokasi='IMAVI'))"
    elif mode == 'koleksi':
        return "return redirect(url_for('koleksi', lokasi='IMAVI'))"
    elif mode == 'analisis_lanjutan':
        return "return redirect(url_for('analisis_lanjutan', lokasi='IMAVI'))"
    return match.group(0)

code = re.sub(r"return render_template\('pilih_lokasi\.html',\s*mode='([^']+)'\)", replacer, code)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Bypassed pilih_lokasi.html")
