import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    code = f.read()

old_select = '''<select name="lokasi" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2.5 px-4 outline-none transition focus:border-primary active:border-primary">
                        <option value="STPD">STPD</option>
                        <option value="IMAVI">IMAVI</option>
                    </select>'''

new_select = '''<select name="lokasi" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2.5 px-4 outline-none transition focus:border-primary active:border-primary">
                        <option value="IMAVI" selected>IMAVI</option>
                        <option value="STPD">STPD</option>
                    </select>'''

code = code.replace(old_select, new_select)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(code)
