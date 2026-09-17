import codecs

with codecs.open('templates/input_stiker.html', 'r', 'utf-8') as f:
    html = f.read()

# Add a small form in the right panel for existing books
old_panel_header = '''        <div class="xl:col-span-1 rounded-sm border border-stroke bg-white shadow-default sticky top-24">
            <div class="border-b border-stroke py-4 px-6">
                <h3 class="font-medium text-black">
                    <i class="fa-solid fa-list-ol mr-2 text-primary"></i> Antrean Cetak Stiker
                </h3>
                <p class="text-sm text-slate-500 mt-1">Hanya buku baru yang diinput langsung</p>
            </div>'''
            
new_panel_header = '''        <div class="xl:col-span-1 rounded-sm border border-stroke bg-white shadow-default sticky top-24">
            <!-- Search Existing Book -->
            <div class="border-b border-stroke py-4 px-6 bg-gray-50">
                <h3 class="font-medium text-black text-sm mb-2">
                    <i class="fa-solid fa-search mr-2 text-primary"></i> Cetak Ulang Buku Lama
                </h3>
                <div class="flex gap-2">
                    <input type="text" id="inputNoIndukLama" placeholder="Ketik No Induk (Barcode)" class="w-full rounded border-[1.5px] border-stroke bg-white py-1.5 px-3 text-sm outline-none transition focus:border-primary">
                    <button type="button" onclick="tambahBukuLama()" class="bg-primary text-white px-3 rounded hover:bg-opacity-90 transition text-sm">
                        <i class="fa-solid fa-plus"></i>
                    </button>
                </div>
            </div>

            <div class="border-b border-stroke py-4 px-6">
                <h3 class="font-medium text-black">
                    <i class="fa-solid fa-list-ol mr-2 text-primary"></i> Antrean Cetak Stiker
                </h3>
            </div>'''
            
html = html.replace(old_panel_header, new_panel_header)

# Add JS function
js_script = '''
    async function tambahBukuLama() {
        const input = document.getElementById('inputNoIndukLama');
        const no_induk = input.value.trim();
        if(!no_induk) return;
        
        try {
            const res = await fetch('/api/antrean/existing', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({no_induk: no_induk})
            });
            const data = await res.json();
            if(data.status === 'success') {
                input.value = '';
                muatAntrean();
            } else {
                alert(data.message || 'Gagal menambahkan buku lama.');
            }
        } catch(e) {
            alert('Terjadi kesalahan jaringan.');
        }
    }
'''

html = html.replace('function kosongkanAntrean() {', js_script + '\n    function kosongkanAntrean() {')

with codecs.open('templates/input_stiker.html', 'w', 'utf-8') as f:
    f.write(html)

print("success ui")
