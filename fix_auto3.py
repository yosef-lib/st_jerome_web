import codecs

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    kiosk = f.read()

import re

pattern = r'div\.innerHTML = <p class="font-bold text-black">\\</p><p class="text-xs text-slate-500">\\ - \\</p>;'
new_js = "div.innerHTML = '<p class=\"font-bold text-black\">' + item.identitas + '</p><p class=\"text-xs text-slate-500\">' + item.asal_instansi + ' - ' + item.peran_jabatan + '</p>';"

kiosk = re.sub(pattern, new_js, kiosk)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(kiosk)
