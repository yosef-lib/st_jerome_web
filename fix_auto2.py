import codecs

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    kiosk = f.read()

import re

# We can just replace the whole autocomplete JS block
pattern = r'tamuNama\.addEventListener\(\'input\', function\(\) \{.*?\n        \}\);'

new_js = '''tamuNama.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            const val = this.value;
            if(val.length < 3) {
                autocompleteList.classList.add('hidden');
                return;
            }
            debounceTimer = setTimeout(async () => {
                const res = await fetch('/api/kunjungan/autocomplete?q=' + encodeURIComponent(val));
                if(res.ok) {
                    const data = await res.json();
                    autocompleteList.innerHTML = '';
                    if(data.length > 0) {
                        data.forEach(item => {
                            const div = document.createElement('div');
                            div.className = 'px-4 py-2 hover:bg-gray-50 cursor-pointer border-b border-stroke last:border-b-0';
                            div.innerHTML = <p class="font-bold text-black">\</p><p class="text-xs text-slate-500">\ - \</p>;
                            div.addEventListener('click', () => {
                                tamuNama.value = item.identitas;
                                document.getElementById('tamuInstansi').value = item.asal_instansi || '';
                                document.getElementById('tamuPeran').value = item.peran_jabatan || '';
                                document.getElementById('tamuFakultas').value = item.fakultas || '';
                                checkPeran();
                                autocompleteList.classList.add('hidden');
                            });
                            autocompleteList.appendChild(div);
                        });
                        autocompleteList.classList.remove('hidden');
                    } else {
                        autocompleteList.classList.add('hidden');
                    }
                }
            }, 300);
        });'''

kiosk = re.sub(pattern, new_js, kiosk, flags=re.DOTALL)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(kiosk)
