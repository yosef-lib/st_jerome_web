import codecs

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

# Replace head with correct Tailwind and fonts
new_head = '''<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buku Tamu - St. Jerome Library Assistant</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              boxdark: '#3E2723',
              boxdark2: '#4E342E',
              bodydark: '#A1887F',
              bodydark2: '#A1887F',
              primary: '#6D4C41',
              secondary: '#8D6E63',
              stroke: '#E2E8F0',
              danger: '#E53935',
              success: '#43A047',
              warning: '#F57C00',
              'gray-2': '#F8FAFC',
            },
            fontFamily: {
              satoshi: ['Inter', 'sans-serif'],
            },
          }
        }
      }
    </script>
    <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .kiosk-bg {
            background-color: #F3E5F5;
            background-image: radial-gradient(#6D4C41 0.5px, transparent 0.5px), radial-gradient(#6D4C41 0.5px, #F3E5F5 0.5px);
            background-size: 20px 20px;
            background-position: 0 0, 10px 10px;
            background-opacity: 0.1;
        }
        .no-scrollbar::-webkit-scrollbar { display: none; }
    </style>
</head>'''

import re
html = re.sub(r'<head>.*?</head>', new_head, html, flags=re.DOTALL)

# Fix logo
old_logo = '''<img src="{{ url_for('static', filename='images/logo.png') }}" onerror="this.src='https://ui-avatars.com/api/?name=St+Jerome&background=fff&color=1e293b'" alt="Logo" class="w-14 h-14 object-contain">'''
new_logo = '''<img src="{{ url_for('static', filename='img/logo_imavi.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="IMAVI Logo" class="w-16 h-16 object-contain">'''
html = html.replace(old_logo, new_logo)

# Update the left side layout to match St Jerome theme better
old_left = '''<div class="md:w-5/12 bg-primary p-8 md:p-12 text-white flex flex-col justify-between">
            <div>
                <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center mb-6 shadow-inner">
                    <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="IMAVI Logo" class="w-16 h-16 object-contain">
                </div>
                <h1 class="text-3xl font-bold mb-4 leading-tight">Buku Tamu Perpustakaan</h1>
                <p class="text-primary-light text-lg mb-8 opacity-90">Silakan scan Kartu Anggota Anda atau isi form buku tamu jika Anda bukan anggota tetap.</p>
            </div>
            <div class="mt-auto">
                <p class="text-sm opacity-70">St. Jerome Library Assistant</p>
            </div>
        </div>'''

new_left = '''<div class="md:w-5/12 bg-boxdark p-8 md:p-12 text-white flex flex-col justify-between relative overflow-hidden">
            <!-- Decorative circle -->
            <div class="absolute -top-24 -left-24 w-64 h-64 rounded-full bg-primary opacity-50 blur-3xl"></div>
            <div class="absolute -bottom-24 -right-24 w-64 h-64 rounded-full bg-primary opacity-50 blur-3xl"></div>
            
            <div class="relative z-10">
                <div class="w-24 h-24 bg-white rounded-full flex items-center justify-center mb-6 shadow-lg border-4 border-primary">
                    <img src="{{ url_for('static', filename='img/logo_imavi.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="IMAVI Logo" class="w-16 h-16 object-contain">
                </div>
                <h1 class="text-4xl font-bold mb-4 leading-tight tracking-tight">Buku Tamu<br>IMAVI</h1>
                <p class="text-bodydark text-lg mb-8 font-medium">Silakan pindai Kartu Anggota Anda atau isi form buku tamu jika Anda bukan anggota tetap (tamu).</p>
            </div>
            <div class="mt-auto relative z-10 flex items-center gap-3">
                <i class="fa-solid fa-book-open-reader text-2xl text-bodydark"></i>
                <div>
                    <p class="text-sm font-bold text-white tracking-wide">ST. JEROME</p>
                    <p class="text-xs text-bodydark">Library Assistant</p>
                </div>
            </div>
        </div>'''

html = html.replace(old_left, new_left)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)

print("Kiosk HTML fixed")
