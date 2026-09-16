import codecs

with codecs.open('templates/audit_rak.html', 'r', 'utf-8') as f:
    content = f.read()

# I will append the history and stats UI right after the resultBox div, before closing the main div.
target = '''            <!-- Result Box -->
            <div id="resultBox" class="hidden text-center rounded-lg border-2 p-5 mb-5 animate-[fadeIn_0.3s_ease-out]">
                <i id="resultIcon" class="fa-solid text-4xl mb-2"></i>
                <div id="resultTitle" class="font-bold text-xl mb-1"></div>
                <div id="resultDesc" class="font-semibold text-black text-sm"></div>
            </div>
        </div>
    </div>'''

replacement = '''            <!-- Result Box -->
            <div id="resultBox" class="hidden text-center rounded-lg border-2 p-5 mb-5 animate-[fadeIn_0.3s_ease-out]">
                <i id="resultIcon" class="fa-solid text-4xl mb-2"></i>
                <div id="resultTitle" class="font-bold text-xl mb-1"></div>
                <div id="resultDesc" class="font-semibold text-black text-sm"></div>
            </div>
        </div>
    </div>

    <!-- STATISTIK & RIWAYAT -->
    <div class="mt-6 rounded-sm border border-stroke bg-white shadow-default p-6">
        <div class="flex items-center justify-between mb-4">
            <h4 class="text-xl font-bold text-black">Riwayat Sensus & Audit</h4>
            
            <form action="/reset_audit" method="POST" onsubmit="return confirm('Yakin ingin menghapus seluruh riwayat stok opname saat ini? Pastikan Anda sudah merekapnya.');">
                <button type="submit" class="flex items-center gap-2 rounded bg-danger py-2 px-4 font-medium text-white hover:bg-opacity-90 transition text-sm">
                    <i class="fa-solid fa-trash"></i> Reset Data
                </button>
            </form>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-4 gap-4 mb-6">
            <div class="bg-gray-2 rounded p-3 text-center border-b-4 border-primary">
                <div class="text-2xl font-bold text-black">{{ stats.total }}</div>
                <div class="text-xs text-slate-500 uppercase">Total Scan</div>
            </div>
            <div class="bg-success/10 rounded p-3 text-center border-b-4 border-success">
                <div class="text-2xl font-bold text-success">{{ stats.benar or 0 }}</div>
                <div class="text-xs text-slate-500 uppercase">Sesuai Rak</div>
            </div>
            <div class="bg-danger/10 rounded p-3 text-center border-b-4 border-danger">
                <div class="text-2xl font-bold text-danger">{{ stats.salah or 0 }}</div>
                <div class="text-xs text-slate-500 uppercase">Salah Rak</div>
            </div>
            <div class="bg-warning/10 rounded p-3 text-center border-b-4 border-warning">
                <div class="text-2xl font-bold text-warning">{{ stats.anomali or 0 }}</div>
                <div class="text-xs text-slate-500 uppercase">Anomali</div>
            </div>
        </div>

        <!-- History Table -->
        <div class="max-w-full overflow-x-auto">
            <table class="w-full table-auto text-sm">
                <thead>
                    <tr class="bg-gray-2 text-left">
                        <th class="py-2 px-3 font-medium text-black">Waktu</th>
                        <th class="py-2 px-3 font-medium text-black">No Induk</th>
                        <th class="py-2 px-3 font-medium text-black">Judul</th>
                        <th class="py-2 px-3 font-medium text-black">Target</th>
                        <th class="py-2 px-3 font-medium text-black">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for r in riwayat %}
                    <tr class="{% if loop.index0 == 0 %}bg-primary/5{% endif %}">
                        <td class="border-b border-[#eee] py-3 px-3 text-slate-500 text-xs">{{ r.waktu_scan[-8:] }}</td>
                        <td class="border-b border-[#eee] py-3 px-3 font-bold">{{ r.no_induk }}</td>
                        <td class="border-b border-[#eee] py-3 px-3 line-clamp-1" title="{{ r.judul }}">{{ r.judul }}</td>
                        <td class="border-b border-[#eee] py-3 px-3 font-bold">{{ r.rak_target }}</td>
                        <td class="border-b border-[#eee] py-3 px-3">
                            {% if r.status_audit == 'BENAR' %}
                                <span class="bg-success/10 text-success px-2 py-1 rounded text-xs font-bold"><i class="fa-solid fa-check"></i> BENAR</span>
                            {% elif r.status_audit == 'SALAH RAK' %}
                                <span class="bg-danger/10 text-danger px-2 py-1 rounded text-xs font-bold"><i class="fa-solid fa-xmark"></i> SALAH RAK ({{ r.klasifikasi }})</span>
                            {% else %}
                                <span class="bg-warning/10 text-warning px-2 py-1 rounded text-xs font-bold"><i class="fa-solid fa-triangle-exclamation"></i> ANOMALI</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="5" class="text-center py-6 text-slate-500">Belum ada buku yang diaudit. Silakan mulai memindai!</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>'''

content = content.replace(target, replacement)

# We also want to auto-refresh the page when a scan happens so the history updates!
# Or we can just let them refresh manually. Let's add a JS location.reload() after a delay.
# Wait, reloading destroys the camera scanning session!
# It's better to just prepend the new row via JS, but that's complex. Let's just update the JS to reload the page IF they used manual input, or just tell them "Refresh to see full history".
# Even better: The user scans 50 books in a row using their HP camera. When they are done, they stop the camera, the page refreshes, and they see the history.
# So I'll add setTimeout(() => location.reload(), 2000) inside the Stop button!
# But wait, manual inputs don't reload either. I'll just put a refresh button.

refresh_btn = '''        <div class="flex items-center justify-between mb-4">
            <h4 class="text-xl font-bold text-black">Riwayat Sensus & Audit</h4>
            
            <div class="flex gap-2">
                <button onclick="location.reload()" class="flex items-center gap-2 rounded bg-primary py-2 px-4 font-medium text-white hover:bg-opacity-90 transition text-sm">
                    <i class="fa-solid fa-rotate"></i> Segarkan Tabel
                </button>
                <form action="/reset_audit" method="POST" onsubmit="return confirm('Yakin ingin menghapus seluruh riwayat stok opname saat ini? Pastikan Anda sudah merekapnya.');">
                    <button type="submit" class="flex items-center gap-2 rounded bg-danger py-2 px-4 font-medium text-white hover:bg-opacity-90 transition text-sm">
                        <i class="fa-solid fa-trash"></i> Reset Data
                    </button>
                </form>
            </div>
        </div>'''
content = content.replace('''        <div class="flex items-center justify-between mb-4">
            <h4 class="text-xl font-bold text-black">Riwayat Sensus & Audit</h4>
            
            <form action="/reset_audit" method="POST" onsubmit="return confirm('Yakin ingin menghapus seluruh riwayat stok opname saat ini? Pastikan Anda sudah merekapnya.');">
                <button type="submit" class="flex items-center gap-2 rounded bg-danger py-2 px-4 font-medium text-white hover:bg-opacity-90 transition text-sm">
                    <i class="fa-solid fa-trash"></i> Reset Data
                </button>
            </form>
        </div>''', refresh_btn)

with codecs.open('templates/audit_rak.html', 'w', 'utf-8') as f:
    f.write(content)

print("audit UI updated")
