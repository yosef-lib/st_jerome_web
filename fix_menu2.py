import codecs

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    code = f.read()

old_backup = '''                                <a href="/backup" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium text-bodydark duration-300 ease-in-out hover:bg-boxdark2 hover:text-white">
                                    <i class="fa-solid fa-download w-5 text-center"></i>
                                    Download Database
                                </a>
                            </li>'''

new_menu = old_backup + '''
                            
                            <li>
                                <a href="/manajemen_data" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium text-warning duration-300 ease-in-out hover:bg-boxdark2 hover:text-warning">
                                    <i class="fa-solid fa-database w-5 text-center"></i>
                                    Manajemen Data Ekstra
                                </a>
                            </li>'''

if '/manajemen_data' not in code:
    code = code.replace(old_backup, new_menu)
    with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
        f.write(code)
    print("Menu added properly")
else:
    print("Already exists")
