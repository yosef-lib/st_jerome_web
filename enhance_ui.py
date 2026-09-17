import codecs
import re

# 1. Update Kiosk.html Autocomplete Logic
with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    kiosk = f.read()

old_js = '''if(data.length > 0) {
                        data.forEach(name => {
                            const div = document.createElement('div');
                            div.innerHTML = name;
                            div.addEventListener('click', () => {
                                tamuNama.value = name;
                                autocompleteList.classList.add('hidden');
                            });
                            autocompleteList.appendChild(div);
                        });'''

new_js = '''if(data.length > 0) {
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
                        });'''

kiosk = kiosk.replace(old_js, new_js)

# Fix the innerHTML styling just in case it didn't look good before (we replaced it entirely)
old_ac_list = '''<div id="autocompleteList" class="absolute z-40 w-full bg-white border border-stroke rounded-lg mt-1 shadow-lg hidden max-h-48 overflow-y-auto no-scrollbar">'''
new_ac_list = '''<div id="autocompleteList" class="absolute z-40 w-full bg-white border border-stroke rounded-lg mt-1 shadow-lg hidden max-h-60 overflow-y-auto no-scrollbar">'''
kiosk = kiosk.replace(old_ac_list, new_ac_list)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(kiosk)

# 2. Update analitik_kunjungan.html
with codecs.open('templates/analitik_kunjungan.html', 'r', 'utf-8') as f:
    analitik = f.read()

old_cards = '''<div class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5 mb-6">
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default">
            <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2">
                <i class="fa-solid fa-users text-primary text-xl"></i>
            </div>
            <div class="mt-4 flex items-end justify-between">
                <div>
                    <h4 class="text-title-md font-bold text-black">
                        {{ kunjungan_hari_ini }}
                    </h4>
                    <span class="text-sm font-medium">Kunjungan Hari Ini</span>
                </div>
            </div>
        </div>
        
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default md:col-span-1 xl:col-span-3">'''

new_cards = '''<div class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5 mb-6">
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default">
            <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2">
                <i class="fa-solid fa-users text-primary text-xl"></i>
            </div>
            <div class="mt-4 flex items-end justify-between">
                <div>
                    <h4 class="text-title-md font-bold text-black">
                        {{ kunjungan_hari_ini }}
                    </h4>
                    <span class="text-sm font-medium">Kunjungan Hari Ini</span>
                </div>
            </div>
            <div class="mt-4 pt-4 border-t border-stroke">
                <p class="text-sm flex justify-between"><span class="text-slate-500">Anggota:</span> <span class="font-bold text-black">{{ member_hari_ini }}</span></p>
                <p class="text-sm flex justify-between mt-1"><span class="text-slate-500">Non-Member:</span> <span class="font-bold text-black">{{ non_member_hari_ini }}</span></p>
            </div>
        </div>
        
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default xl:col-span-2">
            <h4 class="font-bold text-black mb-4">Sebaran Fakultas Hari Ini</h4>
            {% if fakultas_hari_ini %}
                <div class="space-y-2">
                    {% for f in fakultas_hari_ini %}
                    <div class="flex items-center justify-between text-sm">
                        <span class="text-slate-600 truncate mr-2">{{ f.fakultas }}</span>
                        <span class="font-bold bg-primary/10 text-primary py-0.5 px-2 rounded">{{ f.jumlah }}</span>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <p class="text-sm text-slate-500">Belum ada kunjungan berfakultas hari ini.</p>
            {% endif %}
        </div>
        
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default md:col-span-2 xl:col-span-1 flex flex-col justify-center">'''

# Let's use regex instead since old_cards might be fragile.
analitik_pattern = r'<div class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5 mb-6">.*?<form action="/export_kunjungan"'
analitik_new = '''<div class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5 mb-6">
        <!-- Card 1: Total Hari Ini -->
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default">
            <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2">
                <i class="fa-solid fa-users text-primary text-xl"></i>
            </div>
            <div class="mt-4 flex items-end justify-between">
                <div>
                    <h4 class="text-title-md font-bold text-black">
                        {{ kunjungan_hari_ini }}
                    </h4>
                    <span class="text-sm font-medium">Kunjungan Hari Ini</span>
                </div>
            </div>
            <div class="mt-4 pt-4 border-t border-stroke">
                <p class="text-sm flex justify-between"><span class="text-slate-500">Anggota:</span> <span class="font-bold text-black">{{ member_hari_ini }}</span></p>
                <p class="text-sm flex justify-between mt-1"><span class="text-slate-500">Non-Member:</span> <span class="font-bold text-black">{{ non_member_hari_ini }}</span></p>
            </div>
        </div>
        
        <!-- Card 2: Sebaran Fakultas -->
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default xl:col-span-1 max-h-48 overflow-y-auto no-scrollbar">
            <h4 class="font-bold text-black mb-4">Fakultas Hari Ini</h4>
            {% if fakultas_hari_ini %}
                <div class="space-y-2">
                    {% for f in fakultas_hari_ini %}
                    <div class="flex items-center justify-between text-sm">
                        <span class="text-slate-600 truncate mr-2">{{ f.fakultas }}</span>
                        <span class="font-bold bg-primary/10 text-primary py-0.5 px-2 rounded">{{ f.jumlah }}</span>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <p class="text-sm text-slate-500">Kosong.</p>
            {% endif %}
        </div>
        
        <!-- Card 3: Export -->
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default md:col-span-2 xl:col-span-2">
            <h4 class="font-bold text-black mb-4">Ekspor Data Borang Akreditasi</h4>
            <form action="/export_kunjungan"'''

analitik = re.sub(analitik_pattern, analitik_new, analitik, flags=re.DOTALL)

with codecs.open('templates/analitik_kunjungan.html', 'w', 'utf-8') as f:
    f.write(analitik)

print("Updated UI templates")
