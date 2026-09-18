import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Add Button next to Klasifikasi
old_klas = '''                <div class="w-full xl:w-1/3">
                    <label class="mb-2.5 block text-black font-medium text-sm">Klasifikasi (DDC)</label>
                    <input type="text" name="klasifikasi" id="klasifikasi" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2 px-4 outline-none transition focus:border-primary active:border-primary text-sm">
                </div>'''

# wait, does it have id="klasifikasi"? 
# In previous script: <input type="text" name="klasifikasi" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2 px-4 outline-none transition focus:border-primary active:border-primary text-sm">

old_klas_exact = '''                <div class="w-full xl:w-1/3">
                    <label class="mb-2.5 block text-black font-medium text-sm">Klasifikasi (DDC)</label>
                    <input type="text" name="klasifikasi" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2 px-4 outline-none transition focus:border-primary active:border-primary text-sm">
                </div>'''

new_klas_exact = '''                <div class="w-full xl:w-1/3">
                    <label class="mb-2.5 block text-black font-medium text-sm flex justify-between">
                        <span>Klasifikasi (DDC)</span>
                        <button type="button" onclick="document.getElementById('ddcModal').showModal()" class="text-primary hover:underline"><i class="fa-solid fa-search"></i> Kamus DDC</button>
                    </label>
                    <input type="text" name="klasifikasi" id="input_klasifikasi" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2 px-4 outline-none transition focus:border-primary active:border-primary text-sm">
                </div>'''

html = html.replace(old_klas_exact, new_klas_exact)

# 2. Add Modal at the bottom before {% endblock %}
modal_html = '''
<!-- Modal Kamus DDC -->
<dialog id="ddcModal" class="rounded-sm border border-stroke bg-white p-6 shadow-default w-full max-w-2xl fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[9999]">
    <div class="flex justify-between items-center mb-5">
        <h3 class="text-xl font-semibold text-black"><i class="fa-solid fa-book-bookmark text-primary mr-2"></i> Kamus DDC & Referensi Cepat</h3>
        <button type="button" onclick="document.getElementById('ddcModal').close()" class="text-slate-400 hover:text-slate-700 text-2xl">&times;</button>
    </div>
    
    <div class="mb-4">
        <input type="text" id="searchDDC" placeholder="Cari topik (misal: Liturgi, Moral, Komputer)..." class="w-full rounded border-[1.5px] border-stroke bg-slate-50 py-3 px-5 outline-none transition focus:border-primary">
    </div>
    
    <div class="max-h-96 overflow-y-auto border border-stroke rounded-sm">
        <ul id="ddcList" class="flex flex-col">
            <!-- Diisi oleh JS -->
        </ul>
    </div>
</dialog>

<script>
    const ddcData = [
        { code: "000", desc: "Komputer, Informasi, & Karya Umum" },
        { code: "100", desc: "Filsafat & Psikologi" },
        { code: "150", desc: "Psikologi" },
        { code: "180", desc: "Filsafat Kuno, Abad Pertengahan, Timur" },
        { code: "190", desc: "Filsafat Barat Modern" },
        
        { code: "200", desc: "Agama" },
        { code: "210", desc: "Filsafat & Teori Agama" },
        { code: "220", desc: "Alkitab (Bibel)" },
        { code: "221", desc: "Perjanjian Lama (PL)" },
        { code: "225", desc: "Perjanjian Baru (PB)" },
        { code: "230", desc: "Kekristenan & Teologi Kristen" },
        { code: "231", desc: "Allah (Tritunggal, Bapa, Roh Kudus)" },
        { code: "232", desc: "Yesus Kristus (Kristologi)" },
        { code: "233", desc: "Manusia (Antropologi Teologis)" },
        { code: "234", desc: "Keselamatan (Soteriologi) & Rahmat" },
        { code: "236", desc: "Eskatologi (Akhir Zaman)" },
        { code: "240", desc: "Teologi Moral Kristiani & Spiritualitas" },
        { code: "241", desc: "Etika Kristen (Moral)" },
        { code: "248", desc: "Pengalaman & Praktik Kristen (Spiritualitas)" },
        { code: "250", desc: "Gereja Lokal & Praktik Pastoral" },
        { code: "253", desc: "Teologi Pastoral (Penggembalaan)" },
        { code: "260", desc: "Teologi Sosial Kristen & Eklesiologi" },
        { code: "261", desc: "Teologi Sosial (Gereja & Masyarakat)" },
        { code: "262", desc: "Eklesiologi (Struktur Gereja, Paus, Uskup)" },
        { code: "264", desc: "Liturgi & Ibadah Umum" },
        { code: "265", desc: "Sakramen-Sakramen" },
        { code: "266", desc: "Misi & Penginjilan (Misiologi)" },
        { code: "270", desc: "Sejarah Gereja & Kekristenan" },
        { code: "280", desc: "Denominasi & Sekte (Gereja Katolik, Ortodoks, dll)" },
        { code: "282", desc: "Gereja Katolik Roma" },
        { code: "290", desc: "Agama Lain & Perbandingan Agama" },
        { code: "297", desc: "Islam" },

        { code: "300", desc: "Ilmu Sosial, Sosiologi, & Antropologi" },
        { code: "320", desc: "Ilmu Politik" },
        { code: "330", desc: "Ekonomi" },
        { code: "340", desc: "Hukum" },
        { code: "348", desc: "Hukum Gereja (Hukum Kanonik)" },
        { code: "370", desc: "Pendidikan" },
        
        { code: "400", desc: "Bahasa" },
        { code: "470", desc: "Bahasa Latin" },
        { code: "480", desc: "Bahasa Yunani Kuno & Klasik" },
        { code: "492.4", desc: "Bahasa Ibrani" },
        
        { code: "500", desc: "Sains & Ilmu Pengetahuan Alam" },
        { code: "600", desc: "Teknologi & Ilmu Terapan" },
        { code: "700", desc: "Kesenian & Rekreasi" },
        { code: "726", desc: "Arsitektur Gereja / Tempat Ibadah" },
        { code: "782.2", desc: "Musik Liturgi & Musik Gereja" },
        { code: "800", desc: "Sastra & Literatur" },
        { code: "900", desc: "Sejarah & Geografi" }
    ];

    const ddcList = document.getElementById('ddcList');
    const searchDDC = document.getElementById('searchDDC');

    function renderDDC(filterText = "") {
        ddcList.innerHTML = '';
        const filtered = ddcData.filter(item => 
            item.code.includes(filterText) || item.desc.toLowerCase().includes(filterText.toLowerCase())
        );
        
        if(filtered.length === 0) {
            ddcList.innerHTML = '<li class="p-4 text-center text-slate-500">Tidak ada kategori yang cocok.</li>';
            return;
        }

        filtered.forEach(item => {
            const li = document.createElement('li');
            li.className = "flex justify-between items-center p-3 border-b border-stroke hover:bg-slate-50 cursor-pointer transition";
            li.onclick = () => {
                document.getElementById('input_klasifikasi').value = item.code;
                document.getElementById('ddcModal').close();
            };
            li.innerHTML = 
                <div>
                    <span class="font-bold text-primary inline-block w-16"></span>
                    <span class="text-black"></span>
                </div>
                <button type="button" class="text-xs bg-slate-200 hover:bg-primary hover:text-white px-3 py-1 rounded transition">Pilih</button>
            ;
            ddcList.appendChild(li);
        });
    }

    searchDDC.addEventListener('input', (e) => renderDDC(e.target.value));
    
    // Render initial list
    renderDDC();
</script>
'''

html = html.replace('{% endblock %}', modal_html + '\n{% endblock %}')

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(html)

print("Added Kamus DDC")
