import codecs

# 1. Fix app.py column names
with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

old_query = "SELECT member_name, instansi FROM anggota WHERE member_id = ?"
new_query = "SELECT nama, institusi FROM anggota WHERE member_id = ?"
app_code = app_code.replace(old_query, new_query)
app_code = app_code.replace("member['member_name']", "member['nama']")
app_code = app_code.replace("member['instansi']", "member['institusi']")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

# 2. Fix layout.html sidebar
with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    layout = f.read()

import re

# Insert after audit_rak list item
# We'll use regex to find the </li> closing the /audit_rak <li>
audit_rak_li = r'(<a href="/audit_rak".*?</a>\s*</li>)'
menu_kunjungan = r'''\1
                            <li>
                                <a href="/analitik_kunjungan" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/analitik_kunjungan' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                    <i class="fa-solid fa-chart-pie w-5 text-center"></i> Analitik Kunjungan
                                </a>
                            </li>'''

layout = re.sub(audit_rak_li, menu_kunjungan, layout, flags=re.DOTALL)

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(layout)
