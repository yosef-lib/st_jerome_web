import codecs
import re

with codecs.open('templates/anomali.html', 'r', 'utf-8') as f:
    html = f.read()

# I will just regex replace the whole div for the second table
pattern = r'(<!-- Tabel 2: Inkonsistensi Klasifikasi -->.*?)(</div>\s*</div>\s*</div>)'
replacement = '''<!-- Tabel 2: Inkonsistensi Klasifikasi -->
        <div class="rounded-sm border border-stroke bg-white px-5 pt-6 pb-2.5 shadow-default sm:px-7.5 xl:pb-6 mb-6">
            <h4 class="mb-4 text-xl font-semibold text-black">
                Inkonsistensi Klasifikasi (Judul Sama, DDC Beda)
            </h4>
            <p class="text-sm text-slate-500 mb-6">Buku-buku ini memiliki judul yang sama persis, tetapi petugas memberikan nomor klasifikasi DDC yang berbeda. Periksa semua eksemplar di bawah ini untuk melihat nomor panggilnya.</p>
            
            {% if inkonsistensi_dict %}
            <div class="flex flex-col gap-6">
                {% for judul, exemplars in inkonsistensi_dict.items() %}
                <div class="border border-stroke rounded-lg overflow-hidden shadow-sm">
                    <div class="bg-gray-2 py-3 px-4 border-b border-stroke flex flex-col gap-1">
                        <h4 class="font-bold text-black text-sm">{{ judul }}</h4>
                        <span class="text-xs text-slate-500">Pengarang: {{ exemplars[0]['pengarang'] }} | Penerbit: {{ exemplars[0]['penerbit'] }} ({{ exemplars[0]['tahun_terbit'] }})</span>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full table-auto text-sm">
                            <thead>
                                <tr class="bg-white text-left text-slate-500 text-xs uppercase">
                                    <th class="py-2 px-4 font-medium border-b border-stroke">No Induk</th>
                                    <th class="py-2 px-4 font-medium border-b border-stroke">Nomor Panggil (Call Number)</th>
                                    <th class="py-2 px-4 font-medium border-b border-stroke">DDC Dasar</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for ex in exemplars %}
                                <tr class="hover:bg-gray-50 transition border-b border-stroke last:border-b-0">
                                    <td class="py-2 px-4 font-bold text-black">{{ ex['no_induk'] }}</td>
                                    <td class="py-2 px-4 font-bold text-danger">{{ ex['no_panggil'] }}</td>
                                    <td class="py-2 px-4">{{ ex['klasifikasi'] }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <!-- Pagination -->
            <div class="mt-6 flex justify-between items-center border-t border-stroke pt-4">
                {% if page > 1 %}
                <a href="?lokasi={{ lokasi }}&page={{ page - 1 }}" class="rounded border border-primary text-primary py-2 px-4 hover:bg-primary hover:text-white transition font-medium text-sm">
                    <i class="fa-solid fa-chevron-left mr-1"></i> Sebelumnya
                </a>
                {% else %}
                <div></div>
                {% endif %}
                
                <span class="text-sm text-slate-500 font-medium">Halaman {{ page }} dari {{ total_pages }}</span>
                
                {% if page < total_pages %}
                <a href="?lokasi={{ lokasi }}&page={{ page + 1 }}" class="rounded border border-primary text-primary py-2 px-4 hover:bg-primary hover:text-white transition font-medium text-sm">
                    Selanjutnya <i class="fa-solid fa-chevron-right ml-1"></i>
                </a>
                {% else %}
                <div></div>
                {% endif %}
            </div>
            {% else %}
            <div class="py-6 text-center">
                <p class="text-success font-medium">Hebat! Semua buku ber-eksemplar ganda memiliki klasifikasi yang konsisten.</p>
            </div>
            {% endif %}
        </div>
    </div>
</div>'''

html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with codecs.open('templates/anomali.html', 'w', 'utf-8') as f:
    f.write(html)

print("HTML anomali replaced successfully")
