import codecs
import re

with codecs.open('templates/sirkulasi.html', 'r', 'utf-8') as f:
    html = f.read()

# 1. Update the F10 keydown on the main div
html = html.replace('''@keydown.f2.window.prevent="activeTab = 'peminjaman'" @keydown.f3.window.prevent="activeTab = 'saat_ini'"''', '''@keydown.f2.window.prevent="activeTab = 'peminjaman'" @keydown.f3.window.prevent="activeTab = 'saat_ini'" @keydown.f10.window.prevent="activeTab = 'sejarah'"''')

# 2. Update the Tabs to make F10 active
old_tabs = '''<a href="#" class="px-5 py-2 text-slate-400 cursor-not-allowed">Sejarah Peminjaman (F10)</a>'''
new_tabs = '''<a href="#" @click.prevent="activeTab = 'sejarah'" :class="activeTab === 'sejarah' ? 'text-primary border-b-2 border-primary bg-slate-50' : 'text-slate-500 hover:text-black'" class="px-5 py-2 transition">Sejarah Peminjaman (F10)</a>'''
html = html.replace(old_tabs, new_tabs)

# 3. Add the 'Perpanjang' button to the 'Pinjaman Saat Ini' table
old_kembalikan = '''<button @click="processReturnFromList(loan.no_induk)" class="text-xs bg-slate-200 hover:bg-success hover:text-white px-3 py-1.5 rounded font-medium transition shadow-sm">Kembalikan</button>'''
new_actions = '''<button @click="processReturnFromList(loan.no_induk)" class="text-xs bg-slate-200 hover:bg-success hover:text-white px-3 py-1.5 rounded font-medium transition shadow-sm mb-1 w-full">Kembalikan</button>
<button @click="processRenew(loan.no_induk)" class="text-xs bg-slate-200 hover:bg-primary hover:text-white px-3 py-1.5 rounded font-medium transition shadow-sm w-full">Perpanjang</button>'''
html = html.replace(old_kembalikan, new_actions)

# 4. Inject the History Tab Content
history_tab = '''
                <!-- Tab Content: Sejarah Peminjaman -->
                <div x-show="activeTab === 'sejarah'" style="display: none;">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-sm border-collapse border border-stroke mt-1">
                            <thead>
                                <tr class="bg-slate-100 border-b border-stroke text-black">
                                    <th class="p-2 border-r border-stroke">Kode Eksemplar</th>
                                    <th class="p-2 border-r border-stroke">Judul</th>
                                    <th class="p-2 border-r border-stroke">Tgl Pinjam</th>
                                    <th class="p-2 border-r border-stroke">Tgl Kembali</th>
                                    <th class="p-2">Status Denda</th>
                                </tr>
                            </thead>
                            <tbody>
                                <template x-for="hist in (member?.history_loans || [])" :key="hist.id">
                                    <tr class="border-b border-stroke hover:bg-slate-50">
                                        <td class="p-2 border-r border-stroke text-black" x-text="hist.no_induk"></td>
                                        <td class="p-2 border-r border-stroke font-medium text-black" x-text="hist.judul"></td>
                                        <td class="p-2 border-r border-stroke text-black" x-text="hist.loan_date.substring(0,10)"></td>
                                        <td class="p-2 border-r border-stroke font-semibold" :class="hist.fine_amount > 0 ? 'text-danger' : 'text-success'" x-text="hist.return_date.substring(0,10)"></td>
                                        <td class="p-2">
                                            <span x-show="hist.fine_amount == 0" class="text-xs text-success bg-green-100 px-2 py-0.5 rounded font-bold">LUNAS / TEPAT WAKTU</span>
                                            <span x-show="hist.fine_amount > 0" class="text-xs text-danger bg-red-100 px-2 py-0.5 rounded font-bold" x-text="'DENDA RP ' + hist.fine_amount"></span>
                                        </td>
                                    </tr>
                                </template>
                                <tr x-show="!member || !member.history_loans || member.history_loans.length === 0">
                                    <td colspan="5" class="p-6 text-center text-slate-500 bg-slate-50 border border-dashed border-stroke">
                                        Anggota ini belum memiliki sejarah peminjaman.
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
'''
html = html.replace('            </div>\n        </div>\n\n        <!-- MODE PENGEMBALIAN KILAT -->', history_tab + '        </div>\n\n        <!-- MODE PENGEMBALIAN KILAT -->')


# 5. Inject JS processRenew function
js_renew = '''        async processRenew(bookId) {
            try {
                const response = await fetch('/api/sirkulasi/renew', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ book_id: bookId })
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    this.showAlert('success', 'Perpanjang Sukses', result.message + ' (Jatuh tempo baru: ' + result.new_due_date + ')');
                    await this.refreshMemberData(); // update list
                } else {
                    this.showAlert('error', 'Gagal Diperpanjang', result.message);
                }
            } catch (err) {
                this.showAlert('error', 'Error', 'Gagal memproses perpanjangan.');
            }
        },'''
html = html.replace('async processReturnFromList(bookId) {', js_renew + '\n        \n        async processReturnFromList(bookId) {')

with codecs.open('templates/sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html)
print("Updated UI with Renew and History")
