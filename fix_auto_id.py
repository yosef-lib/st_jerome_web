import codecs
import re

# 1. UPDATE APP.PY
with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

new_eksemplar_logic = '''        # Auto-Generate Eksemplar ID (Format: 0001/26)
        import datetime
        current_year = datetime.datetime.now().strftime('%y')
        lokasi = request.form.get('lokasi', 'IMAVI')
        is_ref = 1 if request.form.get('is_reference_only') else 0
        total = int(request.form.get('total_item', 1))
        eksemplar_count = 0
        
        # Cari urutan terakhir di tahun ini
        cursor.execute("SELECT no_induk FROM eksemplar WHERE no_induk LIKE ?", (f'%/{current_year}',))
        existing_ids = cursor.fetchall()
        
        highest_seq = 0
        for eid in existing_ids:
            try:
                seq = int(eid[0].split('/')[0])
                if seq > highest_seq:
                    highest_seq = seq
            except:
                pass
                
        for i in range(total):
            highest_seq += 1
            barcode = f"{str(highest_seq).zfill(4)}/{current_year}"
            
            cursor.execute("""
                INSERT INTO eksemplar (no_induk, biblio_id, lokasi, is_reference_only, copy_ke)
                VALUES (?, ?, ?, ?, ?)
            """, (barcode, biblio_id, lokasi, is_ref, i+1))
        
        eksemplar_count = total
        conn.commit()'''

# Find and replace the eksemplar logic in api_bibliografi
pattern = re.compile(r'# Insert Eksemplar[\s\S]*?conn\.commit\(\)', re.DOTALL)
app_code = pattern.sub(new_eksemplar_logic, app_code)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)


# 2. UPDATE HTML
with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    html_code = f.read()

old_html_gen = '''            <!-- GENERATOR EKSEMPLAR -->
            <div class="p-5 mb-6 rounded bg-slate-50 border border-stroke">
                <h4 class="font-semibold text-black mb-4"><i class="fa-solid fa-barcode text-primary mr-2"></i> Pembuat Nomor Eksemplar (Barcode)</h4>
                
                <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
                    <div class="w-full xl:w-1/3">
                        <label class="mb-2.5 block text-black font-medium text-sm">Pola Eksemplar</label>
                        <select name="pola_eksemplar" id="pola_eksemplar" class="w-full rounded border-[1.5px] border-stroke bg-white py-3 px-5 outline-none transition focus:border-primary active:border-primary">
                            <option value="">-- Pilih Pola / Manual --</option>
                            <option value="B00000">B00000 (Contoh: B00001)</option>
                            <option value="P00000">P00000 (Contoh: P00001)</option>
                        </select>
                    </div>
                    
                    <div class="w-full xl:w-1/3" id="manual_barcode_div">
                        <label class="mb-2.5 block text-black font-medium text-sm">Barcode / No Induk Manual</label>
                        <input type="text" name="manual_barcode" id="manual_barcode" placeholder="Ketik barcode jika tidak pakai pola" class="w-full rounded border-[1.5px] border-stroke bg-white py-3 px-5 outline-none transition focus:border-primary active:border-primary">
                    </div>
                    
                    <div class="w-full xl:w-1/3" id="total_item_div" style="display:none;">
                        <label class="mb-2.5 block text-black font-medium text-sm">Total Item (Jumlah Copy)</label>
                        <input type="number" name="total_item" id="total_item" min="1" value="1" class="w-full rounded border-[1.5px] border-stroke bg-white py-3 px-5 outline-none transition focus:border-primary active:border-primary">
                    </div>
                </div>'''

new_html_gen = '''            <!-- GENERATOR EKSEMPLAR -->
            <div class="p-5 mb-6 rounded bg-slate-50 border border-stroke">
                <h4 class="font-semibold text-black mb-4"><i class="fa-solid fa-barcode text-primary mr-2"></i> Nomor Induk (Barcode) Otomatis</h4>
                
                <div class="mb-4.5 flex flex-col gap-6 xl:flex-row">
                    <div class="w-full xl:w-1/2">
                        <div class="rounded-md border border-primary bg-blue-50 px-4 py-3 mb-2">
                            <p class="text-sm text-primary font-medium">Sistem akan secara otomatis memberikan Nomor Induk berurutan dengan format <strong>XXXX/26</strong> (Misal: 0001/26) saat Anda menyimpan data.</p>
                        </div>
                    </div>
                    
                    <div class="w-full xl:w-1/2">
                        <label class="mb-2.5 block text-black font-medium text-sm">Jumlah Copy (Item)</label>
                        <input type="number" name="total_item" id="total_item" min="1" value="1" required class="w-full rounded border-[1.5px] border-stroke bg-white py-3 px-5 outline-none transition focus:border-primary active:border-primary">
                        <p class="text-xs text-slate-500 mt-2">Jika Anda memasukkan 3, sistem akan meng-generate 3 nomor seri sekaligus.</p>
                    </div>
                </div>'''

html_code = html_code.replace(old_html_gen, new_html_gen)

# Remove the JS that handles the old dropdown
script_to_remove = '''    const polaSelect = document.getElementById('pola_eksemplar');
    const manualDiv = document.getElementById('manual_barcode_div');
    const manualInput = document.getElementById('manual_barcode');
    const totalDiv = document.getElementById('total_item_div');
    
    polaSelect.addEventListener('change', function() {
        if (this.value === "") {
            manualDiv.style.display = 'block';
            totalDiv.style.display = 'none';
            manualInput.required = true;
        } else {
            manualDiv.style.display = 'none';
            totalDiv.style.display = 'block';
            manualInput.required = false;
        }
    });'''

html_code = html_code.replace(script_to_remove, "")
html_code = html_code.replace("polaSelect.dispatchEvent(new Event('change'));", "")

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(html_code)

print("Updates completed.")
