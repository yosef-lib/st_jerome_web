import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    html = f.read()

# Add a print button next to Edit and Delete
old_actions = '''                              <a href="/koleksi/edit/{{ buku.id }}" class="hover:text-primary transition" title="Edit">
                                  <i class="fa-solid fa-pen-to-square"></i>
                              </a>'''
new_actions = '''                              <button type="button" onclick="addToPrintQueue('{{ buku.no_induk }}')" class="hover:text-success transition text-slate-500" title="Tambahkan ke Antrean Cetak Stiker">
                                  <i class="fa-solid fa-print"></i>
                              </button>
                              <a href="/koleksi/edit/{{ buku.id }}" class="hover:text-primary transition" title="Edit">
                                  <i class="fa-solid fa-pen-to-square"></i>
                              </a>'''
html = html.replace(old_actions, new_actions)

# Add JS script at the bottom
js = '''
<script>
async function addToPrintQueue(no_induk) {
    try {
        const res = await fetch('/api/antrean/existing', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({no_induk: no_induk})
        });
        const data = await res.json();
        if(data.status === 'success') {
            alert('Buku berhasil ditambahkan ke Antrean Cetak Stiker!');
        } else {
            alert(data.message || 'Gagal menambahkan.');
        }
    } catch(e) {
        alert('Terjadi kesalahan jaringan.');
    }
}
</script>
'''

html = html.replace('{% endblock %}', js + '\n{% endblock %}')

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(html)
print("success koleksi")
