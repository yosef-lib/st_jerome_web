import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

old_query = '''# Metrik 3: Demografi Instansi (Bulan Ini)'''
new_query = '''# Log Kunjungan Hari Ini
        log_hari_ini_rows = conn.execute("""
            SELECT waktu_kunjungan, identitas, tipe_pengunjung, asal_instansi, peran_jabatan, fakultas
            FROM sjla_visitor_logs
            WHERE date(waktu_kunjungan) = date('now', 'localtime')
            ORDER BY waktu_kunjungan DESC
        """).fetchall()
        log_hari_ini = [dict(row) for row in log_hari_ini_rows]
        
        # Metrik 3: Demografi Instansi (Bulan Ini)'''
app_code = app_code.replace(old_query, new_query)

old_render = '''return render_template('analitik_kunjungan.html', 
                          kunjungan_hari_ini=kunjungan_hari_ini, 
                          member_hari_ini=member_hari_ini,
                          non_member_hari_ini=non_member_hari_ini,
                          fakultas_hari_ini=fakultas_hari_ini,
                          demografi=demografi, 
                          top_visitors=top_visitors)'''
new_render = '''return render_template('analitik_kunjungan.html', 
                          kunjungan_hari_ini=kunjungan_hari_ini, 
                          member_hari_ini=member_hari_ini,
                          non_member_hari_ini=non_member_hari_ini,
                          fakultas_hari_ini=fakultas_hari_ini,
                          demografi=demografi, 
                          top_visitors=top_visitors,
                          log_hari_ini=log_hari_ini)'''
app_code = app_code.replace(old_render, new_render)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

with codecs.open('templates/analitik_kunjungan.html', 'r', 'utf-8') as f:
    html = f.read()

# Add a full width table block below the grid of 2 columns
table_html = '''
    <!-- Log Kunjungan Hari Ini -->
    <div class="mt-4 md:mt-6 2xl:mt-7.5 rounded-sm border border-stroke bg-white px-5 pt-6 pb-2.5 shadow-default sm:px-7.5 xl:pb-1">
        <h4 class="mb-4 text-xl font-bold text-black">Rincian Kunjungan Hari Ini</h4>
        <div class="max-w-full overflow-x-auto max-h-96 overflow-y-auto">
            <table class="w-full table-auto">
                <thead>
                    <tr class="bg-gray-2 text-left">
                        <th class="py-2 px-4 font-medium text-black">Waktu</th>
                        <th class="py-2 px-4 font-medium text-black">Identitas</th>
                        <th class="py-2 px-4 font-medium text-black">Status</th>
                        <th class="py-2 px-4 font-medium text-black">Instansi & Peran</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in log_hari_ini %}
                    <tr>
                        <td class="border-b border-[#eee] py-3 px-4 text-sm text-slate-500 whitespace-nowrap">
                            {{ log.waktu_kunjungan[11:16] }} WIB
                        </td>
                        <td class="border-b border-[#eee] py-3 px-4">
                            <h5 class="font-medium text-black">{{ log.identitas }}</h5>
                        </td>
                        <td class="border-b border-[#eee] py-3 px-4">
                            {% if log.tipe_pengunjung == 'Member' %}
                            <span class="inline-block rounded bg-success/10 py-1 px-2.5 text-xs font-medium text-success">Member</span>
                            {% else %}
                            <span class="inline-block rounded bg-warning/10 py-1 px-2.5 text-xs font-medium text-warning">Non-Member</span>
                            {% endif %}
                        </td>
                        <td class="border-b border-[#eee] py-3 px-4">
                            <p class="text-sm text-black">{{ log.asal_instansi }}</p>
                            <p class="text-xs text-slate-500">
                                {% if log.peran_jabatan %}{{ log.peran_jabatan }}{% endif %}
                                {% if log.fakultas %} ({{ log.fakultas }}){% endif %}
                            </p>
                        </td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="4" class="py-4 text-center text-slate-500">Belum ada kunjungan hari ini.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
'''

html = html.replace('</div>\n\n<!-- ApexCharts Setup -->', '</div>\n' + table_html + '\n</div>\n\n<!-- ApexCharts Setup -->')

with codecs.open('templates/analitik_kunjungan.html', 'w', 'utf-8') as f:
    f.write(html)

print("Added Daily Log Table")
