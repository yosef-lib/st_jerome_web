import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

old_td = """<td class="p-3 font-semibold text-primary" x-text="b.judul"></td>"""

new_td = """<td class="p-3">
    <div class="flex items-start gap-3">
        <div class="w-10 h-14 bg-slate-100 border border-slate-200 rounded flex-shrink-0 flex justify-center items-center overflow-hidden">
            <template x-if="b.cover_url">
                <img :src="b.cover_url" class="w-full h-full object-cover" @error="b.cover_url = null" alt="cover">
            </template>
            <template x-if="!b.cover_url">
                <i class="fa-solid fa-book text-slate-300 text-lg"></i>
            </template>
        </div>
        <div>
            <div class="font-semibold text-primary leading-tight" x-text="b.judul"></div>
            <div class="text-xs text-slate-400 mt-1" x-show="b.isbn" x-text="'ISBN: ' + b.isbn"></div>
        </div>
    </div>
</td>"""

code = code.replace(old_td, new_td)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("UI patched for cover thumbnails")
