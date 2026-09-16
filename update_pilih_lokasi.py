with open('templates/pilih_lokasi.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_stpd = '''                <div class="mb-5 flex h-20 w-20 items-center justify-center rounded-full bg-primary/10 text-primary group-hover:bg-primary group-hover:text-white transition duration-300">
                    <i class="fa-solid fa-building-columns text-4xl"></i>
                </div>'''

new_stpd = '''                <div class="mb-5 flex h-24 w-24 items-center justify-center rounded-full bg-white shadow-sm overflow-hidden group-hover:shadow-md transition duration-300 p-2">
                    <img src="{{ url_for('static', filename='img/logo_stpd.png') }}" alt="STPD" class="w-full h-full object-contain" />
                </div>'''

old_imavi = '''                <div class="mb-5 flex h-20 w-20 items-center justify-center rounded-full bg-success/10 text-success group-hover:bg-success group-hover:text-white transition duration-300">
                    <i class="fa-solid fa-church text-4xl"></i>
                </div>'''

new_imavi = '''                <div class="mb-5 flex h-24 w-24 items-center justify-center rounded-full bg-white shadow-sm overflow-hidden group-hover:shadow-md transition duration-300 p-2">
                    <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" alt="IMAVI" class="w-full h-full object-contain" />
                </div>'''

content = content.replace(old_stpd, new_stpd)
content = content.replace(old_imavi, new_imavi)

with open('templates/pilih_lokasi.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("done lokasi")
