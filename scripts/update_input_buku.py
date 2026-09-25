import codecs, re

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    html = f.read()

# Add cover image input before the submit button
old_submit = '''                      <div class="md:col-span-2 pt-4">
                          <button type="submit" class="w-full rounded bg-primary py-3 font-medium text-white hover:bg-opacity-90 transition">
                              <i class="fa-solid fa-plus mr-2"></i> Tambahkan ke Antrean Cetak
                          </button>
                      </div>'''

new_submit = '''                      <div class="md:col-span-2">
                          <label class="mb-2 block text-sm font-medium text-black">Gambar Sampul <span class="text-xs text-slate-400 font-normal">(Opsional - Untuk OPAC)</span></label>
                          <input type="file" name="gambar_sampul" id="gambar_sampul" accept="image/*" class="w-full rounded border border-stroke bg-transparent py-2.5 px-4 outline-none focus:border-primary focus-visible:shadow-none" />
                      </div>
                      <div class="md:col-span-2 pt-4">
                          <button type="submit" class="w-full rounded bg-primary py-3 font-medium text-white hover:bg-opacity-90 transition">
                              <i class="fa-solid fa-plus mr-2"></i> Tambahkan ke Antrean Cetak
                          </button>
                      </div>'''
html = html.replace(old_submit, new_submit)

# Update Javascript form submission
old_js = '''      // Submit form tambah buku
      document.getElementById('formAntrean').addEventListener('submit', function(e) {
          e.preventDefault();
          const btn = this.querySelector('button[type="submit"]');
          const originalText = btn.innerHTML;
          btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Menyimpan...';
          btn.disabled = true;

          const data = {
              no_induk: this.no_induk.value,
              judul: this.judul.value,
              pengarang: this.pengarang.value,
              subjek: this.subjek.value,
              klasifikasi: this.klasifikasi.value,
              cutter: this.cutter.value,
              huruf_judul: this.huruf_judul.value,
              gmd: this.gmd.value,
              edisi: this.edisi.value,
              isbn: this.isbn.value,
              penerbit: this.penerbit.value,
              tahun_terbit: this.tahun_terbit.value,
              tempat_terbit: this.tempat_terbit.value,
              deskripsi_fisik: this.deskripsi_fisik.value,
              judul_seri: this.judul_seri.value,
              bahasa: this.bahasa.value,
              copy_ke: this.copy_ke.value,
              catatan: this.catatan.value,
              tgl_terima: this.tgl_terima.value,
              status_buku: this.status_buku.value,
              lokasi: this.lokasi.value
          };

          fetch('/api/antrean', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(data)
          })'''

new_js = '''      // Autofill when typing no_induk
      document.getElementById('no_induk').addEventListener('blur', function(e) {
          const noInduk = this.value.trim();
          if(!noInduk) return;
          
          fetch('/api/buku/' + encodeURIComponent(noInduk))
          .then(r => r.json())
          .then(res => {
              if(res.status === 'success') {
                  const d = res.data;
                  // Autofill form fields
                  const form = document.getElementById('formAntrean');
                  if(d.judul) form.judul.value = d.judul;
                  if(d.pengarang) form.pengarang.value = d.pengarang;
                  if(d.subjek) form.subjek.value = d.subjek;
                  if(d.klasifikasi) form.klasifikasi.value = d.klasifikasi;
                  if(d.cutter) form.cutter.value = d.cutter;
                  if(d.huruf_judul) form.huruf_judul.value = d.huruf_judul;
                  if(d.gmd) form.gmd.value = d.gmd;
                  if(d.edisi) form.edisi.value = d.edisi;
                  if(d.isbn) form.isbn.value = d.isbn;
                  if(d.penerbit) form.penerbit.value = d.penerbit;
                  if(d.tahun_terbit) form.tahun_terbit.value = d.tahun_terbit;
                  if(d.tempat_terbit) form.tempat_terbit.value = d.tempat_terbit;
                  if(d.deskripsi_fisik) form.deskripsi_fisik.value = d.deskripsi_fisik;
                  if(d.judul_seri) form.judul_seri.value = d.judul_seri;
                  if(d.bahasa) form.bahasa.value = d.bahasa;
                  if(d.copy_ke) form.copy_ke.value = d.copy_ke;
                  if(d.catatan) form.catatan.value = d.catatan;
                  if(d.tgl_terima) form.tgl_terima.value = d.tgl_terima;
                  if(d.status_buku) form.status_buku.value = d.status_buku;
                  if(d.lokasi) form.lokasi.value = d.lokasi;
                  
                  // Highlight visually
                  form.judul.style.backgroundColor = '#e0f2fe';
                  setTimeout(() => form.judul.style.backgroundColor = '', 1000);
              }
          });
      });

      // Submit form tambah buku
      document.getElementById('formAntrean').addEventListener('submit', function(e) {
          e.preventDefault();
          const btn = this.querySelector('button[type="submit"]');
          const originalText = btn.innerHTML;
          btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Menyimpan...';
          btn.disabled = true;

          const formData = new FormData(this);

          fetch('/api/antrean', {
              method: 'POST',
              body: formData
          })'''

html = html.replace(old_js, new_js)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(html)
print("input_buku updated")
