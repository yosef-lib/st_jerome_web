import codecs
import re

with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    code = f.read()

if 'alpinejs' not in code:
    code = code.replace('</head>', '    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>\n</head>')

new_nav = '''<nav class="mt-5 py-4 px-4 lg:mt-6 lg:px-6">
                    <ul class="flex flex-col gap-1.5">
                        
                        <!-- Menu Beranda -->
                        <li>
                            <a href="/" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if request.path == '/' %}bg-primary text-white{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                <i class="fa-solid fa-home w-5 text-center"></i> Beranda Utama
                            </a>
                        </li>

                        <!-- Menu Sirkulasi & Koleksi -->
                        {% set koleksi_active = request.path.startswith('/koleksi') or request.path == '/input_buku' or request.path == '/audit_rak' %}
                        <li x-data="{ expanded: {{ 'true' if koleksi_active else 'false' }} }">
                            <a href="#" @click.prevent="expanded = !expanded" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if koleksi_active %}text-white bg-boxdark2{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                <i class="fa-solid fa-book w-5 text-center"></i> Sirkulasi & Koleksi
                                <i class="fa-solid fa-chevron-down absolute right-4 transition-transform duration-200" :class="{ 'rotate-180': expanded }"></i>
                            </a>
                            <div x-show="expanded" style="display: none;" x-transition>
                                <ul class="mt-2 flex flex-col gap-1 pl-10 pr-2 pb-2">
                                    <li><a href="/koleksi" class="flex rounded-md px-3 py-2 text-sm {% if request.path.startswith('/koleksi') %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Daftar Koleksi</a></li>
                                    <li><a href="/input_buku" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/input_buku' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Input Buku Baru</a></li>
                                    <li><a href="/audit_rak" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/audit_rak' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Audit Rak</a></li>
                                </ul>
                            </div>
                        </li>

                        <!-- Menu Cetak & Label -->
                        {% set cetak_active = request.path == '/cetak_khusus' or request.path == '/cetak_sirkulasi' %}
                        <li x-data="{ expanded: {{ 'true' if cetak_active else 'false' }} }">
                            <a href="#" @click.prevent="expanded = !expanded" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if cetak_active %}text-white bg-boxdark2{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                <i class="fa-solid fa-print w-5 text-center"></i> Cetak & Label
                                <i class="fa-solid fa-chevron-down absolute right-4 transition-transform duration-200" :class="{ 'rotate-180': expanded }"></i>
                            </a>
                            <div x-show="expanded" style="display: none;" x-transition>
                                <ul class="mt-2 flex flex-col gap-1 pl-10 pr-2 pb-2">
                                    <li><a href="/cetak_sirkulasi" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/cetak_sirkulasi' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Kartu & Kantong Buku</a></li>
                                    <li><a href="/cetak_khusus" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/cetak_khusus' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Stiker Eksemplar Khusus</a></li>
                                </ul>
                            </div>
                        </li>

                        <!-- Menu Keanggotaan & Kunjungan -->
                        {% set anggota_active = request.path.startswith('/anggota') or request.path == '/scan' or request.path == '/analitik_kunjungan' %}
                        <li x-data="{ expanded: {{ 'true' if anggota_active else 'false' }} }">
                            <a href="#" @click.prevent="expanded = !expanded" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if anggota_active %}text-white bg-boxdark2{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                <i class="fa-solid fa-users w-5 text-center"></i> Anggota & Kunjungan
                                <i class="fa-solid fa-chevron-down absolute right-4 transition-transform duration-200" :class="{ 'rotate-180': expanded }"></i>
                            </a>
                            <div x-show="expanded" style="display: none;" x-transition>
                                <ul class="mt-2 flex flex-col gap-1 pl-10 pr-2 pb-2">
                                    <li><a href="/anggota" class="flex rounded-md px-3 py-2 text-sm {% if request.path.startswith('/anggota') %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Daftar Keanggotaan</a></li>
                                    <li><a href="/scan" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/scan' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Scanner Meja Baca</a></li>
                                    <li><a href="/analitik_kunjungan" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/analitik_kunjungan' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Analitik Kunjungan</a></li>
                                </ul>
                            </div>
                        </li>

                        <!-- Menu Laporan & Analisis -->
                        {% set lapor_active = request.path == '/dashboard' or request.path == '/analisis_lanjutan' or request.path == '/anomali' %}
                        <li x-data="{ expanded: {{ 'true' if lapor_active else 'false' }} }">
                            <a href="#" @click.prevent="expanded = !expanded" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if lapor_active %}text-white bg-boxdark2{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                <i class="fa-solid fa-chart-line w-5 text-center"></i> Laporan & Analisis
                                <i class="fa-solid fa-chevron-down absolute right-4 transition-transform duration-200" :class="{ 'rotate-180': expanded }"></i>
                            </a>
                            <div x-show="expanded" style="display: none;" x-transition>
                                <ul class="mt-2 flex flex-col gap-1 pl-10 pr-2 pb-2">
                                    <li><a href="/dashboard" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/dashboard' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Analisis Dasar</a></li>
                                    <li><a href="/analisis_lanjutan" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/analisis_lanjutan' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Analisis Lanjutan</a></li>
                                    <li><a href="/anomali" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/anomali' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Kualitas Data</a></li>
                                </ul>
                            </div>
                        </li>

                        <!-- Menu Sinkronisasi & Backup -->
                        {% set sinkron_active = request.path == '/import_slims' or request.path == '/export_biblio' or request.path == '/export_item' or request.path == '/backup' %}
                        <li x-data="{ expanded: {{ 'true' if sinkron_active else 'false' }} }">
                            <a href="#" @click.prevent="expanded = !expanded" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium duration-300 ease-in-out {% if sinkron_active %}text-white bg-boxdark2{% else %}text-bodydark hover:bg-boxdark2 hover:text-white{% endif %}">
                                <i class="fa-solid fa-cloud-arrow-up w-5 text-center"></i> Sinkronisasi & Sistem
                                <i class="fa-solid fa-chevron-down absolute right-4 transition-transform duration-200" :class="{ 'rotate-180': expanded }"></i>
                            </a>
                            <div x-show="expanded" style="display: none;" x-transition>
                                <ul class="mt-2 flex flex-col gap-1 pl-10 pr-2 pb-2">
                                    <li><a href="/import_slims" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/import_slims' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Integrasi SLiMS</a></li>
                                    <li><a href="/export_biblio" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/export_biblio' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Ekspor Bibliografi</a></li>
                                    <li><a href="/export_item" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/export_item' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Ekspor Item</a></li>
                                    <li><a href="/backup" class="flex rounded-md px-3 py-2 text-sm {% if request.path == '/backup' %}text-white font-medium{% else %}text-bodydark2 hover:text-white{% endif %}">Backup Database</a></li>
                                </ul>
                            </div>
                        </li>

                    </ul>

                    <ul class="mt-8 flex flex-col gap-1.5 border-t border-boxdark2 pt-4">
                        <li>
                            <a href="/logout" class="group relative flex items-center gap-3 rounded-md px-4 py-3 font-medium text-danger duration-300 ease-in-out hover:bg-boxdark2 hover:text-white">
                                <i class="fa-solid fa-power-off w-5 text-center"></i> Keluar
                            </a>
                        </li>
                    </ul>
                </nav>'''

# Replace from <nav ...> to </nav>
pattern = re.compile(r'<nav class="mt-5 py-4 px-4 lg:mt-6 lg:px-6">.*?</nav>', re.DOTALL)
code = pattern.sub(new_nav, code)

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(code)
print("Menu rebuilt")
