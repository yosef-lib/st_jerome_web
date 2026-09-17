import codecs

with codecs.open('templates/analitik_kunjungan.html', 'r', 'utf-8') as f:
    html = f.read()

# Add a Print button next to the filter form
old_form = '''<button type="submit" class="bg-primary text-white text-sm px-3 py-1 rounded hover:bg-opacity-90 transition"><i class="fa-solid fa-filter"></i> Filter</button>
        </form>'''
new_form = '''<button type="submit" class="bg-primary text-white text-sm px-3 py-1 rounded hover:bg-opacity-90 transition"><i class="fa-solid fa-filter"></i> Filter</button>
            <button type="button" onclick="window.print()" class="bg-slate-600 text-white text-sm px-3 py-1 rounded hover:bg-opacity-90 transition ml-2 print:hidden"><i class="fa-solid fa-print"></i> Cetak PDF</button>
        </form>'''
html = html.replace(old_form, new_form)

with codecs.open('templates/analitik_kunjungan.html', 'w', 'utf-8') as f:
    f.write(html)


# Add print CSS to layout.html
with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    layout = f.read()

# I will inject a <style> block right before </head>
print_style = '''
    <style>
        @media print {
            aside, header, nav, .print\:hidden {
                display: none !important;
            }
            .max-h-96 {
                max-height: none !important;
                overflow: visible !important;
            }
            .max-h-48 {
                max-height: none !important;
                overflow: visible !important;
            }
            body {
                background-color: white !important;
            }
            .bg-white {
                box-shadow: none !important;
                border: 1px solid #ddd !important;
            }
            main {
                padding: 0 !important;
                margin: 0 !important;
            }
        }
    </style>
</head>'''

layout = layout.replace('</head>', print_style)

with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(layout)

