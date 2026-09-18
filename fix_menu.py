import codecs

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    code = f.read()

old_menu = '''                    <li>
                        <a href="/ekspor_impor" class="group relative flex items-center gap-2.5 rounded-sm py-2 px-4 font-medium text-bodydark1 duration-300 ease-in-out hover:bg-graydark">
                            <i class="fa-solid fa-file-export"></i>
                            Ekspor & Impor
                        </a>
                    </li>'''

new_menu = '''                    <li>
                        <a href="/ekspor_impor" class="group relative flex items-center gap-2.5 rounded-sm py-2 px-4 font-medium text-bodydark1 duration-300 ease-in-out hover:bg-graydark">
                            <i class="fa-solid fa-file-export"></i>
                            Ekspor & Impor
                        </a>
                    </li>
                    <li>
                        <a href="/manajemen_data" class="group relative flex items-center gap-2.5 rounded-sm py-2 px-4 font-medium text-bodydark1 duration-300 ease-in-out hover:bg-graydark">
                            <i class="fa-solid fa-database"></i>
                            Manajemen Data Ekstra
                        </a>
                    </li>'''

if '/manajemen_data' not in code:
    code = code.replace(old_menu, new_menu)
    with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
        f.write(code)
    print("Menu added")
