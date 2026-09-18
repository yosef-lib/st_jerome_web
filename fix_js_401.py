import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

old_biblio = """                const ct = res.headers.get('content-type') || '';
                if (!ct.includes('json')) { alert('Sesi habis, silakan login ulang.'); window.location='/login'; return; }
                const data = await res.json();
                if (data.status === 'success') {
                    this.expandedId = null;
                    this.loadData(this.currentPage);
                    alert('Buku berhasil dihapus!');
                } else {
                    alert('Gagal: ' + (data.message || res.status));
                }"""

new_biblio = """                if (res.status === 401) { alert('Sesi habis! Silakan refresh halaman dan coba lagi.'); return; }
                const data = await res.json();
                if (data.status === 'success') {
                    this.expandedId = null;
                    this.loadData(this.currentPage);
                } else {
                    alert('Gagal: ' + (data.message || res.status));
                }"""

old_eks = """                const ct = res.headers.get('content-type') || '';
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
                }"""

new_eks = """                if (res.status === 401) { alert('Sesi habis! Silakan refresh halaman dan coba lagi.'); return; }
                const data = await res.json();
                if (data.status === 'success') {
                    const bid = this.expandedId;
                    this.expandedId = null;
                    this.eksemplarList = [];
                    await this.toggleEksemplar(bid);
                    this.loadData(this.currentPage);
                } else {
                    alert('Gagal: ' + (data.message || res.status));
                }"""

code = code.replace(old_biblio, new_biblio)
code = code.replace(old_eks, new_eks)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("JS fixed to use 401 check")
