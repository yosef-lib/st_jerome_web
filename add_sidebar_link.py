import codecs

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    html = f.read()

old_menu = '''                                <ul class="mt-2 flex flex-col gap-1 pl-10 pr-2 pb-2">
                                    <li><a href="/koleksi" class="flex rounded-md px-3 py-2 text-sm {% if request.path.startswith('/koleksi') %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Daftar Koleksi</a></li>'''

new_menu = '''                                <ul class="mt-2 flex flex-col gap-1 pl-10 pr-2 pb-2">
                                    <li><a href="/sirkulasi" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/sirkulasi' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}"><i class="fa-solid fa-cash-register mr-2 mt-1"></i> Kasir Sirkulasi</a></li>
                                    <li><a href="/koleksi" class="flex rounded-md px-3 py-2 text-sm {% if request.path.startswith('/koleksi') %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Daftar Koleksi</a></li>'''

html = html.replace(old_menu, new_menu)

# update active state logic
old_active = '''{% set koleksi_active = request.path.startswith('/koleksi') or request.path == '/input_buku' or request.path == '/audit_rak' %}'''
new_active = '''{% set koleksi_active = request.path == '/sirkulasi' or request.path.startswith('/koleksi') or request.path == '/input_buku' or request.path == '/audit_rak' %}'''
html = html.replace(old_active, new_active)

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(html)
