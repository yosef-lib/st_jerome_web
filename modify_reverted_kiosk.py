import codecs
import re

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Change "Anggota SLiMS" to "Anggota Perpustakaan"
html = html.replace('Anggota SLiMS', 'Anggota Perpustakaan')

# 2. Replace Member Content to remove camera
member_content_pattern = r'<!-- Konten Member -->(.*?)<!-- Konten Tamu -->'
new_member_content = '''<!-- Konten Member -->
            <div id="contentMember" class="block animate-fade-in">
                <div class="text-center mb-10">
                    <h3 class="text-2xl font-bold text-black mb-3">Scan Barcode Anda</h3>
                    <p class="text-slate-500">Gunakan scanner fisik di meja untuk memindai kartu anggota Anda.</p>
                </div>
                
                <div class="relative mt-8">
                    <i class="fa-solid fa-barcode absolute left-4 top-1/2 -translate-y-1/2 text-2xl text-slate-400"></i>
                    <input type="text" id="memberIdInput" placeholder="Arahkan kursor kesini dan Scan Barcode..." onkeypress="if(event.key === 'Enter') submitMember()" class="w-full rounded-xl border-2 border-stroke bg-gray-50 py-5 pl-14 pr-24 outline-none transition focus:border-primary focus:bg-white text-lg font-semibold">
                    <button onclick="submitMember()" class="absolute right-2 top-2 bottom-2 rounded-lg bg-primary px-6 font-bold text-white hover:bg-opacity-90 transition">Kirim</button>
                </div>
                <p id="memberError" class="text-danger text-sm mt-3 hidden text-center font-bold"></p>
                
                <div class="mt-12 text-center">
                    <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-primary/10 mb-4">
                        <i class="fa-solid fa-qrcode text-4xl text-primary"></i>
                    </div>
                    <p class="text-sm font-medium text-slate-500">Sistem otomatis mendeteksi barcode Anda.</p>
                </div>
            </div>

            <!-- Konten Tamu -->'''
html = re.sub(member_content_pattern, new_member_content, html, flags=re.DOTALL)

# 3. Modify Tamu Form
tamu_form_pattern = r'<form id="formTamu".*?</form>'
new_tamu_form = '''<form id="formTamu" onsubmit="event.preventDefault(); submitTamu();">
                    
                    <div class="mb-5 relative">
                        <label class="mb-2 block text-sm font-bold text-black">Nama Lengkap</label>
                        <input type="text" id="tamuNama" required autocomplete="off" placeholder="Ketik nama Anda..." class="w-full rounded-lg border-[1.5px] border-stroke bg-transparent py-3 px-5 outline-none transition focus:border-primary active:border-primary">
                        
                        <!-- Autocomplete Suggestions -->
                        <div id="autocompleteList" class="absolute z-40 w-full bg-white border border-stroke rounded-lg mt-1 shadow-lg hidden max-h-48 overflow-y-auto no-scrollbar">
                            <!-- Items injected via JS -->
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
                        <div>
                            <label class="mb-2 block text-sm font-bold text-black">Asal Instansi</label>
                            <select id="tamuInstansi" required class="w-full rounded-lg border-[1.5px] border-stroke bg-transparent py-3 px-5 outline-none transition focus:border-primary active:border-primary cursor-pointer appearance-none">
                                <option value="" disabled selected>-- Pilih Instansi --</option>
                                <option value="IMAVI">IMAVI</option>
                                <option value="UKWMS">UKWMS</option>
                                <option value="Lain-lain">Lain-lain</option>
                            </select>
                        </div>

                        <div>
                            <label class="mb-2 block text-sm font-bold text-black">Peran / Jabatan</label>
                            <select id="tamuPeran" required onchange="checkPeran()" class="w-full rounded-lg border-[1.5px] border-stroke bg-transparent py-3 px-5 outline-none transition focus:border-primary active:border-primary cursor-pointer appearance-none">
                                <option value="" disabled selected>-- Pilih Peran --</option>
                                <option value="Dosen">Dosen</option>
                                <option value="Karyawan">Karyawan</option>
                                <option value="Mahasiswa">Mahasiswa</option>
                                <option value="Romo">Romo</option>
                                <option value="Umum">Umum</option>
                            </select>
                        </div>
                    </div>

                    <div id="fakultasContainer" class="mb-8 hidden animate-fade-in">
                        <label class="mb-2 block text-sm font-bold text-black">Fakultas (Wajib bagi Mahasiswa)</label>
                        <input type="text" id="tamuFakultas" placeholder="Contoh: Fakultas Filsafat" class="w-full rounded-lg border-[1.5px] border-stroke bg-transparent py-3 px-5 outline-none transition focus:border-primary active:border-primary">
                    </div>

                    <button type="submit" class="w-full rounded-lg bg-primary py-4 px-6 text-center font-bold text-white hover:bg-opacity-90 transition text-lg shadow-md mt-4">
                        <i class="fa-solid fa-check-circle mr-2"></i> Rekam Kunjungan
                    </button>
                    <p id="tamuError" class="text-danger text-sm mt-3 hidden text-center font-bold"></p>
                </form>'''
html = re.sub(tamu_form_pattern, new_tamu_form, html, flags=re.DOTALL)

# 4. Modify submitTamu() javascript
old_submit_js = '''const instansi = document.getElementById('tamuInstansi').value;
            const tujuan = document.getElementById('tamuTujuan').value;
            
            if(!instansi) {
                err.innerText = "Silakan pilih Asal Instansi.";
                err.classList.remove('hidden');
                return;
            }
            
            try {
                const res = await fetch('/api/kunjungan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        tipe_pengunjung: 'Non-Member',
                        identitas: nama,
                        asal_instansi: instansi,
                        tujuan_kunjungan: tujuan
                    })
                });'''

new_submit_js = '''const instansi = document.getElementById('tamuInstansi').value;
            const peran = document.getElementById('tamuPeran').value;
            const fakultas = document.getElementById('tamuFakultas').value;
            
            if(!instansi || !peran) {
                err.innerText = "Silakan lengkapi form.";
                err.classList.remove('hidden');
                return;
            }
            
            if(peran === 'Mahasiswa' && !fakultas.trim()) {
                err.innerText = "Mahasiswa wajib mengisi kolom Fakultas.";
                err.classList.remove('hidden');
                return;
            }
            
            try {
                const res = await fetch('/api/kunjungan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        tipe_pengunjung: 'Non-Member',
                        identitas: nama,
                        asal_instansi: instansi,
                        peran_jabatan: peran,
                        fakultas: fakultas
                    })
                });'''
html = html.replace(old_submit_js, new_submit_js)

# 5. Add checkPeran() js function
js_append = '''function checkPeran() {
            const peran = document.getElementById('tamuPeran').value;
            const facContainer = document.getElementById('fakultasContainer');
            const facInput = document.getElementById('tamuFakultas');
            if(peran === 'Mahasiswa') {
                facContainer.classList.remove('hidden');
                facInput.setAttribute('required', 'true');
            } else {
                facContainer.classList.add('hidden');
                facInput.removeAttribute('required');
                facInput.value = '';
            }
        }
        
        // Remove camera logic block completely
        '''
# Find "// Kamera Logic" and replace to EOF
html = re.sub(r'// Kamera Logic.*?</script>', js_append + '</script>', html, flags=re.DOTALL)

# Add html5-qrcode script removal
html = html.replace('<script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>', '')

# Re-add the Back Button
back_btn = '''<body class="kiosk-bg min-h-screen flex items-center justify-center p-4 relative">
    
    <!-- Tombol Kembali -->
    <a href="/" class="absolute top-6 left-6 bg-white text-black font-semibold py-2 px-4 rounded shadow hover:bg-gray-50 transition flex items-center gap-2 text-sm z-10 border border-stroke">
        <i class="fa-solid fa-arrow-left"></i> Kembali
    </a>'''

html = html.replace('<body class="kiosk-bg min-h-screen flex items-center justify-center p-4">', back_btn)

# Reset form on tab switch and focus
focus_logic = '''document.getElementById('formTamu').reset();
                checkPeran();'''
html = html.replace("document.getElementById('formTamu').reset();", focus_logic)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)

print("Modified reverted kiosk.html")
