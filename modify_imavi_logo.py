import codecs
import re

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

# Fix IMAVI logo
old_imavi = '''<div class="w-28 h-28 bg-white rounded-full flex items-center justify-center mb-6 shadow-lg border-4 border-primary mx-auto">
                    <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="IMAVI Logo" class="w-20 h-20 object-contain">
                </div>'''
new_imavi = '''<div class="w-28 h-28 bg-white rounded-full flex items-center justify-center mb-6 shadow-lg border-4 border-primary mx-auto overflow-hidden">
                    <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="IMAVI Logo" class="w-full h-full object-cover">
                </div>'''
html = html.replace(old_imavi, new_imavi)

# Remove Kirim button
old_btn = '''<button onclick="submitMember()" class="absolute right-2 top-2 bottom-2 rounded-lg bg-primary px-6 font-bold text-white hover:bg-opacity-90 transition">Kirim</button>'''
html = html.replace(old_btn, '')

# Change input logic to auto-submit on input with debounce
# Also remove onkeypress
old_input = '''<input type="text" id="memberIdInput" autofocus placeholder="Arahkan kursor kesini dan Scan Barcode..." onkeypress="if(event.key === 'Enter') submitMember()" class="w-full rounded-xl border-2 border-stroke bg-gray-50 py-5 pl-14 pr-24 outline-none transition focus:border-primary focus:bg-white text-lg font-semibold">'''
new_input = '''<input type="text" id="memberIdInput" autofocus placeholder="Arahkan kursor kesini dan Scan Barcode..." class="w-full rounded-xl border-2 border-stroke bg-gray-50 py-5 pl-14 pr-8 outline-none transition focus:border-primary focus:bg-white text-lg font-semibold">'''
html = html.replace(old_input, new_input)

# Add JS debounce for barcode
js_append = '''
        let barcodeTimer;
        document.getElementById('memberIdInput').addEventListener('input', function() {
            clearTimeout(barcodeTimer);
            if(this.value.trim().length > 0) {
                barcodeTimer = setTimeout(() => {
                    submitMember();
                }, 300); // 300ms after last character is typed by scanner
            }
        });
        
        // Still keep Enter key support just in case
        document.getElementById('memberIdInput').addEventListener('keypress', function(e) {
            if(e.key === 'Enter') {
                clearTimeout(barcodeTimer);
                e.preventDefault();
                submitMember();
            }
        });
'''
html = html.replace('// Ensure clicking anywhere', js_append + '\n        // Ensure clicking anywhere')

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)
