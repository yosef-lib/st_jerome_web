import codecs
import re

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Remove Tombol Kembali
back_btn_pattern = r'<!-- Tombol Kembali -->.*?</a>'
html = re.sub(back_btn_pattern, '', html, flags=re.DOTALL)

# 2. Remove Big Barcode Logo
qr_logo_pattern = r'<div class="mt-12 text-center">.*?Sistem otomatis mendeteksi barcode Anda\.</p>\s*</div>'
html = re.sub(qr_logo_pattern, '', html, flags=re.DOTALL)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)
