import codecs

with codecs.open('templates/index.html', 'r', 'utf-8') as f:
    code = f.read()

old_logo = '''    <!-- Logo Institusi -->
    <div class="flex items-center justify-center gap-6 mb-6">
        <img src="{{ url_for('static', filename='img/logo_stpd.png') }}" alt="STPD" class="w-24 h-24 object-contain rounded-full border-4 border-white shadow-md bg-white">
        <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" alt="IMAVI" class="w-24 h-24 object-contain rounded-full border-4 border-white shadow-md bg-white">
    </div>'''

new_logo = '''    <!-- Logo Institusi -->
    <div class="flex items-center justify-center gap-6 mb-6">
        <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" alt="IMAVI" class="w-24 h-24 object-contain rounded-full border-4 border-white shadow-md bg-white">
    </div>'''

code = code.replace(old_logo, new_logo)

with codecs.open('templates/index.html', 'w', 'utf-8') as f:
    f.write(code)
