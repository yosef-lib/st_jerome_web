import codecs
import re

with codecs.open('templates/sirkulasi.html', 'r', 'utf-8') as f:
    html = f.read()

# Replace fetchMember
old_fetch = '''        async fetchMember() {
            if (!this.memberId.trim()) return;
            this.isLoadingMember = true;
            
            // Dummy simulation for now until backend API is ready
            // We will hook this up to actual Python backend next.
            setTimeout(() => {
                this.member = {
                    id: this.memberId,
                    nama: 'Fr. ' + this.memberId, // Dummy
                    tipe: 'Reguler',
                    status: 'AKTIF', // Or DIBLOKIR
                    suspended_until: '-',
                    active_loans: 0,
                    max_loans: 2
                };
                this.isLoadingMember = false;
                
                // Focus on borrow book input
                setTimeout(() => document.querySelector('[x-model="borrowBookId"]').focus(), 100);
            }, 500);
        },'''

new_fetch = '''        async fetchMember() {
            if (!this.memberId.trim()) return;
            this.isLoadingMember = true;
            
            try {
                const response = await fetch('/api/sirkulasi/member/' + encodeURIComponent(this.memberId));
                const result = await response.json();
                
                if (result.status === 'success') {
                    this.member = result.data;
                    setTimeout(() => document.querySelector('[x-model="borrowBookId"]').focus(), 100);
                } else {
                    this.showAlert('error', 'Gagal', result.message);
                    this.member = null;
                }
            } catch (err) {
                this.showAlert('error', 'Error', 'Gagal terhubung ke server.');
            } finally {
                this.isLoadingMember = false;
            }
        },'''
html = html.replace(old_fetch, new_fetch)

# Replace processBorrow
old_borrow = '''        async processBorrow() {
            if (!this.borrowBookId.trim() || !this.canBorrow) return;
            this.isBorrowing = true;
            
            // Dummy simulation
            setTimeout(() => {
                this.logCounter++;
                this.logs.push({
                    id: this.logCounter,
                    type: 'borrow',
                    time: new Date().toLocaleTimeString('id-ID'),
                    buku_judul: 'Buku Dummy ' + this.borrowBookId,
                    buku_id: this.borrowBookId,
                    anggota_nama: this.member.nama,
                    denda: 0
                });
                
                this.showAlert('success', 'Berhasil', Buku <b>\</b> berhasil dipinjamkan kepada <b>\</b>.);
                this.member.active_loans++;
                this.borrowBookId = '';
                this.isBorrowing = false;
            }, 500);
        },'''

new_borrow = '''        async processBorrow() {
            if (!this.borrowBookId.trim() || !this.canBorrow) return;
            this.isBorrowing = true;
            
            try {
                const response = await fetch('/api/sirkulasi/borrow', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        member_id: this.member.id,
                        book_id: this.borrowBookId
                    })
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    this.logCounter++;
                    this.logs.push({
                        id: this.logCounter,
                        type: 'borrow',
                        time: new Date().toLocaleTimeString('id-ID'),
                        buku_judul: result.data.buku_judul,
                        buku_id: this.borrowBookId,
                        anggota_nama: this.member.nama,
                        denda: 0
                    });
                    
                    this.showAlert('success', 'Berhasil', Buku <b>\</b> berhasil dipinjamkan.);
                    this.member.active_loans++;
                    this.borrowBookId = '';
                } else {
                    this.showAlert('error', 'Gagal', result.message);
                }
            } catch (err) {
                this.showAlert('error', 'Error', 'Gagal memproses peminjaman.');
            } finally {
                this.isBorrowing = false;
            }
        },'''
html = html.replace(old_borrow, new_borrow)

# Replace processReturn
old_return = '''        async processReturn() {
            if (!this.returnBookId.trim()) return;
            this.isLoadingReturn = true;
            
            // Dummy simulation
            setTimeout(() => {
                this.logCounter++;
                // Randomize fake fine for UI testing
                let isLate = Math.random() > 0.7;
                let days = isLate ? 3 : 0;
                let denda = days * 500;
                
                this.logs.push({
                    id: this.logCounter,
                    type: 'return',
                    time: new Date().toLocaleTimeString('id-ID'),
                    buku_judul: 'Buku Dummy ' + this.returnBookId,
                    buku_id: this.returnBookId,
                    anggota_nama: 'Fr. Anonymous',
                    denda: denda,
                    terlambat_hari: days
                });
                
                if (denda > 0) {
                    this.showAlert('error', 'Terlambat & Denda', Buku kembali terlambat \ hari. Denda Rp \. Akun otomatis dibekukan.);
                } else {
                    this.showAlert('success', 'Berhasil', Buku <b>\</b> berhasil dikembalikan tepat waktu.);
                }
                
                this.returnBookId = '';
                this.isLoadingReturn = false;
            }, 500);
        }'''

new_return = '''        async processReturn() {
            if (!this.returnBookId.trim()) return;
            this.isLoadingReturn = true;
            
            try {
                const response = await fetch('/api/sirkulasi/return', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        book_id: this.returnBookId
                    })
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    this.logCounter++;
                    this.logs.push({
                        id: this.logCounter,
                        type: 'return',
                        time: new Date().toLocaleTimeString('id-ID'),
                        buku_judul: result.data.buku_judul,
                        buku_id: this.returnBookId,
                        anggota_nama: result.data.anggota_nama || '-',
                        denda: result.data.denda,
                        terlambat_hari: result.data.terlambat_hari
                    });
                    
                    if (result.data.denda > 0) {
                        this.showAlert('error', 'Terlambat & Denda', Terlambat \ hari kerja (di luar libur/weekend). Denda Rp \. Akun peminjam otomatis dibekukan sampai besok.);
                    } else {
                        this.showAlert('success', 'Berhasil', Buku <b>\</b> berhasil dikembalikan tepat waktu.);
                    }
                    this.returnBookId = '';
                } else {
                    this.showAlert('error', 'Gagal', result.message);
                }
            } catch (err) {
                this.showAlert('error', 'Error', 'Gagal memproses pengembalian.');
            } finally {
                this.isLoadingReturn = false;
            }
        }'''
html = html.replace(old_return, new_return)

with codecs.open('templates/sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html)
print("Connected UI to actual API.")
