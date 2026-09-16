import codecs

with codecs.open('templates/audit_rak.html', 'r', 'utf-8') as f:
    html = f.read()

old_content = '''        <div class="p-6">
            <div id="reader" class="rounded-lg overflow-hidden border-2 border-stroke bg-black w-full min-h-[250px] flex items-center justify-center relative">
                <button id="btnStartScan" class="absolute z-10 flex items-center gap-2 rounded bg-warning py-3 px-6 font-medium text-black hover:bg-opacity-90 transition shadow-lg">
                    <i class="fa-solid fa-camera"></i> Buka Kamera HP
                </button>
            </div>
            
            <div class="mt-4 flex justify-center hidden" id="scanActions">
                <button id="btnStopScan" class="flex items-center gap-2 rounded border border-danger text-danger py-1.5 px-4 font-medium hover:bg-danger hover:text-white transition text-sm">
                    <i class="fa-solid fa-stop"></i> Hentikan Kamera
                </button>
            </div>
            
            <!-- Manual Input -->
            <div class="mt-6 mb-5">
                <label class="mb-2 block text-sm font-bold text-black">Atau Masukkan Manual / Gunakan Scanner Fisik:</label>
                <div class="flex gap-2">
                    <input type="text" id="manualInput" autofocus placeholder="Ketik No. Induk..." onkeypress="if(event.key === 'Enter') submitManual()" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2 px-4 outline-none transition focus:border-warning active:border-warning">
                    <button class="flex items-center justify-center rounded bg-warning py-2 px-5 font-medium text-black hover:bg-opacity-90 transition" onclick="submitManual()">Cek Rak</button>
                </div>
            </div>

            <hr class="border-stroke mb-5">
            
            <div class="mt-8 flex justify-between items-center mb-4">
                <h4 class="text-title-sm2 font-bold text-black">Riwayat Audit Sesi Ini</h4>
                <button onclick="window.location.href='/export_audit'" class="flex items-center gap-2 rounded border border-primary text-primary py-1 px-3 hover:bg-primary hover:text-white transition text-xs font-medium">
                    <i class="fa-solid fa-file-excel"></i> Ekspor Excel
                </button>
            </div>
            
            <div class="grid grid-cols-4 gap-2 mb-4 text-center">
                <div class="rounded border border-stroke bg-gray-2 py-2">
                    <div class="text-2xl font-bold text-black">{{ stats.total or 0 }}</div>
                    <div class="text-xs text-slate-500 uppercase">Total</div>
                </div>
                <div class="rounded border border-stroke bg-success/10 py-2">
                    <div class="text-2xl font-bold text-success">{{ stats.sesuai or 0 }}</div>
                    <div class="text-xs text-slate-500 uppercase">Sesuai</div>
                </div>
                <div class="rounded border border-stroke bg-danger/10 py-2">
                    <div class="text-2xl font-bold text-danger">{{ stats.salah or 0 }}</div>
                    <div class="text-xs text-slate-500 uppercase">Salah</div>
                </div>
                <div class="rounded border border-stroke bg-warning/10 py-2">
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
                        {% for row in history %}
                        <tr class="border-b border-[#eee]">
                            <td class="py-2 px-3">{{ row['scan_time'].split(' ')[1] }}</td>
                            <td class="py-2 px-3 font-medium">{{ row['no_induk'] }}</td>
                            <td class="py-2 px-3 truncate max-w-[120px]" title="{{ row['judul'] }}">{{ row['judul'] }}</td>
                            <td class="py-2 px-3">{{ row['target_rak'] }}</td>
                            <td class="py-2 px-3">
                                {% if row['status_match'] == 'SESUAI' %}
                                <span class="inline-flex rounded-full bg-success bg-opacity-10 py-1 px-2 text-xs font-medium text-success">SESUAI</span>
                                {% elif row['status_match'] == 'SALAH RAK' %}
                                <span class="inline-flex rounded-full bg-danger bg-opacity-10 py-1 px-2 text-xs font-medium text-danger">SALAH RAK</span>
                                {% else %}
                                <span class="inline-flex rounded-full bg-warning bg-opacity-10 py-1 px-2 text-xs font-medium text-warning">ANOMALI</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>'''

new_content = '''        <div class="p-6 grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Left Side: Scanner -->
            <div class="lg:col-span-1 flex flex-col">
                <div id="reader" class="rounded-lg overflow-hidden border-2 border-stroke bg-black w-full h-[300px] flex items-center justify-center relative">
                    <button id="btnStartScan" class="absolute z-10 flex items-center gap-2 rounded bg-warning py-3 px-6 font-medium text-black hover:bg-opacity-90 transition shadow-lg">
                        <i class="fa-solid fa-camera"></i> Buka Kamera HP
                    </button>
                </div>
                
                <div class="mt-4 flex justify-center hidden" id="scanActions">
                    <button id="btnStopScan" class="flex items-center gap-2 rounded border border-danger text-danger py-1.5 px-4 font-medium hover:bg-danger hover:text-white transition text-sm">
                        <i class="fa-solid fa-stop"></i> Hentikan Kamera
                    </button>
                </div>
                
                <!-- Manual Input -->
                <div class="mt-6 mb-5">
                    <label class="mb-2 block text-sm font-bold text-black">Atau Masukkan Manual / Gunakan Scanner Fisik:</label>
                    <div class="flex flex-col xl:flex-row gap-2">
                        <input type="text" id="manualInput" autofocus placeholder="Ketik No. Induk..." onkeypress="if(event.key === 'Enter') submitManual()" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2 px-4 outline-none transition focus:border-warning active:border-warning">
                        <button class="flex items-center justify-center rounded bg-warning py-2 px-5 font-medium text-black hover:bg-opacity-90 transition whitespace-nowrap" onclick="submitManual()">Cek Rak</button>
                    </div>
                </div>
                
                <div class="grid grid-cols-2 gap-2 text-center mt-auto">
                    <div class="rounded border border-stroke bg-gray-2 py-2">
                        <div class="text-xl font-bold text-black">{{ stats.total or 0 }}</div>
                        <div class="text-xs text-slate-500 uppercase">Total</div>
                    </div>
                    <div class="rounded border border-stroke bg-success/10 py-2">
                        <div class="text-xl font-bold text-success">{{ stats.sesuai or 0 }}</div>
                        <div class="text-xs text-slate-500 uppercase">Sesuai</div>
                    </div>
                    <div class="rounded border border-stroke bg-danger/10 py-2">
                        <div class="text-xl font-bold text-danger">{{ stats.salah or 0 }}</div>
                        <div class="text-xs text-slate-500 uppercase">Salah</div>
                    </div>
                    <div class="rounded border border-stroke bg-warning/10 py-2">
                        <div class="text-xl font-bold text-warning">{{ stats.anomali or 0 }}</div>
                        <div class="text-xs text-slate-500 uppercase">Anomali</div>
                    </div>
                </div>
            </div>
            
            <!-- Right Side: History -->
            <div class="lg:col-span-2 border-t lg:border-t-0 lg:border-l border-stroke pt-6 lg:pt-0 lg:pl-8 flex flex-col">
                <div class="flex justify-between items-center mb-4">
                    <h4 class="text-title-sm2 font-bold text-black">Riwayat Audit Sesi Ini</h4>
                    <button onclick="window.location.href='/export_audit'" class="flex items-center gap-2 rounded border border-primary text-primary py-1 px-3 hover:bg-primary hover:text-white transition text-xs font-medium">
                        <i class="fa-solid fa-file-excel"></i> Ekspor Excel
                    </button>
                </div>

                <!-- History Table -->
                <div class="max-w-full overflow-x-auto bg-white rounded border border-stroke">
                    <table class="w-full table-auto text-sm">
                        <thead>
                            <tr class="bg-gray-2 text-left">
                                <th class="py-3 px-4 font-bold text-black border-b border-stroke">Waktu</th>
                                <th class="py-3 px-4 font-bold text-black border-b border-stroke">No Induk</th>
                                <th class="py-3 px-4 font-bold text-black border-b border-stroke">Judul</th>
                                <th class="py-3 px-4 font-bold text-black border-b border-stroke">Target</th>
                                <th class="py-3 px-4 font-bold text-black border-b border-stroke">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in history %}
                            <tr class="border-b border-[#eee] hover:bg-gray-50">
                                <td class="py-3 px-4">{{ row['scan_time'].split(' ')[1] }}</td>
                                <td class="py-3 px-4 font-medium">{{ row['no_induk'] }}</td>
                                <td class="py-3 px-4 truncate max-w-[200px]" title="{{ row['judul'] }}">{{ row['judul'] }}</td>
                                <td class="py-3 px-4">{{ row['target_rak'] }}</td>
                                <td class="py-3 px-4">
                                    {% if row['status_match'] == 'SESUAI' %}
                                    <span class="inline-flex rounded-full bg-success bg-opacity-10 py-1 px-3 text-xs font-bold text-success">SESUAI</span>
                                    {% elif row['status_match'] == 'SALAH RAK' %}
                                    <span class="inline-flex rounded-full bg-danger bg-opacity-10 py-1 px-3 text-xs font-bold text-danger">SALAH RAK</span>
                                    {% else %}
                                    <span class="inline-flex rounded-full bg-warning bg-opacity-10 py-1 px-3 text-xs font-bold text-warning">ANOMALI</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                            {% if not history %}
                            <tr>
                                <td colspan="5" class="py-6 text-center text-slate-500">Belum ada riwayat scan hari ini.</td>
                            </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </div>
            
        </div>'''

html = html.replace(old_content, new_content)

with codecs.open('templates/audit_rak.html', 'w', 'utf-8') as f:
    f.write(html)

print("audit rak grid layout fixed")
