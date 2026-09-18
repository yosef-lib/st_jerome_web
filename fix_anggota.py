import codecs
import re

with codecs.open('templates/anggota.html', 'r', 'utf-8') as f:
    code = f.read()

# Add Status to Table Header
code = code.replace('''                            <th class="py-4 px-4 font-medium text-black">Masa Berlaku</th>
                            <th class="py-4 px-4 font-medium text-black">Aksi</th>''', '''                            <th class="py-4 px-4 font-medium text-black">Masa Berlaku</th>
                            <th class="py-4 px-4 font-medium text-black">Status</th>
                            <th class="py-4 px-4 font-medium text-black">Aksi</th>''')

# Add Status to Table Row
code = code.replace('''                              <p class="text-black">{{ anggota['masa_berlaku'] }}</p>
                          </td>
                          <td class="py-4 px-4">
                              <button type="button" class="text-primary hover:text-blue-800 transition font-medium" onclick="openEditModal('{{ anggota['member_id'] }}', '{{ anggota['nama'] }}', '{{ anggota['tipe_anggota'] }}', '{{ anggota['masa_berlaku'] }}')">''', '''                              <p class="text-black">{{ anggota['masa_berlaku'] }}</p>
                          </td>
                          <td class="py-4 px-4">
                              {% if anggota.status == 'DIBLOKIR' %}
                                  <span class="inline-block rounded-full bg-danger px-3 py-1 text-sm font-medium text-white">DIBLOKIR</span>
                                  {% if anggota.suspended_until %}
                                  <span class="block text-xs mt-1 text-danger">s.d. {{ anggota.suspended_until }}</span>
                                  {% endif %}
                              {% else %}
                                  <span class="inline-block rounded-full bg-success px-3 py-1 text-sm font-medium text-white">AKTIF</span>
                              {% endif %}
                          </td>
                          <td class="py-4 px-4">
                              <button type="button" class="text-primary hover:text-blue-800 transition font-medium" onclick="openEditModal('{{ anggota['member_id'] }}', '{{ anggota['nama'] }}', '{{ anggota['tipe_anggota'] }}', '{{ anggota['masa_berlaku'] }}', '{{ anggota['status'] }}')">''')

# Update Edit Modal HTML
old_modal = '''          <div class="mb-4">
              <label class="mb-2 block text-sm font-medium text-black">Tipe Anggota</label>
              <input type="text" name="tipe_anggota" id="edit_tipe_anggota" required class="w-full rounded border border-stroke bg-transparent py-2.5 px-4 outline-none transition focus:border-primary active:border-primary">
          </div>
          <div class="mb-5">
              <label class="mb-1 block text-sm font-medium text-black">Masa Berlaku (Tahun-Bulan-Tanggal)</label>
              <input type="text" name="masa_berlaku" id="edit_masa_berlaku" required class="w-full rounded border border-stroke bg-transparent py-2.5 px-4 outline-none transition focus:border-primary active:border-primary">
              <span class="text-xs text-slate-500 mt-1 block">Contoh: 2029-12-31</span>
          </div>'''

new_modal = '''          <div class="mb-4">
              <label class="mb-2 block text-sm font-medium text-black">Tipe Anggota</label>
              <input type="text" list="tipe_options" name="tipe_anggota" id="edit_tipe_anggota" required class="w-full rounded border border-stroke bg-transparent py-2.5 px-4 outline-none transition focus:border-primary active:border-primary">
              <datalist id="tipe_options">
                  <option value="Frater Reguler">
                  <option value="Frater Skripsi/Tesis">
                  <option value="Dosen">
                  <option value="Mahasiswa">
                  <option value="Staf">
              </datalist>
          </div>
          <div class="mb-4">
              <label class="mb-2 block text-sm font-medium text-black">Status Keanggotaan</label>
              <select name="status" id="edit_status" class="w-full rounded border border-stroke bg-transparent py-2.5 px-4 outline-none transition focus:border-primary active:border-primary">
                  <option value="AKTIF">AKTIF</option>
                  <option value="DIBLOKIR">DIBLOKIR</option>
              </select>
          </div>
          <div class="mb-5">
              <label class="mb-1 block text-sm font-medium text-black">Masa Berlaku (Tahun-Bulan-Tanggal)</label>
              <input type="text" name="masa_berlaku" id="edit_masa_berlaku" required class="w-full rounded border border-stroke bg-transparent py-2.5 px-4 outline-none transition focus:border-primary active:border-primary">
              <span class="text-xs text-slate-500 mt-1 block">Contoh: 2029-12-31</span>
          </div>'''

code = code.replace(old_modal, new_modal)

# Update JS signature
code = code.replace("function openEditModal(id, nama, tipe, masa) {", "function openEditModal(id, nama, tipe, masa, status) {")
code = code.replace("document.getElementById('edit_masa_berlaku').value = masa;", "document.getElementById('edit_masa_berlaku').value = masa;\n    document.getElementById('edit_status').value = status || 'AKTIF';")

with codecs.open('templates/anggota.html', 'w', 'utf-8') as f:
    f.write(code)
print("Updated anggota.html")
