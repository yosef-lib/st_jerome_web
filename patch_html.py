import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    code = f.read()

# Add file input
file_html = '''
                    <div class="md:col-span-3">
                        <label class="block text-sm font-medium mb-1">Gambar Sampul / Cover (Opsional)</label>
                        <input type="file" @change="handleFile" accept="image/*" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black">
                        <div x-show="imagePreview" class="mt-2">
                            <img :src="imagePreview" class="h-32 object-contain border border-stroke rounded p-1">
                        </div>
                    </div>
'''
code = code.replace('<!-- SECTION 2: Eksemplar -->', file_html + '\n            <!-- SECTION 2: Eksemplar -->')

# Update Alpine component
js_add = '''
        imageFile: null,
        imagePreview: null,
        
        handleFile(e) {
            const file = e.target.files[0];
            if (file) {
                this.imageFile = file;
                this.imagePreview = URL.createObjectURL(file);
            }
        },
'''
code = code.replace('jumlah: 1\n        },', 'jumlah: 1\n        },\n' + js_add)

submit_logic = '''
            try {
                const formData = new FormData();
                for (let key in this.form) {
                    if (this.form[key] !== null && this.form[key] !== '') {
                        formData.append(key, this.form[key]);
                    }
                }
                if (this.imageFile) {
                    formData.append('image', this.imageFile);
                }

                const res = await fetch('/api/buku/input_batch', {
                    method: 'POST',
                    body: formData
                });
'''
code = code.replace('''            try {
                const res = await fetch('/api/buku/input_batch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.form)
                });''', submit_logic)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(code)
print("Patched input_buku.html for image upload")
