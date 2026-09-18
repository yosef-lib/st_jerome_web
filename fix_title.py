import codecs

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

old_logic = "    judul = buku.get('judul', '')\n    if len(judul) > 35:\n        judul = judul[:32] + '...'"

new_logic = '''    judul = buku.get('judul', '')
    
    # Reformat "Seri Dokumen Gerejawi" 
    if "Seri Dokumen Gerejawi" in judul and (";" in judul or ":" in judul or "-" in judul):
        # find the delimiter
        import re
        parts = re.split(r'[;:\-]', judul, maxsplit=1)
        if len(parts) >= 2:
            series_part = parts[0].strip()
            title_part = parts[1].strip()
            # If the series part is the one containing "Seri Dokumen"
            if "Seri Dokumen" in series_part:
                series_part = series_part.replace("Seri Dokumen Gerejawi", "SDG")
                judul = f"{title_part} ({series_part})"
            
    if len(judul) > 50:
        judul = judul[:47] + '...'
'''

code = code.replace(old_logic, new_logic)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
print("Title truncation fixed")
