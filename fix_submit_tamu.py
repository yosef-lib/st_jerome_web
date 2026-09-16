import codecs
import re

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

pattern = r'async function submitTamu\(\) \{.*?\n        \}'

new_submit = '''async function submitTamu() {
            const err = document.getElementById('tamuError');
            err.classList.add('hidden');
            
            const nama = document.getElementById('tamuNama').value;
            const instansi = document.getElementById('tamuInstansi').value;
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
                });
                const data = await res.json();
                if(res.ok) {
                    showSuccess(data.display_name);
                } else {
                    err.innerText = data.message || "Gagal merekam data.";
                    err.classList.remove('hidden');
                }
            } catch(e) {
                err.innerText = "Terjadi kesalahan jaringan.";
                err.classList.remove('hidden');
            }
        }'''

html = re.sub(pattern, new_submit, html, flags=re.DOTALL)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)

print("Fixed submitTamu()")
