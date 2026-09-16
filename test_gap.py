import sqlite3
import pandas as pd

conn = sqlite3.connect('katalog.db')

query = '''
SELECT 
    CASE 
        WHEN SUBSTR(klasifikasi, 1, 1) = '0' THEN '000 - Komputer & Informasi'
        WHEN SUBSTR(klasifikasi, 1, 1) = '1' THEN '100 - Filsafat & Psikologi'
        WHEN SUBSTR(klasifikasi, 1, 1) = '2' THEN '200 - Agama & Teologi'
        WHEN SUBSTR(klasifikasi, 1, 1) = '3' THEN '300 - Ilmu Sosial'
        WHEN SUBSTR(klasifikasi, 1, 1) = '4' THEN '400 - Bahasa'
        WHEN SUBSTR(klasifikasi, 1, 1) = '5' THEN '500 - Sains & Matematika'
        WHEN SUBSTR(klasifikasi, 1, 1) = '6' THEN '600 - Teknologi'
        WHEN SUBSTR(klasifikasi, 1, 1) = '7' THEN '700 - Kesenian & Rekreasi'
        WHEN SUBSTR(klasifikasi, 1, 1) = '8' THEN '800 - Sastra'
        WHEN SUBSTR(klasifikasi, 1, 1) = '9' THEN '900 - Sejarah & Geografi'
        ELSE 'Lainnya'
    END as ddc_group,
    MAX(tgl_terima) as update_terakhir,
    COUNT(no_induk) as jumlah_koleksi
FROM buku
WHERE lokasi = 'STPD' AND tgl_terima IS NOT NULL AND tgl_terima != ''
GROUP BY ddc_group
ORDER BY update_terakhir ASC
'''

try:
    df = pd.read_sql_query(query, conn)
    print(df)
except Exception as e:
    print("Error:", e)
