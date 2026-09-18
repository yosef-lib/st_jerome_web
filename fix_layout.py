import codecs, re

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    html = f.read()

pattern = r"(<li>\s*<a href=\"/cetak_khusus\".*?Cetak Stiker Khusus\s*</a>\s*</li>)"
new_menu = r'''\1
                            <li>
                                <a href="/cetak_sirkulasi" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/cetak_sirkulasi' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                    <i class="fa-solid fa-address-card w-5 text-center"></i> Cetak Kartu & Kantong
                                </a>
                            </li>'''

html, count = re.subn(pattern, new_menu, html, flags=re.DOTALL)
print(f"Replaced {count} times")

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(html)
