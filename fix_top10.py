import codecs
import re

# 1. Update app.py query
with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

old_query = "SELECT identitas, tipe_pengunjung, asal_instansi, peran_jabatan, COUNT(id) as jumlah_kunjungan"
new_query = "SELECT identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas, COUNT(id) as jumlah_kunjungan"
app_code = app_code.replace(old_query, new_query)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

# 2. Update analitik_kunjungan.html UI
with codecs.open('templates/analitik_kunjungan.html', 'r', 'utf-8') as f:
    html = f.read()

old_td = '''<td class="border-b border-[#eee] py-3 px-4">
                                <h5 class="font-medium text-black">{{ v.identitas }}</h5>
                                <p class="text-xs text-slate-500">{{ v.tipe_pengunjung }} - {{ v.peran_jabatan }}</p>
                            </td>'''

new_td = '''<td class="border-b border-[#eee] py-3 px-4">
                                <h5 class="font-medium text-black">{{ v.identitas }}</h5>
                                <p class="text-xs text-slate-500">
                                    {{ v.tipe_pengunjung }}
                                    {% if v.peran_jabatan %} - {{ v.peran_jabatan }}{% endif %}
                                    {% if v.fakultas %} ({{ v.fakultas }}){% endif %}
                                </p>
                            </td>'''

html = html.replace(old_td, new_td)

with codecs.open('templates/analitik_kunjungan.html', 'w', 'utf-8') as f:
    f.write(html)
