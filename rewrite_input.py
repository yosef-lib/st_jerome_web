import codecs

new_html = '''{% extends "layout.html" %}
{% block content %}
<div x-data="inputBuku()" class="max-w-4xl mx-auto bg-white rounded-lg shadow-sm border border-stroke overflow-hidden">
    <div class="bg-primary px-6 py-4 border-b border-stroke flex justify-between items-center">
        <h2 class="text-lg font-bold text-white"><i class="fa-solid fa-book-medical mr-2"></i> Input Buku Baru</h2>
    </div>
    
    <div class="p-6">
        <!-- Notifikasi -->
        <div x-show="notif.show" :class="notif.type === 'success' ? 'bg-success/10 text-success border-success' : 'bg-danger/10 text-danger border-danger'" class="border px-4 py-3 rounded mb-6 flex justify-between items-center">
            <div>
                <strong class="font-bold" x-text="notif.title"></strong>
                <span class="block text-sm" x-text="notif.message"></span>
            </div>
            <button @click="notif.show = false"><i class="fa-solid fa-xmark"></i></button>
        </div>

        <form @submit.prevent="submitForm">
            <!-- SECTION 1: Bibliografi -->
            <div class="mb-8">
                <h3 class="text-md font-semibold border-b border-stroke pb-2 mb-4 text-slate-700">1. Data Bibliografi (Judul)</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="md:col-span-2 relative">
                        <label class="block text-sm font-medium mb-1">Judul Buku *</label>
                        <input type="text" x-model="form.judul" @input.debounce.500ms="searchBiblio()" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black" required placeholder="Ketik judul buku...">
                        
                        <!-- Autocomplete Judul -->
                        <div x-show="biblioResults.length > 0" @click.away="biblioResults = []" class="absolute z-10 w-full bg-white border border-stroke mt-1 rounded shadow-lg max-h-60 overflow-y-auto">
                            <template x-for="b in biblioResults">
                                <div @click="selectBiblio(b)" class="p-3 border-b border-stroke hover:bg-slate-50 cursor-pointer">
                                    <div class="font-semibold text-black text-sm" x-text="b.judul"></div>
                                    <div class="text-xs text-slate-500" x-text="(b.pengarang || '-') + ' | ' + (b.penerbit || '-')"></div>
                                </div>
                            </template>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium mb-1">Pengarang</label>
                        <input type="text" x-model="form.pengarang" :disabled="form.biblio_id" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black" :class="form.biblio_id ? 'bg-slate-100' : ''">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Penerbit</label>
                        <input type="text" x-model="form.penerbit" :disabled="form.biblio_id" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black" :class="form.biblio_id ? 'bg-slate-100' : ''">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Tahun Terbit</label>
                        <input type="text" x-model="form.tahun_terbit" :disabled="form.biblio_id" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black" :class="form.biblio_id ? 'bg-slate-100' : ''">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">ISBN / ISSN</label>
                        <input type="text" x-model="form.isbn" :disabled="form.biblio_id" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black" :class="form.biblio_id ? 'bg-slate-100' : ''">
                    </div>
                    <div class="relative">
                        <label class="block text-sm font-medium mb-1 flex justify-between">
                            <span>Klasifikasi DDC</span>
                            <button type="button" @click="cariDdc()" class="text-xs text-primary font-semibold hover:underline"><i class="fa-solid fa-magnifying-glass"></i> Cari Kamus</button>
                        </label>
                        <input type="text" x-model="form.klasifikasi" :disabled="form.biblio_id" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black" :class="form.biblio_id ? 'bg-slate-100' : ''">
                        
                        <!-- Autocomplete DDC -->
                        <div x-show="ddcResults.length > 0" @click.away="ddcResults = []" class="absolute z-10 w-full bg-white border border-stroke mt-1 rounded shadow-lg max-h-48 overflow-y-auto">
                            <template x-for="d in ddcResults">
                                <div @click="selectDdc(d.kode)" class="p-2 border-b border-stroke hover:bg-slate-50 cursor-pointer flex gap-2">
                                    <span class="font-bold text-primary w-12" x-text="d.kode"></span>
                                    <span class="text-sm text-black" x-text="d.deskripsi"></span>
                                </div>
                            </template>
                            <div x-show="ddcResults.length === 0" class="p-3 text-sm text-slate-500 text-center">Tidak ada kecocokan di Kamus lokal.</div>
                        </div>
                    </div>
                    
                    <div x-show="form.biblio_id" class="md:col-span-2 mt-2 bg-blue-50 text-blue-700 p-3 rounded text-sm flex items-start gap-2">
                        <i class="fa-solid fa-circle-info mt-0.5"></i>
                        <div>
                            <strong>Judul Sudah Ada!</strong><br>
                            Anda menambahkan eksemplar/salinan baru untuk judul yang sudah ada di database. Kolom bibliografi otomatis dikunci.
                            <button type="button" @click="resetBiblio()" class="underline font-semibold ml-2">Batal & Buat Judul Baru</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SECTION 2: Eksemplar -->
            <div class="mb-6">
                <h3 class="text-md font-semibold border-b border-stroke pb-2 mb-4 text-slate-700">2. Data Salinan Fisik (Eksemplar)</h3>
                <div class="bg-slate-50 p-4 border border-stroke rounded grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label class="block text-sm font-medium mb-1">Jumlah Eksemplar *</label>
                        <input type="number" min="1" x-model="form.jumlah" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black" required>
                        <p class="text-xs text-slate-500 mt-1">Barcode akan di-generate berurutan.</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Lokasi Rak</label>
                        <select x-model="form.lokasi" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black">
                            <option value="IMAVI">IMAVI</option>
                            <option value="Taman Baca">Taman Baca</option>
                            <option value="Gudang">Gudang</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Asal Buku</label>
                        <select x-model="form.status_buku" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black">
                            <option value="BELI">BELI</option>
                            <option value="HADIAH">HADIAH</option>
                            <option value="HIBAH">HIBAH</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- HASIL BARCODE -->
            <div x-show="generatedBarcodes.length > 0" class="mb-6 p-4 border border-success bg-success/5 rounded">
                <h4 class="font-bold text-success mb-2"><i class="fa-solid fa-check-circle mr-1"></i> Berhasil Disimpan!</h4>
                <p class="text-sm mb-2">Sistem telah membuatkan barcode berikut untuk dicetak:</p>
                <div class="flex flex-wrap gap-2">
                    <template x-for="bc in generatedBarcodes">
                        <span class="bg-white border border-success text-black px-3 py-1 rounded font-mono font-bold shadow-sm" x-text="bc"></span>
                    </template>
                </div>
                <div class="mt-4">
                    <button type="button" @click="resetForm()" class="bg-primary text-white px-4 py-2 rounded text-sm hover:bg-opacity-90">Input Judul Berikutnya</button>
                </div>
            </div>

            <!-- BUTTONS -->
            <div class="flex justify-end gap-3 border-t border-stroke pt-4" x-show="generatedBarcodes.length === 0">
                <button type="button" @click="resetForm()" class="px-5 py-2 rounded font-medium text-slate-600 bg-slate-100 hover:bg-slate-200">Reset</button>
                <button type="submit" :disabled="isSubmitting" class="px-6 py-2 rounded font-bold text-white bg-primary hover:bg-opacity-90 shadow-sm disabled:opacity-50">
                    <span x-show="!isSubmitting">Simpan & Buat Barcode</span>
                    <span x-show="isSubmitting"><i class="fa-solid fa-spinner fa-spin"></i> Memproses...</span>
                </button>
            </div>
        </form>
    </div>
</div>

<script>
document.addEventListener('alpine:init', () => {
    Alpine.data('inputBuku', () => ({
        form: {
            biblio_id: null,
            judul: '',
            pengarang: '',
            penerbit: '',
            tahun_terbit: '',
            isbn: '',
            klasifikasi: '',
            jumlah: 1,
            lokasi: 'IMAVI',
            status_buku: 'BELI'
        },
        isSubmitting: false,
        biblioResults: [],
        ddcResults: [],
        generatedBarcodes: [],
        notif: { show: false, type: '', title: '', message: '' },
        
        async searchBiblio() {
            if (this.form.biblio_id) return; // don't search if already locked
            if (this.form.judul.length < 3) {
                this.biblioResults = [];
                return;
            }
            try {
                const res = await fetch('/api/bibliografi/search?q=' + encodeURIComponent(this.form.judul));
                this.biblioResults = await res.json();
            } catch (e) {
                console.error(e);
            }
        },
        
        selectBiblio(b) {
            this.form.biblio_id = b.id;
            this.form.judul = b.judul;
            this.form.pengarang = b.pengarang;
            this.form.penerbit = b.penerbit;
            this.form.tahun_terbit = b.tahun_terbit;
            this.form.isbn = b.isbn;
            this.form.klasifikasi = b.klasifikasi;
            this.biblioResults = [];
        },
        
        resetBiblio() {
            this.form.biblio_id = null;
            this.form.pengarang = '';
            this.form.penerbit = '';
            this.form.tahun_terbit = '';
            this.form.isbn = '';
            this.form.klasifikasi = '';
        },
        
        async cariDdc() {
            // search using title keywords
            const q = this.form.judul || this.form.klasifikasi;
            if (!q) {
                alert('Ketik judul atau kata kunci DDC terlebih dahulu.');
                return;
            }
            try {
                const res = await fetch('/api/ddc/search?q=' + encodeURIComponent(q));
                this.ddcResults = await res.json();
                if (this.ddcResults.length === 0) {
                    this.ddcResults = [{kode: '---', deskripsi: 'Kata kunci tidak ditemukan di kamus lokal.'}];
                }
            } catch (e) {
                console.error(e);
            }
        },
        
        selectDdc(kode) {
            if(kode !== '---') {
                this.form.klasifikasi = kode;
            }
            this.ddcResults = [];
        },
        
        async submitForm() {
            this.isSubmitting = true;
            this.notif.show = false;
            
            try {
                const res = await fetch('/api/buku/input_batch', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(this.form)
                });
                const result = await res.json();
                
                if (result.status === 'success') {
                    this.generatedBarcodes = result.barcodes;
                    this.notif = { show: true, type: 'success', title: 'Berhasil!', message: result.message };
                    // scroll to top
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                } else {
                    this.notif = { show: true, type: 'error', title: 'Gagal', message: result.message };
                }
            } catch (err) {
                this.notif = { show: true, type: 'error', title: 'Error', message: 'Koneksi ke server terputus.' };
            }
            this.isSubmitting = false;
        },
        
        resetForm() {
            this.form = {
                biblio_id: null, judul: '', pengarang: '', penerbit: '', tahun_terbit: '',
                isbn: '', klasifikasi: '', jumlah: 1, lokasi: 'IMAVI', status_buku: 'BELI'
            };
            this.generatedBarcodes = [];
            this.biblioResults = [];
            this.ddcResults = [];
            this.notif.show = false;
        }
    }));
});
</script>
{% endblock %}
'''

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(new_html)
print("input_buku.html rewritten.")
