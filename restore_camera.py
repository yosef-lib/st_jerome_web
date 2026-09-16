import codecs

# 1. Update scanner.html (Meja Baca)
scanner_content = '''{% extends 'layout.html' %}

{% block content %}
<div class="max-w-md mx-auto p-4 md:p-6 2xl:p-10">

    <div class="rounded-sm border border-stroke bg-white shadow-default">
        <div class="text-center pt-8 pb-4 px-6">
            <div class="inline-flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary mb-4">
                <i class="fa-solid fa-qrcode text-3xl"></i>
            </div>
            <h4 class="text-xl font-bold text-black mb-1">Pemindai Meja Baca</h4>
            <p class="text-sm font-medium text-slate-500">Arahkan kamera ke barcode buku, pencatatan otomatis ke log keterbacaan.</p>
        </div>
        
        <div class="p-6">
            <div id="reader" class="rounded-lg overflow-hidden border-2 border-stroke bg-black w-full min-h-[250px] flex items-center justify-center relative">
                <button id="btnStartScan" class="absolute z-10 flex items-center gap-2 rounded bg-primary py-3 px-6 font-medium text-white hover:bg-opacity-90 transition shadow-lg">
                    <i class="fa-solid fa-camera"></i> Buka Kamera HP
                </button>
            </div>
            
            <div class="mt-4 flex justify-center hidden" id="scanActions">
                <button id="btnStopScan" class="flex items-center gap-2 rounded border border-danger text-danger py-1.5 px-4 font-medium hover:bg-danger hover:text-white transition text-sm">
                    <i class="fa-solid fa-stop"></i> Hentikan Kamera
                </button>
            </div>
            
            <!-- Manual Input -->
            <div class="mt-6 mb-5">
                <label class="mb-2 block text-sm font-bold text-black">Atau Masukkan Manual / Gunakan Scanner Fisik:</label>
                <div class="flex gap-2">
                    <input type="text" id="manualInput" autofocus placeholder="Ketik No. Induk..." onkeypress="if(event.key === 'Enter') submitManual()" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2 px-4 outline-none transition focus:border-primary active:border-primary">
                    <button class="flex items-center justify-center rounded bg-primary py-2 px-5 font-medium text-white hover:bg-opacity-90 transition" onclick="submitManual()">Catat</button>
                </div>
            </div>

            <!-- Result Box -->
            <div id="resultBox" class="hidden text-center rounded-lg border p-5 mb-5 animate-[fadeIn_0.3s_ease-out]">
                <i id="resultIcon" class="fa-solid text-3xl mb-2"></i>
                <div id="resultTitle" class="font-bold text-lg mb-1"></div>
                <div id="resultDesc" class="font-semibold text-black text-sm"></div>
            </div>
        </div>
    </div>
</div>

<script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
<script>
    let html5QrCode;
    
    function parseScanResult(code) {
        if (html5QrCode && html5QrCode.isScanning) html5QrCode.pause();
        document.getElementById('manualInput').value = code;
        submitManual();
        setTimeout(() => {
            if (html5QrCode && html5QrCode.getState() === Html5QrcodeScannerState.PAUSED) html5QrCode.resume();
        }, 2000);
    }

    function playAudio(freq, duration, type) {
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = type;
            osc.frequency.value = freq;
            osc.start();
            setTimeout(function() { osc.stop(); }, duration);
        } catch (e) {}
    }

    function submitManual() {
        const no_induk = document.getElementById('manualInput').value.trim();
        if(!no_induk) return;
        const resultBox = document.getElementById('resultBox');
        const icon = document.getElementById('resultIcon');
        const title = document.getElementById('resultTitle');
        const desc = document.getElementById('resultDesc');
        
        resultBox.style.display = 'none';

        fetch('/api/scan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({no_induk: no_induk, mode: 'meja_baca'})
        }).then(r => r.json()).then(data => {
            resultBox.className = 'text-center rounded-lg border p-5 mb-5 animate-[fadeIn_0.3s_ease-out]';
            icon.className = 'fa-solid text-3xl mb-2';
            
            if(data.status === 'success') {
                playAudio(800, 150, 'sine');
                resultBox.classList.add('border-success', 'bg-success/10');
                icon.classList.add('fa-circle-check', 'text-success');
                title.classList.add('text-success');
                title.innerText = 'Berhasil Dicatat!';
                desc.innerText = data.message;
            } else {
                playAudio(300, 400, 'sawtooth');
                resultBox.classList.add('border-danger', 'bg-danger/10');
                icon.classList.add('fa-circle-xmark', 'text-danger');
                title.classList.add('text-danger');
                title.innerText = 'Gagal';
                desc.innerText = data.message;
            }
            resultBox.style.display = 'block';
            document.getElementById('manualInput').value = '';
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        html5QrCode = new Html5Qrcode("reader");
        const btnStart = document.getElementById('btnStartScan');
        const btnStop = document.getElementById('btnStopScan');
        const actionBox = document.getElementById('scanActions');

        btnStart.addEventListener('click', () => {
            html5QrCode.start(
                { facingMode: "environment" },
                { fps: 10, qrbox: { width: 250, height: 100 } },
                (decodedText) => { parseScanResult(decodedText); },
                (errorMessage) => {}
            ).then(() => {
                btnStart.style.display = 'none';
                actionBox.classList.remove('hidden');
            }).catch((err) => {
                alert("Gagal mengakses kamera. Pastikan koneksi HTTPS atau gunakan localhost.");
            });
        });

        btnStop.addEventListener('click', () => {
            if (html5QrCode && html5QrCode.isScanning) {
                html5QrCode.stop().then(() => {
                    btnStart.style.display = 'flex';
                    actionBox.classList.add('hidden');
                });
            }
        });
    });
</script>
{% endblock %}
'''

with codecs.open('templates/scanner.html', 'w', 'utf-8') as f:
    f.write(scanner_content)

# 2. Update audit_rak.html
audit_content = '''{% extends 'layout.html' %}

{% block content %}
<div class="max-w-md mx-auto p-4 md:p-6 2xl:p-10">

    <div class="rounded-sm border border-stroke bg-white shadow-default border-t-4 border-t-warning">
        <div class="text-center pt-8 pb-4 px-6">
            <div class="inline-flex h-16 w-16 items-center justify-center rounded-full bg-warning/10 text-warning mb-4">
                <i class="fa-solid fa-boxes-packing text-3xl"></i>
            </div>
            <h4 class="text-xl font-bold text-black mb-1">Stok Opname / Audit Rak</h4>
            <p class="text-sm font-medium text-slate-500">Scan barcode buku, sistem akan mendeteksi jika ada buku yang salah letak!</p>
        </div>
        
        <div class="px-6 mb-4">
            <label class="mb-2.5 block font-bold text-black text-center text-lg">Anda Sedang Mengaudit Rak DDC Berapa?</label>
            <select id="target_rak" class="w-full rounded border-[1.5px] border-stroke bg-warning/10 py-3 px-5 outline-none font-bold text-center">
                <option value="000">Rak 000 (Komputer & Umum)</option>
                <option value="100">Rak 100 (Filsafat & Psikologi)</option>
                <option value="200" selected>Rak 200 (Agama & Teologi)</option>
                <option value="300">Rak 300 (Ilmu Sosial)</option>
                <option value="400">Rak 400 (Bahasa)</option>
                <option value="500">Rak 500 (Sains & Mat)</option>
                <option value="600">Rak 600 (Teknologi)</option>
                <option value="700">Rak 700 (Kesenian)</option>
                <option value="800">Rak 800 (Sastra)</option>
                <option value="900">Rak 900 (Sejarah & Geografi)</option>
            </select>
        </div>

        <div class="p-6">
            <div id="reader" class="rounded-lg overflow-hidden border-2 border-stroke bg-black w-full min-h-[250px] flex items-center justify-center relative">
                <button id="btnStartScan" class="absolute z-10 flex items-center gap-2 rounded bg-warning py-3 px-6 font-medium text-black hover:bg-opacity-90 transition shadow-lg">
                    <i class="fa-solid fa-camera"></i> Buka Kamera HP
                </button>
            </div>
            
            <div class="mt-4 flex justify-center hidden" id="scanActions">
                <button id="btnStopScan" class="flex items-center gap-2 rounded border border-danger text-danger py-1.5 px-4 font-medium hover:bg-danger hover:text-white transition text-sm">
                    <i class="fa-solid fa-stop"></i> Hentikan Kamera
                </button>
            </div>
            
            <!-- Manual Input -->
            <div class="mt-6 mb-5">
                <label class="mb-2 block text-sm font-bold text-black">Atau Masukkan Manual / Gunakan Scanner Fisik:</label>
                <div class="flex gap-2">
                    <input type="text" id="manualInput" autofocus placeholder="Ketik No. Induk..." onkeypress="if(event.key === 'Enter') submitManual()" class="w-full rounded border-[1.5px] border-stroke bg-transparent py-2 px-4 outline-none transition focus:border-warning active:border-warning">
                    <button class="flex items-center justify-center rounded bg-warning py-2 px-5 font-medium text-black hover:bg-opacity-90 transition" onclick="submitManual()">Cek Rak</button>
                </div>
            </div>

            <!-- Result Box -->
            <div id="resultBox" class="hidden text-center rounded-lg border-2 p-5 mb-5 animate-[fadeIn_0.3s_ease-out]">
                <i id="resultIcon" class="fa-solid text-4xl mb-2"></i>
                <div id="resultTitle" class="font-bold text-xl mb-1"></div>
                <div id="resultDesc" class="font-semibold text-black text-sm"></div>
            </div>
        </div>
    </div>
</div>

<script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
<script>
    let html5QrCode;
    
    function parseScanResult(code) {
        if (html5QrCode && html5QrCode.isScanning) html5QrCode.pause();
        document.getElementById('manualInput').value = code;
        submitManual();
        setTimeout(() => {
            if (html5QrCode && html5QrCode.getState() === Html5QrcodeScannerState.PAUSED) html5QrCode.resume();
        }, 2500);
    }

    function playAudio(freq, duration, type) {
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = type;
            osc.frequency.value = freq;
            osc.start();
            setTimeout(function() { osc.stop(); }, duration);
        } catch (e) {}
    }

    function submitManual() {
        const no_induk = document.getElementById('manualInput').value.trim();
        const target_rak = document.getElementById('target_rak').value;
        if(!no_induk) return;

        const resultBox = document.getElementById('resultBox');
        const icon = document.getElementById('resultIcon');
        const title = document.getElementById('resultTitle');
        const desc = document.getElementById('resultDesc');
        
        resultBox.style.display = 'none';

        fetch('/api/scan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({no_induk: no_induk, mode: 'audit_rak', target_rak: target_rak})
        }).then(r => r.json()).then(data => {
            resultBox.className = 'text-center rounded-lg border-4 p-5 mb-5 animate-[fadeIn_0.3s_ease-out]';
            icon.className = 'fa-solid text-4xl mb-2';
            
            if(data.status === 'success') {
                playAudio(800, 150, 'sine');
                resultBox.classList.add('border-success', 'bg-success/10');
                icon.classList.add('fa-circle-check', 'text-success');
                title.classList.add('text-success');
                title.innerText = 'BENAR!';
                desc.innerText = data.message;
            } else if(data.status === 'danger' || data.status === 'error') {
                playAudio(300, 600, 'sawtooth');
                resultBox.classList.add('border-danger', 'bg-danger/10');
                icon.classList.add('fa-triangle-exclamation', 'text-danger');
                title.classList.add('text-danger');
                title.innerText = 'SALAH RAK!';
                desc.innerText = data.message;
            } else if(data.status === 'warning') {
                playAudio(400, 300, 'square');
                resultBox.classList.add('border-warning', 'bg-warning/10');
                icon.classList.add('fa-circle-question', 'text-warning');
                title.classList.add('text-warning');
                title.innerText = 'ANOMALI METADATA';
                desc.innerText = data.message;
            }
            resultBox.style.display = 'block';
            document.getElementById('manualInput').value = '';
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        html5QrCode = new Html5Qrcode("reader");
        const btnStart = document.getElementById('btnStartScan');
        const btnStop = document.getElementById('btnStopScan');
        const actionBox = document.getElementById('scanActions');

        btnStart.addEventListener('click', () => {
            html5QrCode.start(
                { facingMode: "environment" },
                { fps: 10, qrbox: { width: 250, height: 100 } },
                (decodedText) => { parseScanResult(decodedText); },
                (errorMessage) => {}
            ).then(() => {
                btnStart.style.display = 'none';
                actionBox.classList.remove('hidden');
            }).catch((err) => {
                alert("Gagal mengakses kamera. Pastikan koneksi HTTPS atau gunakan localhost.");
            });
        });

        btnStop.addEventListener('click', () => {
            if (html5QrCode && html5QrCode.isScanning) {
                html5QrCode.stop().then(() => {
                    btnStart.style.display = 'flex';
                    actionBox.classList.add('hidden');
                });
            }
        });
    });
</script>
{% endblock %}
'''

with codecs.open('templates/audit_rak.html', 'w', 'utf-8') as f:
    f.write(audit_content)

print("restored camera scanners")
