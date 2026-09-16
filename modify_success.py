import codecs

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

# Change JS logic
old_js = '''msg.innerText = "Selamat Datang, " + name + "!";'''
new_js = '''msg.innerText = "Halo " + name + ",\\nselamat datang di perpustakaan St. Jerome.";'''

html = html.replace(old_js, new_js)

# Also let's just make the toast text slightly more accommodating for multi-line
old_toast_html = '''<h2 id="successMessage" class="text-4xl font-bold mb-2 text-center px-4">Selamat Datang!</h2>
            <p class="text-xl opacity-90">Kunjungan Anda telah tercatat.</p>'''
# Actually it might be <p class="text-xl opacity-90">Kehadiran Anda telah tercatat.</p> now
old_toast_html_1 = '''<h2 id="successMessage" class="text-4xl font-bold mb-2 text-center px-4">Selamat Datang!</h2>'''
new_toast_html_1 = '''<h2 id="successMessage" class="text-3xl md:text-4xl font-bold mb-2 text-center px-4 whitespace-pre-line leading-tight">Selamat Datang!</h2>'''
html = html.replace(old_toast_html_1, new_toast_html_1)

# Remove the text below it so it just says "Halo [Nama]..."
old_toast_p = '''<p class="text-xl opacity-90">Kehadiran Anda telah tercatat.</p>'''
html = html.replace(old_toast_p, '')

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)
