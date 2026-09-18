import codecs, re

with codecs.open('templates/cetak_khusus.html', 'r', 'utf-8') as f:
    html = f.read()

# Update placeholder
html = html.replace('placeholder="Cari Judul / Pengarang"', 'placeholder="Cari Judul / Pengarang / No Induk"')

# Replace script
old_script = '''<script>
document.addEventListener('DOMContentLoaded', () => {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.chk-buku');
    
    selectAll.addEventListener('change', (e) => {
        checkboxes.forEach(chk => chk.checked = e.target.checked);
    });
});

async function cetakTerpilih() {
    const checkboxes = document.querySelectorAll('.chk-buku:checked');
    const selectedIds = Array.from(checkboxes).map(chk => chk.value);'''

new_script = '''<script>
let selectedBooks = JSON.parse(sessionStorage.getItem('selectedBooks_khusus') || '[]');

function updateBadge() {
    const badge = document.getElementById('selectedBadge');
    if(badge) {
        badge.innerText = selectedBooks.length + " Buku Terpilih";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateBadge();
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.chk-buku');
    
    // Restore state from session storage
    checkboxes.forEach(chk => {
        if(selectedBooks.includes(chk.value)) {
            chk.checked = true;
        }
        
        // Listen to individual changes
        chk.addEventListener('change', (e) => {
            if(e.target.checked) {
                if(!selectedBooks.includes(chk.value)) selectedBooks.push(chk.value);
            } else {
                selectedBooks = selectedBooks.filter(id => id !== chk.value);
            }
            sessionStorage.setItem('selectedBooks_khusus', JSON.stringify(selectedBooks));
            updateBadge();
        });
    });
    
    // Select all on current page
    selectAll.addEventListener('change', (e) => {
        checkboxes.forEach(chk => {
            chk.checked = e.target.checked;
            // Dispatch event to trigger array update
            chk.dispatchEvent(new Event('change'));
        });
    });
});

async function cetakTerpilih() {
    const selectedIds = JSON.parse(sessionStorage.getItem('selectedBooks_khusus') || '[]');'''

html = html.replace(old_script, new_script)

# Add a badge to the UI next to the Cetak button
old_btn = '''            <button onclick="cetakTerpilih()" class="flex justify-center rounded bg-primary py-2 px-6 font-medium text-white hover:bg-opacity-90 transition gap-2">
                <i class="fa-solid fa-print mt-1"></i> Cetak PDF Terpilih
            </button>'''
new_btn = '''            <div class="flex items-center gap-4">
                <button onclick="cetakTerpilih()" class="flex justify-center rounded bg-primary py-2 px-6 font-medium text-white hover:bg-opacity-90 transition gap-2">
                    <i class="fa-solid fa-print mt-1"></i> Cetak PDF Terpilih
                </button>
                <span id="selectedBadge" class="inline-flex rounded-full bg-warning bg-opacity-20 py-1 px-3 text-sm font-medium text-warning">0 Buku Terpilih</span>
                <button onclick="resetSelection()" class="text-sm text-danger hover:underline">Reset Pilihan</button>
            </div>'''
html = html.replace(old_btn, new_btn)

# Add resetSelection function
reset_func = '''
function resetSelection() {
    if(!confirm("Kosongkan semua pilihan buku?")) return;
    selectedBooks = [];
    sessionStorage.setItem('selectedBooks_khusus', JSON.stringify(selectedBooks));
    document.querySelectorAll('.chk-buku').forEach(chk => chk.checked = false);
    document.getElementById('selectAll').checked = false;
    updateBadge();
}
'''
html = html.replace('async function cetakTerpilih() {', reset_func + '\nasync function cetakTerpilih() {')

with codecs.open('templates/cetak_khusus.html', 'w', 'utf-8') as f:
    f.write(html)
print("cetak_khusus updated")
