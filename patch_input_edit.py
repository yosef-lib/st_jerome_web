import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    code = f.read()

js_init = '''
        init() {
            const urlParams = new URLSearchParams(window.location.search);
            const editId = urlParams.get('edit');
            if (editId) {
                this.loadEditData(editId);
            }
        },
        async loadEditData(id) {
            try {
                // We can use the biblio search API or a new one to get data.
                // Wait, I can just use fetch('/api/bibliografi/search') with ID?
                // Actually I don't have a single GET API. Let's create one in app.py.
                const res = await fetch('/api/bibliografi/get/' + id);
                if (res.ok) {
                    const data = await res.json();
                    this.selectBiblio(data);
                    // Force biblio_id to enable edit mode properly
                    this.form.biblio_id = data.id;
                    this.form.jumlah = 0; // default 0 for edit mode
                }
            } catch (e) { console.error(e); }
        },
'''
code = code.replace("notif: { show: false, type: 'success', title: '', message: '' },", "notif: { show: false, type: 'success', title: '', message: '' },\n" + js_init)

# When form.biblio_id is set (edit mode), we want to allow editing the fields! Currently they are disabled!
# Let's remove the disabled property!
code = code.replace(':disabled="form.biblio_id"', '')
code = code.replace(":class=\"form.biblio_id ? 'bg-slate-100' : ''\"", '')

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(code)
print("Patched input_buku.html for edit mode")
