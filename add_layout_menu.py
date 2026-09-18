import codecs

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    html = f.read()

anchor = '''                              <li>
                                  <a href="/cetak_khusus" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/cetak_khusus' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                      <i class="fa-solid fa-print w-5 text-center"></i> Cetak Stiker Khusus
                                  </a>
                              </li>'''

new_menu = '''                              <li>
                                  <a href="/cetak_khusus" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/cetak_khusus' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                      <i class="fa-solid fa-print w-5 text-center"></i> Cetak Stiker Khusus
                                  </a>
                              </li>
                              <li>
                                  <a href="/cetak_kartu" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/cetak_kartu' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                      <i class="fa-solid fa-address-card w-5 text-center"></i> Cetak Kartu & Kantong
                                  </a>
                              </li>'''

html = html.replace(anchor, new_menu)

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(html)
print("layout updated")
