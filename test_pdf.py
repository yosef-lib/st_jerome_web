from template_stiker import generate_stiker_pdf
import json
import os

buku_list = [
    {
        "id": 1,
        "judul": "Seri Dokumen Gerejawi No. 133; Perjalanan Katekumenat Menuju Hidup Perkawinan",
        "pengarang": "KWI",
        "no_induk": "0421/26",
        "klasifikasi": "262.91 DOK p"
    }
]

import tempfile
fd, temp_path = tempfile.mkstemp(suffix='.json')
with os.fdopen(fd, 'w') as f:
    json.dump(buku_list, f)

options = {'kartu': True, 'kantong': True}
generate_stiker_pdf(temp_path, "test_output.pdf", options)
print("PDF generated successfully")
