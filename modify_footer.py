import codecs
import re

with codecs.open('templates/kiosk.html', 'r', 'utf-8') as f:
    html = f.read()

old_footer = '''<div class="mt-auto relative z-10 flex items-center justify-center gap-3 border-t border-bodydark/30 pt-4">
                <img src="{{ url_for('static', filename='images/logo.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="SJLA" class="w-10 h-10 object-contain bg-white rounded-full border border-stroke">
                <div class="text-left">
                    <p class="text-sm font-bold text-white tracking-wide">ST. JEROME</p>
                    <p class="text-xs text-bodydark">Library Assistant</p>
                </div>
            </div>'''

new_footer = '''<div class="mt-auto relative z-10 flex items-center justify-start gap-3 border-t border-bodydark/30 pt-4">
                <div class="w-10 h-10 rounded-full overflow-hidden border-2 border-white/20 shrink-0">
                    <img src="{{ url_for('static', filename='images/logo.png') }}" onerror="this.src='{{ url_for('static', filename='img/logo.jpg') }}'" alt="SJLA" class="w-full h-full object-cover">
                </div>
                <div class="text-left">
                    <p class="text-sm font-bold text-white tracking-wide">ST. JEROME</p>
                    <p class="text-xs text-bodydark">Library Assistant</p>
                </div>
            </div>'''

html = html.replace(old_footer, new_footer)

with codecs.open('templates/kiosk.html', 'w', 'utf-8') as f:
    f.write(html)
