import codecs

with codecs.open('templates/analisis_lanjutan.html', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace('text-gray', 'text-white')

# Add the old tables at the bottom of the grid
end_grid = "    </div>\n</div>\n{% endblock %}"

old_tables = '''
    <!-- C. ANALISIS PERPUTARAN & DORMAN (Legacy) -->
    <div class="mt-4 grid grid-cols-1 gap-4 md:mt-6 md:gap-6 2xl:mt-7.5 2xl:gap-7.5 xl:grid-cols-2">
        <!-- Turnover Rate -->
        <div class="rounded-sm border border-stroke bg-white px-5 pt-6 pb-2.5 shadow-default sm:px-7.5 xl:pb-1">
            <h4 class="mb-4 text-xl font-semibold text-black">
                C. TURNOVER RATE <span class="text-xs font-normal text-warning bg-warning/10 px-2 py-1 rounded">Per DDC</span>
            </h4>
            <p class="text-sm text-slate-500 mb-6">Tingkat perputaran koleksi: Rasio total pinjam/baca dibanding total eksemplar per kelas DDC.</p>
            
            <div class="max-w-full overflow-x-auto">
                <table class="w-full table-auto">
                    <thead>
                        <tr class="bg-gray-2 text-left">
                            <th class="py-2 px-2 font-medium text-black">DDC</th>
                            <th class="py-2 px-2 font-medium text-black text-center">Eksemplar</th>
                            <th class="py-2 px-2 font-medium text-black text-center">Dipinjam</th>
                            <th class="py-2 px-2 font-medium text-black text-center">Turnover</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for t in turnover_data %}
                        <tr>
                            <td class="border-b border-[#eee] py-3 px-2 font-medium text-black">{{ t.ddc_group }}</td>
                            <td class="border-b border-[#eee] py-3 px-2 text-center">{{ t.total_eksemplar }}</td>
                            <td class="border-b border-[#eee] py-3 px-2 text-center">{{ t.total_pinjam }}</td>
                            <td class="border-b border-[#eee] py-3 px-2 text-center font-bold text-primary">
                                {% if t.total_eksemplar > 0 %}
                                    {{ (t.total_pinjam / t.total_eksemplar)|round(2) }}
                                {% else %}
                                    0
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Dead Stock -->
        <div class="rounded-sm border border-stroke bg-white px-5 pt-6 pb-2.5 shadow-default sm:px-7.5 xl:pb-1">
            <h4 class="mb-4 text-xl font-semibold text-black">
                D. DEAD STOCK <span class="text-xs font-normal text-danger bg-danger/10 px-2 py-1 rounded">Buku Dorman</span>
            </h4>
            <p class="text-sm text-slate-500 mb-6">Buku yang tidak pernah dipinjam atau dibaca. Calon kuat untuk penyiangan (weeding).</p>
            
            <div class="max-w-full overflow-x-auto">
                <table class="w-full table-auto text-sm">
                    <thead>
                        <tr class="bg-gray-2 text-left">
                            <th class="py-2 px-2 font-medium text-black">Judul</th>
                            <th class="py-2 px-2 font-medium text-black">DDC</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for b in dead_stock %}
                        <tr>
                            <td class="border-b border-[#eee] py-3 px-2 line-clamp-1" title="{{ b.judul }}">{{ b.judul }}</td>
                            <td class="border-b border-[#eee] py-3 px-2">{{ b.klasifikasi }}</td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="2" class="text-center py-4 text-slate-500">Tidak ada buku dorman.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <div class="mt-6 flex flex-col gap-2">
                <h5 class="text-sm font-bold text-black">Rasio Aktivitas Peminjaman</h5>
                <div class="flex items-center justify-between">
                    <span class="text-sm text-slate-500">Meja Baca (In-House)</span>
                    <span class="text-sm font-bold text-success">{{ total_in_house }}</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-sm text-slate-500">Bawa Pulang (SLiMS)</span>
                    <span class="text-sm font-bold text-primary">{{ total_external }}</span>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

content = content.replace(end_grid, old_tables)

with codecs.open('templates/analisis_lanjutan.html', 'w', 'utf-8') as f:
    f.write(content)
print("UI fixed")
