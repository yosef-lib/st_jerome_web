import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    html = f.read()

old_bad = """            li.innerHTML = 
                <div>
                    <span class="font-bold text-primary inline-block w-16"></span>
                    <span class="text-black"></span>
                </div>
                <button type="button" class="text-xs bg-slate-200 hover:bg-primary hover:text-white px-3 py-1 rounded transition">Pilih</button>
            ;"""

new_good = """            li.innerHTML = `
                <div>
                    <span class="font-bold text-primary inline-block w-16">${item.code}</span>
                    <span class="text-black">${item.desc}</span>
                </div>
                <button type="button" class="text-xs bg-slate-200 hover:bg-primary hover:text-white px-3 py-1 rounded transition">Pilih</button>
            `;"""

html = html.replace(old_bad, new_good)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(html)
print("Fixed JS syntax eaten by PowerShell.")
