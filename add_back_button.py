import codecs

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

back_btn = '''<body class="flex flex-col items-center py-10 px-4 relative">
    
    <!-- Tombol Kembali -->
    <a href="/" class="absolute top-6 left-6 md:top-10 md:left-10 bg-white text-black font-semibold py-2 px-4 rounded shadow hover:bg-gray-50 transition flex items-center gap-2 text-sm z-10">
        <i class="fa-solid fa-arrow-left"></i> Kembali
    </a>'''

html = html.replace('<body class="flex flex-col items-center py-10 px-4 relative">', back_btn)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)
print("Added back button")
