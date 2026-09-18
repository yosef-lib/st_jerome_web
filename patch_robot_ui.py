import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    html = f.read()

old_ui = """    </div>
    
    <div class="p-4 border-b border-stroke bg-slate-50 flex gap-2">"""

new_ui = """    </div>
    
    <!-- Robot Pencari Sampul -->
    <div class="p-4 bg-indigo-50 border-b border-indigo-200 flex items-center justify-between">
        <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center text-lg">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div>
                <h3 class="font-bold text-indigo-900">Robot Pencari Sampul Otomatis</h3>
                <p class="text-xs text-indigo-700">Mencari sampul buku yang tidak memiliki ISBN (menggunakan Judul & Pengarang).</p>
            </div>
        </div>
        <div>
            <template x-if="!autoCover.active">
                <button @click="startRobot" class="px-4 py-2 bg-indigo-600 text-white rounded font-semibold text-sm hover:bg-indigo-700 transition shadow-sm"><i class="fa-solid fa-play mr-2"></i> Jalankan Robot</button>
            </template>
            <template x-if="autoCover.active">
                <div class="flex items-center gap-3">
                    <div class="text-xs text-indigo-800 font-semibold text-right">
                        Sedang memproses...<br>
                        <span class="font-normal" x-text="autoCover.processed + ' / ' + autoCover.total"></span> - <span class="font-normal truncate inline-block w-40 align-bottom" x-text="autoCover.currentTitle"></span>
                    </div>
                    <button @click="stopRobot" class="px-3 py-1.5 bg-red-500 text-white rounded font-semibold text-sm hover:bg-red-600 transition shadow-sm"><i class="fa-solid fa-stop mr-1"></i> Hentikan</button>
                </div>
            </template>
        </div>
    </div>

    <div class="p-4 border-b border-stroke bg-slate-50 flex gap-2">"""

html = html.replace(old_ui, new_ui)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(html)
print("Robot UI patched!")
