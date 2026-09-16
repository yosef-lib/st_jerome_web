import codecs
import re

# 1. Update layout.html
with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    layout = f.read()

# Revert Scanner & Audit Rak back to Scanner Meja Baca
layout = layout.replace('Scanner & Audit Rak', 'Scanner Meja Baca')

# Add Audit Rak to the UTAMA section right after Scanner Meja Baca
audit_menu = '''                            <li>
                                <a href="/audit_rak" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/audit_rak' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                    <i class="fa-solid fa-boxes-packing w-5 text-center"></i> Stok Opname
                                </a>
                            </li>'''

layout = re.sub(r'(<a href="/scan".*?</a>\s*</li>)', r'\1\n' + audit_menu, layout, flags=re.DOTALL)

# Add Anomali to the LAINNYA section right after Analisis Lanjutan
anomali_menu = '''                            <li>
                                <a href="/anomali" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/anomali' %}bg-boxdark2 text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                    <i class="fa-solid fa-triangle-exclamation w-5 text-center"></i> Kualitas Data
                                </a>
                            </li>'''

layout = re.sub(r'(<a href="/analisis_lanjutan".*?</a>\s*</li>)', r'\1\n' + anomali_menu, layout, flags=re.DOTALL)

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(layout)
    
print("layout updated")

# 2. Update app.py
with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

new_audit_route = '''
@app.route('/audit_rak')
@login_required
def audit_rak():
    return render_template('audit_rak.html')

if __name__ == '__main__':'''
app_code = app_code.replace("if __name__ == '__main__':", new_audit_route)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("app.py updated")
