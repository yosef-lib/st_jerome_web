import codecs
import re

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    code = f.read()

new_menu = '''
                            <li>
                                <a href="/manajemen_data" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium text-warning duration-300 ease-in-out hover:bg-boxdark2 hover:text-warning">
                                    <i class="fa-solid fa-database w-5 text-center"></i>
                                    Manajemen Data Ekstra
                                </a>
                            </li>'''

if '/manajemen_data' not in code:
    # Find the backup li closing tag and insert after it
    code = re.sub(r'(<a href="/backup"[\s\S]*?</li>)', r'\1' + new_menu, code)
    with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
        f.write(code)
    print("Menu added using regex")
