import codecs
import re

with codecs.open('templates/analitik_kunjungan.html', 'r', 'utf-8') as f:
    html = f.read()

# Update title block to add a top filter form
old_title = '''<div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h2 class="text-title-md2 font-bold text-black dark:text-white">
            Analitik Kunjungan
        </h2>
        <nav>
            <ol class="flex items-center gap-2">
                <li><a class="font-medium" href="/">Beranda /</a></li>
                <li class="font-medium text-primary">Analitik Kunjungan</li>
            </ol>
        </nav>
    </div>'''

new_title = '''<div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
            <h2 class="text-title-md2 font-bold text-black dark:text-white">
                Analitik Kunjungan
            </h2>
            <p class="text-sm text-slate-500 mt-1">{% if start_date == end_date %}{{ start_date }}{% else %}{{ start_date }} s/d {{ end_date }}{% endif %}</p>
        </div>
        <form method="GET" action="/analitik_kunjungan" class="flex items-center gap-2 bg-white border border-stroke rounded-lg p-2 shadow-sm">
            <input type="date" name="start_date" value="{{ start_date }}" class="text-sm rounded outline-none border border-stroke px-2 py-1 focus:border-primary">
            <span class="text-sm text-slate-400">s/d</span>
            <input type="date" name="end_date" value="{{ end_date }}" class="text-sm rounded outline-none border border-stroke px-2 py-1 focus:border-primary">
            <button type="submit" class="bg-primary text-white text-sm px-3 py-1 rounded hover:bg-opacity-90 transition"><i class="fa-solid fa-filter"></i> Filter</button>
        </form>
    </div>'''
html = html.replace(old_title, new_title)

# Update texts
html = html.replace('Kunjungan Hari Ini', 'Total Kunjungan')
html = html.replace('Fakultas Hari Ini', 'Sebaran Fakultas')
html = html.replace('Demografi Asal Instansi (Bulan Ini)', 'Demografi Asal Instansi')
html = html.replace('Top 10 Pengunjung Loyal (Bulan Ini)', 'Top 10 Pengunjung Loyal')
html = html.replace('Rincian Kunjungan Hari Ini', 'Log Rincian Kunjungan')
html = html.replace('Belum ada kunjungan hari ini.', 'Tidak ada kunjungan pada rentang tanggal ini.')

with codecs.open('templates/analitik_kunjungan.html', 'w', 'utf-8') as f:
    f.write(html)

print("Updated templates filter")
