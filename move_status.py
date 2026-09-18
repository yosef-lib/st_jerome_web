import codecs
import re

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    code = f.read()

# 1. Remove it from section 2
section2_status = """                        <div class="w-1/3">
                            <label class="block text-sm font-medium mb-1">Asal Koleksi</label>
                            <select x-model="form.status_buku" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black font-semibold text-md" required>
                                <option value="BELI">Beli</option>
                                <option value="HIBAH">Hadiah / Hibah</option>
                            </select>
                        </div>"""

code = code.replace(section2_status, "")

# 2. Add it to section 1 (e.g. next to GMD or Deskripsi Fisik)
section1_target = """                            <div class="w-1/2">
                                <label class="block text-sm font-medium mb-1">GMD</label>
                                <input type="text" x-model="form.gmd" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary" placeholder="Text">
                            </div>
                        </div>"""

section1_new = """                            <div class="w-1/2">
                                <label class="block text-sm font-medium mb-1">GMD</label>
                                <input type="text" x-model="form.gmd" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary" placeholder="Text">
                            </div>
                            <div class="w-1/2">
                                <label class="block text-sm font-medium mb-1 text-primary">Asal Koleksi (Beli/Hibah)</label>
                                <select x-model="form.status_buku" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black font-semibold" required>
                                    <option value="BELI">Beli</option>
                                    <option value="HIBAH">Hadiah / Hibah</option>
                                </select>
                            </div>
                        </div>"""

code = code.replace(section1_target, section1_new)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(code)
print("UI patched")
