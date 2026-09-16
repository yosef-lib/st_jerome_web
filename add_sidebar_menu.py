import codecs
import re

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    html = f.read()

menu_item = '''
            <!-- Menu Item Analitik Kunjungan -->
            <li>
              <a href="/analitik_kunjungan" class="group relative flex items-center gap-2.5 rounded-sm py-2 px-4 font-medium text-bodydark1 duration-300 ease-in-out hover:bg-boxdark2 {% if request.path == '/analitik_kunjungan' %}bg-boxdark2{% endif %}">
                <i class="fa-solid fa-chart-pie w-5 h-5 flex items-center justify-center"></i>
                Analitik Kunjungan
              </a>
            </li>
            <!-- Menu Item Stok Opname -->'''

html = html.replace('<!-- Menu Item Stok Opname -->', menu_item)

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(html)

print("Added sidebar menu")
