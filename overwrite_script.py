import codecs
import re

with codecs.open('templates/sirkulasi.html', 'r', 'utf-8') as f:
    html = f.read()

new_script = '''<script>
function sirkulasiApp() {
    return {
        memberId: '',
        member: null,
        isLoadingMember: false,
        
        borrowBookId: '',
        isBorrowing: false,
        
        returnBookId: '',
        isLoadingReturn: false,
        
        logs: [],
        logCounter: 0,
        
        alert: { show: false, type: '', title: '', message: '' },
        
        get canBorrow() {
            if (!this.member) return false;
            if (this.member.status !== 'AKTIF') return false;
            if (this.member.active_loans >= this.member.max_loans) return false;
            return true;
        },

        showAlert(type, title, message) {
            this.alert = { show: true, type, title, message };
            setTimeout(() => { this.alert.show = false; }, 5000);
        },

        resetMember() {
            this.member = null;
            this.memberId = '';
            this.borrowBookId = '';
            setTimeout(() => document.querySelector('[x-model="memberId"]').focus(), 100);
        },

        async fetchMember() {
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
        },

        async processBorrow() {
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
                    
                    this.showAlert('success', 'Berhasil', 'Buku <b>' + this.borrowBookId + '</b> berhasil dipinjamkan.');
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
        },

        async processReturn() {
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
                        this.showAlert('error', 'Terlambat & Denda', 'Terlambat ' + result.data.terlambat_hari + ' hari kerja (di luar libur/weekend). Denda Rp ' + result.data.denda + '. Akun peminjam otomatis dibekukan sampai besok.');
                    } else {
                        this.showAlert('success', 'Berhasil', 'Buku <b>' + this.returnBookId + '</b> berhasil dikembalikan tepat waktu.');
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
        }
    }
}
</script>'''

pattern = re.compile(r'<script>.*?</script>', re.DOTALL)
html = pattern.sub(new_script, html)

with codecs.open('templates/sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html)
print("Rewrote script")
