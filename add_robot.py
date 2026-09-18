import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

# 1. Add Alpine logic
old_alpine = "isLoadingEksemplar: false,"
new_alpine = """isLoadingEksemplar: false,
        
        autoCover: {
            active: false,
            processed: 0,
            total: 0,
            currentTitle: '',
        },
        
        async startRobot() {
            if(!confirm("Robot ini akan mencari sampul buku di internet satu-per-satu. Proses ini membutuhkan waktu (sekitar 1 detik per buku). Biarkan halaman ini tetap terbuka selama robot bekerja.\\n\\nJalankan robot sekarang?")) return;
            
            this.autoCover.active = true;
            this.autoCover.processed = 0;
            
            while(this.autoCover.active) {
                // Get batch of 50
                const res = await fetch('/api/buku/missing_covers');
                const books = await res.json();
                if(books.length === 0) {
                    alert("Hore! Semua buku (yang bisa dicari) sudah diproses!");
                    this.autoCover.active = false;
                    break;
                }
                
                this.autoCover.total = books.length;
                this.autoCover.processed = 0;
                
                for(let b of books) {
                    if(!this.autoCover.active) break;
                    this.autoCover.currentTitle = b.judul;
                    
                    try {
                        const q = "intitle:" + b.judul + (b.pengarang ? "+inauthor:" + b.pengarang : "");
                        const gRes = await fetch("https://www.googleapis.com/books/v1/volumes?q=" + encodeURIComponent(q));
                        if(gRes.ok) {
                            const gData = await gRes.json();
                            if(gData.items && gData.items.length > 0) {
                                let img = gData.items[0].volumeInfo?.imageLinks?.thumbnail;
                                if(img) {
                                    // replace http with https
                                    img = img.replace("http:", "https:");
                                    await fetch('/api/buku/save_cover', {
                                        method: 'POST',
                                        headers: {'Content-Type': 'application/json'},
                                        body: JSON.stringify({id: b.id, url: img})
                                    });
                                }
                            }
                        }
                    } catch(e) {
                        console.error(e);
                    }
                    this.autoCover.processed++;
                    // sleep 1 second
                    await new Promise(r => setTimeout(r, 1000));
                }
                
                // Refresh list if robot finished a batch
                this.loadBibliografi();
            }
        },
        
        stopRobot() {
            this.autoCover.active = false;
        },"""

code = code.replace(old_alpine, new_alpine)

# 2. Add UI above the table
old_ui = """<div class="mb-4">
            <div class="relative">"""

new_ui = """
        <!-- Robot Pencari Sampul -->
        <div class="mb-4 p-4 bg-indigo-50 border border-indigo-200 rounded-lg flex items-center justify-between">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center text-xl">
                    <i class="fa-solid fa-robot"></i>
                </div>
                <div>
                    <h3 class="font-bold text-indigo-900">Robot Pencari Sampul Otomatis</h3>
                    <p class="text-sm text-indigo-700">Mencari sampul buku yang tidak memiliki ISBN menggunakan Judul & Pengarang.</p>
                </div>
            </div>
            <div>
                <template x-if="!autoCover.active">
                    <button @click="startRobot" class="px-4 py-2 bg-indigo-600 text-white rounded font-semibold hover:bg-indigo-700 transition shadow-sm"><i class="fa-solid fa-play mr-2"></i> Jalankan Robot</button>
                </template>
                <template x-if="autoCover.active">
                    <div class="flex items-center gap-3">
                        <div class="text-sm text-indigo-800 font-semibold text-right">
                            Sedang memproses...<br>
                            <span class="font-normal" x-text="autoCover.processed + ' / ' + autoCover.total"></span> - <span class="font-normal truncate block w-40" x-text="autoCover.currentTitle"></span>
                        </div>
                        <button @click="stopRobot" class="px-4 py-2 bg-red-500 text-white rounded font-semibold hover:bg-red-600 transition shadow-sm"><i class="fa-solid fa-stop mr-2"></i> Hentikan</button>
                    </div>
                </template>
            </div>
        </div>

        <div class="mb-4">
            <div class="relative">"""

code = code.replace(old_ui, new_ui)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("Robot feature added")
