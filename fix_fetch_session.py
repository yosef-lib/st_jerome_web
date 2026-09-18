import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

old_biblio = '''        async deleteBiblio(id) {
            if (!confirm("Peringatan: Anda akan menghapus judul buku ini BESERTA seluruh salinannya! Lanjutkan?")) return;
            try {
                const res = await fetch('/api/bibliografi/' + id, { method: 'DELETE' });
                if (res.ok) {
                    this.loadData(this.currentPage);
                }
            } catch (e) {
                console.error(e); alert("Error");
            }
        },'''

new_biblio = '''        async deleteBiblio(id) {
            if (!confirm("Peringatan: Anda akan menghapus judul buku ini BESERTA seluruh salinannya! Lanjutkan?")) return;
            try {
                const res = await fetch('/api/bibliografi/' + id, { method: 'DELETE', credentials: 'same-origin' });
                const ct = res.headers.get('content-type') || '';
                if (!ct.includes('json')) { alert('Sesi habis, silakan login ulang.'); window.location='/login'; return; }
                const data = await res.json();
                if (data.status === 'success') {
                    this.expandedId = null;
                    this.loadData(this.currentPage);
                    alert('Buku berhasil dihapus!');
                } else {
                    alert('Gagal: ' + (data.message || res.status));
                }
            } catch (e) {
                console.error(e); alert("Error: " + e.message);
            }
        },'''

old_eks = '''        async deleteEksemplar(no_induk) {
            if (!confirm("Hapus barcode " + no_induk + "?")) return;
            try {
                const res = await fetch('/api/eksemplar/' + encodeURIComponent(no_induk), { method: 'DELETE' });
                if (res.ok) {
                    // refresh eksemplar list
                    await this.toggleEksemplar(this.expandedId);
                    this.loadData(this.currentPage);
                }
            } catch (e) {
                console.error(e); alert("Error");
            }
        },'''

new_eks = '''        async deleteEksemplar(no_induk) {
            if (!confirm("Hapus barcode " + no_induk + "?")) return;
            try {
                const res = await fetch('/api/eksemplar/' + encodeURIComponent(no_induk), { method: 'DELETE', credentials: 'same-origin' });
                const ct = res.headers.get('content-type') || '';
                if (!ct.includes('json')) { alert('Sesi habis, silakan login ulang.'); window.location='/login'; return; }
                const data = await res.json();
                if (data.status === 'success') {
                    // Refresh eksemplar list in place
                    const bid = this.expandedId;
                    this.expandedId = null;
                    this.eksemplarList = [];
                    await this.toggleEksemplar(bid);
                    this.loadData(this.currentPage);
                } else {
                    alert('Gagal: ' + (data.message || res.status));
                }
            } catch (e) {
                console.error(e); alert("Error: " + e.message);
            }
        },'''

if old_biblio in code:
    code = code.replace(old_biblio, new_biblio)
    print("Replaced biblio delete")
else:
    print("WARNING: biblio delete string not found!")
    
if old_eks in code:
    code = code.replace(old_eks, new_eks)
    print("Replaced eks delete")
else:
    print("WARNING: eks delete string not found!")

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
