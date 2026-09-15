document.addEventListener("DOMContentLoaded", function() {
    loadAntrean();

    const inputPengarang = document.getElementById("inputPengarang");
    const inputJudul     = document.getElementById("inputJudul");
    const inputCutter    = document.getElementById("inputCutter");
    const inputHurufJudul= document.getElementById("inputHurufJudul");

    // Auto Cutter — 3 huruf kapital pertama pengarang
    if (inputPengarang) {
        inputPengarang.addEventListener("input", function() {
            const text = this.value.replace(/[^a-zA-Z]/g, '');
            inputCutter.value = text.substring(0, 3).toUpperCase();
        });
    }

    // Auto Huruf Judul — 1 huruf kecil pertama judul
    if (inputJudul) {
        inputJudul.addEventListener("input", function() {
            const text = this.value.replace(/[^a-zA-Z]/g, '');
            inputHurufJudul.value = text.length ? text[0].toLowerCase() : '';
        });
    }

    // Form Submit
    const form = document.getElementById("formInputBuku");
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            const data = Object.fromEntries(new FormData(form).entries());

            fetch('/api/antrean', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(r => r.json())
            .then(res => {
                if (res.status === 'success') {
                    form.reset();
                    loadAntrean();
                    showToast('✅ Buku berhasil ditambahkan ke antrean!');
                }
            });
        });
    }
});

function loadAntrean() {
    fetch('/api/antrean')
    .then(r => r.json())
    .then(data => {
        const list = document.getElementById("listAntrean");
        if (!list) return;

        if (!data || data.length === 0) {
            list.innerHTML = `
                <div style="text-align:center; padding:40px 0; color:var(--text-muted);">
                    <div style="font-size:36px;">📋</div>
                    <div style="font-size:13px; margin-top:8px;">Antrean kosong</div>
                </div>`;
            return;
        }

        list.innerHTML = data.map((item, i) => `
            <div class="queue-item">
                <div>
                    <div class="queue-item-title">${item.judul}</div>
                    <div class="queue-item-callnum">
                        <span class="badge-callnum">${item.klasifikasi || ''} ${item.cutter || ''} ${item.huruf_judul || ''}</span>
                        &nbsp;No: ${item.no_induk || ''}
                    </div>
                </div>
                <button class="btn btn-danger-soft btn-sm" onclick="hapusAntrean(${i})" title="Hapus">✕</button>
            </div>
        `).join('');
    });
}

function hapusAntrean(index) {
    fetch('/api/antrean/hapus', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ index })
    })
    .then(r => r.json())
    .then(res => { if (res.status === 'success') loadAntrean(); });
}

function kosongkanAntrean() {
    if (!confirm("Yakin kosongkan semua antrean stiker?\nData buku di database tidak akan terhapus.")) return;
    fetch('/api/antrean/hapus_semua', { method: 'POST' })
    .then(r => r.json())
    .then(() => loadAntrean());
}

function cetakPDF() {
    window.location.href = '/cetak_pdf';
}

function showToast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.innerText = msg;
    t.style.display = 'block';
    setTimeout(() => t.style.display = 'none', 3000);
}
