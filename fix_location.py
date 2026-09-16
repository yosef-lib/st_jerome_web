import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

old_loc = "lokasi = 'IMAVI' if 'IMAVI' in lokasi_raw else lokasi_raw"
new_loc = "lokasi = 'IMAVI' if 'IMAVI' in lokasi_raw else ('STPD' if 'STPD' in lokasi_raw else 'UMUM')"

app_code = app_code.replace(old_loc, new_loc)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("Location logic fixed")
