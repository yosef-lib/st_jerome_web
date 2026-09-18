import codecs
import re

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    html = f.read()

# Hapus script lama
pattern_script = re.compile(r'<script>\s*const ddcData = \[.*?</script>', re.DOTALL)
html = pattern_script.sub('', html)

# Script baru yang lebih canggih dengan Auto-Detect
new_script = '''
<script>
document.addEventListener("DOMContentLoaded", function() {
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

    const ddcKeywords = [
        { keywords: ["komputer", "informasi", "sistem", "data", "software", "program", "internet"], code: "000" },
        { keywords: ["filsafat", "logika", "metafisika", "epistemologi", "filosofi"], code: "100" },
        { keywords: ["psikologi", "mental", "jiwa", "depresi", "karakter", "kepribadian"], code: "150" },
        { keywords: ["agama", "iman", "kepercayaan", "teologi", "Tuhan"], code: "200" },
        { keywords: ["alkitab", "bibel", "injil", "perjanjian", "mazmur", "taurat"], code: "220" },
        { keywords: ["kristen", "kekristenan", "protestan"], code: "230" },
        { keywords: ["allah", "tritunggal", "bapa", "roh kudus"], code: "231" },
        { keywords: ["yesus", "kristus", "kristologi", "salib"], code: "232" },
        { keywords: ["keselamatan", "soteriologi", "dosa", "rahmat", "penebusan"], code: "234" },
        { keywords: ["eskatologi", "akhir zaman", "kiamat"], code: "236" },
        { keywords: ["moral", "etika", "baik buruk", "hati nurani"], code: "240" },
        { keywords: ["pastoral", "gembala", "umat", "paroki"], code: "253" },
        { keywords: ["liturgi", "ibadah", "misa", "ekaristi", "nyanyian gereja"], code: "264" },
        { keywords: ["sakramen", "baptis", "krisma", "imamat"], code: "265" },
        { keywords: ["misi", "penginjilan", "misionaris"], code: "266" },
        { keywords: ["sejarah gereja", "bapa gereja", "patristik", "konsili"], code: "270" },
        { keywords: ["katolik", "roma", "paus", "uskup", "vatikan"], code: "282" },
        { keywords: ["islam", "muslim", "quran", "muhammad"], code: "297" },
        { keywords: ["sosial", "sosiologi", "masyarakat", "komunitas"], code: "300" },
        { keywords: ["politik", "negara", "pemerintah", "demokrasi"], code: "320" },
        { keywords: ["ekonomi", "bisnis", "uang", "manajemen", "keuangan"], code: "330" },
        { keywords: ["hukum", "undang", "pidana", "perdata"], code: "340" },
        { keywords: ["kanonik", "hukum gereja", "codex iuris canonici"], code: "348" },
        { keywords: ["pendidikan", "sekolah", "guru", "belajar", "pedagogi"], code: "370" },
        { keywords: ["bahasa", "linguistik", "tata bahasa", "kamus"], code: "400" },
        { keywords: ["latin"], code: "470" },
        { keywords: ["yunani"], code: "480" },
        { keywords: ["ibrani"], code: "492.4" },
        { keywords: ["sains", "ilmu pengetahuan", "biologi", "fisika", "kimia", "alam"], code: "500" },
        { keywords: ["matematika", "kalkulus", "aljabar"], code: "510" },
        { keywords: ["teknologi", "teknik", "mesin", "industri"], code: "600" },
        { keywords: ["kedokteran", "medis", "kesehatan", "penyakit"], code: "610" },
        { keywords: ["seni", "kesenian", "lukisan", "estetika"], code: "700" },
        { keywords: ["arsitektur", "bangunan", "candi", "gereja (bangunan)"], code: "720" },
        { keywords: ["musik", "lagu", "nyanyian", "not balok"], code: "780" },
        { keywords: ["sastra", "novel", "puisi", "cerpen", "dongeng", "fiksi"], code: "800" },
        { keywords: ["sejarah", "historis", "perang", "masalalu"], code: "900" },
        { keywords: ["geografi", "peta", "bumi", "wilayah"], code: "910" },
        { keywords: ["biografi", "riwayat", "tokoh", "otobiografi", "memoar"], code: "920" }
    ];

    const ddcList = document.getElementById('ddcList');
    const searchDDC = document.getElementById('searchDDC');
    const inputKlasifikasi = document.getElementById('input_klasifikasi');
    const inputJudul = document.querySelector('input[name="judul"]');
    
    // --- FITUR 1: RENDER KAMUS DDC ---
    function renderDDC(filterText = "") {
        if(!ddcList) return;
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
                inputKlasifikasi.value = item.code;
                document.getElementById('ddcModal').close();
                // Add a small success effect
                inputKlasifikasi.classList.add('bg-success', 'bg-opacity-20');
                setTimeout(() => inputKlasifikasi.classList.remove('bg-success', 'bg-opacity-20'), 1000);
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

    if(searchDDC) {
        searchDDC.addEventListener('input', (e) => renderDDC(e.target.value));
        renderDDC();
    }
    
    // --- FITUR 2: AUTO-DETECT DDC DARI JUDUL BUKU ---
    if(inputJudul) {
        // Buat elemen label rekomendasi di bawah input klasifikasi
        const recLabel = document.createElement('div');
        recLabel.className = 'mt-2 text-xs text-primary font-medium hidden';
        recLabel.innerHTML = '<i class="fa-solid fa-sparkles"></i> Rekomendasi AI: <span id="recDDCValue" class="font-bold cursor-pointer hover:underline"></span> (<span id="recDDCDesc"></span>)';
        inputKlasifikasi.parentNode.appendChild(recLabel);

        const recDDCValue = document.getElementById('recDDCValue');
        const recDDCDesc = document.getElementById('recDDCDesc');
        
        // Kalau diklik rekomendasinya, langsung masuk
        recDDCValue.addEventListener('click', function() {
            inputKlasifikasi.value = this.innerText;
            inputKlasifikasi.classList.add('bg-success', 'bg-opacity-20');
            setTimeout(() => inputKlasifikasi.classList.remove('bg-success', 'bg-opacity-20'), 1000);
        });

        inputJudul.addEventListener('input', function(e) {
            const judul = e.target.value.toLowerCase();
            let matchedCode = null;
            let matchedDesc = null;
            
            if (judul.trim().length > 3) {
                for (let category of ddcKeywords) {
                    for (let keyword of category.keywords) {
                        if (judul.includes(keyword)) {
                            matchedCode = category.code;
                            break;
                        }
                    }
                    if (matchedCode) break; // Ambil kecocokan pertama
                }
            }
            
            if (matchedCode) {
                // Cari deskripsi
                const catInfo = ddcData.find(d => d.code === matchedCode);
                matchedDesc = catInfo ? catInfo.desc : "";
                
                recDDCValue.innerText = matchedCode;
                recDDCDesc.innerText = matchedDesc;
                recLabel.classList.remove('hidden');
                
                // Jika klasifikasi masih kosong, isikan secara otomatis
                if(inputKlasifikasi.value.trim() === '') {
                    inputKlasifikasi.value = matchedCode;
                    inputKlasifikasi.classList.add('bg-success', 'bg-opacity-10');
                    setTimeout(() => inputKlasifikasi.classList.remove('bg-success', 'bg-opacity-10'), 1000);
                }
            } else {
                recLabel.classList.add('hidden');
            }
        });
    }
});
</script>
'''

html = html.replace('{% endblock %}', new_script + '\n{% endblock %}')

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(html)

print("Fixed DDC list and added Smart Auto-Detect feature.")
