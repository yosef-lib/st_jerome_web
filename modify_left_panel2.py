import codecs
import re

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Update logo and title
pattern_title = r'<div class="relative z-10">.*?</div>\s*<div class="mt-auto relative z-10'
new_title = '''<div class="relative z-10 flex flex-col items-center text-center mt-4">
                <div class="w-28 h-28 bg-white rounded-full flex items-center justify-center mb-6 shadow-lg border-4 border-primary mx-auto">
                    <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="IMAVI Logo" class="w-20 h-20 object-contain">
                </div>
                <h1 class="text-3xl font-bold mb-4 leading-tight tracking-tight">Selamat Datang di<br>Perpustakaan<br>St. Jerome</h1>
                <p class="text-bodydark text-sm mb-8 font-medium px-4">Silakan pindai Kartu Anggota Anda, atau isi form buku tamu jika Anda bukan anggota.</p>
            </div>
            <div class="mt-auto relative z-10'''
html = re.sub(pattern_title, new_title, html, flags=re.DOTALL)

# 2. Update footer
pattern_footer = r'<div class="mt-auto relative z-10 flex items-center gap-3">.*?</div>\s*</div>\s*</div>'
new_footer = '''<div class="mt-auto relative z-10 flex items-center justify-center gap-3 border-t border-bodydark/30 pt-4">
                <img src="{{ url_for('static', filename='images/logo.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="SJLA" class="w-10 h-10 object-contain bg-white rounded-full border border-stroke">
                <div class="text-left">
                    <p class="text-sm font-bold text-white tracking-wide">ST. JEROME</p>
                    <p class="text-xs text-bodydark">Library Assistant</p>
                </div>
            </div>
        </div>'''
html = re.sub(pattern_footer, new_footer, html, flags=re.DOTALL)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)
