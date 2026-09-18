import codecs

with codecs.open('templates/sirkulasi.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Remove Detail Keanggotaan button
detail_btn = '''<button class="bg-slate-500 hover:bg-slate-600 text-white px-4 py-1.5 rounded shadow flex items-center gap-2 transition text-sm font-medium">
                        <i class="fa-regular fa-user"></i> Detail Keanggotaan
                    </button>'''
html = html.replace(detail_btn, "")

# 2. Update Keyboard Shortcuts for F4 and F9
old_keys = '''@keydown.f2.window.prevent="activeTab = 'peminjaman'" @keydown.f3.window.prevent="activeTab = 'saat_ini'" @keydown.f10.window.prevent="activeTab = 'sejarah'"'''
new_keys = '''@keydown.f2.window.prevent="activeTab = 'peminjaman'" @keydown.f3.window.prevent="activeTab = 'saat_ini'" @keydown.f4.window.prevent="activeTab = 'reservasi'" @keydown.f9.window.prevent="activeTab = 'denda'" @keydown.f10.window.prevent="activeTab = 'sejarah'"'''
html = html.replace(old_keys, new_keys)

# 3. Enable the Tab Links for Reservasi and Denda
old_tabs_res = '''<a href="#" class="px-5 py-2 text-slate-400 cursor-not-allowed">Reservasi (F4)</a>'''
new_tabs_res = '''<a href="#" @click.prevent="activeTab = 'reservasi'" :class="activeTab === 'reservasi' ? 'text-primary border-b-2 border-primary bg-slate-50' : 'text-slate-500 hover:text-black'" class="px-5 py-2 transition">Reservasi (F4)</a>'''
html = html.replace(old_tabs_res, new_tabs_res)

old_tabs_den = '''<a href="#" class="px-5 py-2 text-slate-400 cursor-not-allowed">Denda (F9)</a>'''
new_tabs_den = '''<a href="#" @click.prevent="activeTab = 'denda'" :class="activeTab === 'denda' ? 'text-primary border-b-2 border-primary bg-slate-50' : 'text-slate-500 hover:text-black'" class="px-5 py-2 transition">Denda (F9)</a>'''
html = html.replace(old_tabs_den, new_tabs_den)

# 4. Add Tab Contents for Reservasi and Denda
new_contents = '''
                <!-- Tab Content: Reservasi -->
                <div x-show="activeTab === 'reservasi'" style="display: none;">
                    <div class="p-8 text-center border border-dashed border-stroke bg-slate-50 rounded mt-1">
                        <i class="fa-solid fa-clock-rotate-left text-4xl text-slate-300 mb-3"></i>
                        <h3 class="text-lg font-semibold text-slate-700">Fitur Reservasi Belum Aktif</h3>
                        <p class="text-sm text-slate-500 mt-1">Fitur untuk memesan/menahan (hold) buku sedang dalam tahap pengembangan.</p>
                    </div>
                </div>

                <!-- Tab Content: Denda -->
                <div x-show="activeTab === 'denda'" style="display: none;">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-sm border-collapse border border-stroke mt-1">
                            <thead>
                                <tr class="bg-slate-100 border-b border-stroke text-black">
                                    <th class="p-2 border-r border-stroke">Tgl Kembali</th>
                                    <th class="p-2 border-r border-stroke">Kode Eksemplar</th>
                                    <th class="p-2 border-r border-stroke">Judul Buku</th>
                                    <th class="p-2 border-r border-stroke">Nominal Denda</th>
                                    <th class="p-2">Aksi</th>
                                </tr>
                            </thead>
                            <tbody>
                                <template x-for="denda in (member?.history_loans || []).filter(h => h.fine_amount > 0 && h.fine_status === 'BELUM_LUNAS')" :key="denda.id">
                                    <tr class="border-b border-stroke hover:bg-slate-50">
                                        <td class="p-2 border-r border-stroke text-black font-medium" x-text="denda.return_date.substring(0,10)"></td>
                                        <td class="p-2 border-r border-stroke text-black" x-text="denda.no_induk"></td>
                                        <td class="p-2 border-r border-stroke text-black" x-text="denda.judul"></td>
                                        <td class="p-2 border-r border-stroke text-danger font-bold text-lg" x-text="'Rp ' + denda.fine_amount"></td>
                                        <td class="p-2 text-center">
                                            <button @click="payFine(denda.id)" class="text-xs bg-success hover:bg-opacity-90 text-white px-4 py-1.5 rounded font-medium shadow-sm transition">Bayar Lunas</button>
                                        </td>
                                    </tr>
                                </template>
                                <tr x-show="(member?.history_loans || []).filter(h => h.fine_amount > 0 && h.fine_status === 'BELUM_LUNAS').length === 0">
                                    <td colspan="5" class="p-6 text-center text-slate-500 bg-slate-50 border border-dashed border-stroke">
                                        Anggota ini tidak memiliki denda yang belum dibayar.
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
'''
# inject before the history tab
html = html.replace("<!-- Tab Content: Sejarah Peminjaman -->", new_contents + "\n                <!-- Tab Content: Sejarah Peminjaman -->")

# 5. Add payFine JS
pay_fine_js = '''        async payFine(loanId) {
            if(!confirm('Tandai denda ini sebagai LUNAS?')) return;
            try {
                const response = await fetch('/api/sirkulasi/pay_fine', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ loan_id: loanId })
                });
                const result = await response.json();
                if (result.status === 'success') {
                    this.showAlert('success', 'Denda Lunas', 'Denda telah berhasil dibayar.');
                    await this.refreshMemberData();
                } else {
                    this.showAlert('error', 'Gagal', result.message);
                }
            } catch (err) {
                this.showAlert('error', 'Error', 'Gagal memproses pembayaran denda.');
            }
        },'''
html = html.replace('async processReturnFromList(bookId) {', pay_fine_js + '\n\n        async processReturnFromList(bookId) {')

with codecs.open('templates/sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html)
print("UI Updated.")
