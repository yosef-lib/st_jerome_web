import codecs

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    html = f.read()

# Replace Cetak Stiker menu with two menus
old_menu = '''                            <li>
                                <a href="/cetak_stiker" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/cetak_stiker' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                    <i class="fa-solid fa-print w-5 text-center"></i> Cetak Stiker
                                </a>
                            </li>'''
                            
new_menu = '''                            <li>
                                <a href="/input_buku" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/input_buku' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                    <i class="fa-solid fa-book-medical w-5 text-center"></i> Input Buku Baru
                                </a>
                            </li>
                            <li>
                                <a href="/cetak_khusus" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/cetak_khusus' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                    <i class="fa-solid fa-print w-5 text-center"></i> Cetak Stiker
                                </a>
                            </li>'''

html = html.replace(old_menu, new_menu)
with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(html)

import os
if os.path.exists('templates/input_stiker.html'):
    os.rename('templates/input_stiker.html', 'templates/input_buku.html')

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

app_code = app_code.replace("@app.route('/cetak_stiker')", "@app.route('/input_buku')")
app_code = app_code.replace("def cetak_stiker():", "def input_buku():")
app_code = app_code.replace("return render_template('input_stiker.html')", "return render_template('input_buku.html')")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("success splitting menu")
