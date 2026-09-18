import codecs, re

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

pattern = r"@app\.route\('/cetak_pdf'\)\s*@login_required\s*def cetak_pdf\(\):.*?return.*?400"

new_cetak = '''@app.route('/cetak_pdf')
@login_required
def cetak_pdf():
    from template_stiker import generate_stiker_pdf
    import os
    output_pdf = 'stiker_output.pdf'
    
    if not os.path.exists(ANTREAN_FILE):
        return "Antrean kosong. Tambahkan buku ke antrean terlebih dahulu."
        
    if os.path.exists(output_pdf):
        os.remove(output_pdf)
        
    try:
        generate_stiker_pdf(ANTREAN_FILE, output_pdf)
    except Exception as e:
        print("Error generating PDF:", e)
        return "Gagal menghasilkan PDF. Terjadi kesalahan internal.", 500
    
    if not os.path.exists(output_pdf):
        return "Gagal menghasilkan PDF. Pastikan antrean tidak kosong dan format data benar."
        
    return send_file(output_pdf, as_attachment=True, download_name='stiker.pdf')'''

app_code, count = re.subn(pattern, new_cetak, app_code, flags=re.DOTALL)
print(f"Replaced {count} times")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
