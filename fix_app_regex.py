import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Replace api_buku insert
insert_pattern = r"(INSERT OR REPLACE INTO buku \([\s\S]*?lokasi)\n(\s*\)\s*VALUES\s*\([\s\S]*?\?)\n(\s*\'\'\',\s*\([\s\S]*?data\.get\('lokasi', 'IMAVI'\))\n(\s*\))"
code = re.sub(insert_pattern, r"\1, is_reference_only\n\2, ?\n\3, 1 if str(data.get('is_reference_only', 'false')).lower() in ['true', '1'] else 0\n\4", code)

# Replace edit_koleksi update
update_pattern = r"(UPDATE buku SET[\s\S]*?huruf_judul=\?, lokasi=\?)\n(\s*WHERE id=\?\n\s*\'\'\',\s*\([\s\S]*?request\.form\.get\('lokasi'\)),\s*id\n(\s*\))"
code = re.sub(update_pattern, r"\1, is_reference_only=?\n\2, 1 if request.form.get('is_reference_only') else 0, id\n\3", code)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Regex updated app.py")
