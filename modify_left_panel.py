import codecs
import re

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Update left panel (logo and title)
old_content = '''<div class="relative z-10">
                <div class="w-24 h-24 bg-white rounded-full flex items-center justify-center mb-6 shadow-lg border-4 border-primary">
                    <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="IMAVI Logo" class="w-16 h-16 object-contain">
                </div>
                <h1 class="text-4xl font-bold mb-4 leading-tight tracking-tight">Buku Tamu<br>IMAVI</h1>
                <p class="text-bodydark text-lg mb-8 font-medium">Silakan pindai Kartu Anggota Anda atau isi form buku tamu jika Anda bukan anggota tetap (tamu).</p>
            </div>'''
new_content = '''<div class="relative z-10 flex flex-col items-center text-center mt-4">
                <div class="w-28 h-28 bg-white rounded-full flex items-center justify-center mb-6 shadow-lg border-4 border-primary mx-auto">
                    <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="IMAVI Logo" class="w-20 h-20 object-contain">
                </div>
                <h1 class="text-3xl font-bold mb-4 leading-tight tracking-tight">Selamat Datang di<br>Perpustakaan<br>St. Jerome</h1>
                <p class="text-bodydark text-sm mb-8 font-medium px-4">Silakan pindai Kartu Anggota Anda, atau isi form buku tamu jika Anda bukan anggota.</p>
            </div>'''
html = html.replace(old_content, new_content)

# 2. Update St Jerome Library Assistant logo
old_footer = '''<div class="mt-auto relative z-10 flex items-center gap-3">
                <i class="fa-solid fa-book-open-reader text-2xl text-bodydark"></i>
                <div>
                    <p class="text-sm font-bold text-white tracking-wide">ST. JEROME</p>
                    <p class="text-xs text-bodydark">Library Assistant</p>
                </div>
            </div>'''
new_footer = '''<div class="mt-auto relative z-10 flex items-center justify-center gap-3 border-t border-bodydark/30 pt-4">
                <img src="{{ url_for('static', filename='images/logo.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="SJLA" class="w-10 h-10 object-contain bg-white rounded-full border border-stroke">
                <div class="text-left">
                    <p class="text-sm font-bold text-white tracking-wide">ST. JEROME</p>
                    <p class="text-xs text-bodydark">Library Assistant</p>
                </div>
            </div>'''
html = html.replace(old_footer, new_footer)

# 3. Add autofocus to input and JS logic
html = html.replace('id="memberIdInput" placeholder="Arahkan', 'id="memberIdInput" autofocus placeholder="Arahkan')

# Just to be 100% sure it autofocuses on load, add a script block at the end of body
js_focus = '''
        window.addEventListener('load', function() {
            setTimeout(() => {
                if(!contentMember.classList.contains('hidden')) {
                    document.getElementById('memberIdInput').focus();
                }
            }, 100);
        });
        
        // Ensure clicking anywhere on the document refocuses if on member tab
        document.addEventListener('click', function(e) {
            if(!contentMember.classList.contains('hidden') && e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A') {
                document.getElementById('memberIdInput').focus();
            }
        });
'''
html = html.replace('// Remove camera logic block completely', js_focus)

# Also fix the weird remnant <p> Kunjungan Anda telah tercatat </p> that I missed in last step if it's there
html = html.replace('<p class="text-xl opacity-90">Kunjungan Anda telah tercatat.</p>', '')

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)
