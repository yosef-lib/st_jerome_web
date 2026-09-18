import json
with open('antrian_stiker.json', 'w') as f:
    json.dump([{
        "no_induk": "8132/22",
        "judul": "10 Agenda Pastoral Transformatif dan Kontekstual di Era Digital",
        "pengarang": "Yosef Paskah",
        "klasifikasi": "261.8",
        "cutter": "BAN",
        "huruf_judul": "a"
    }], f)

from template_stiker import generate_stiker_pdf
try:
    generate_stiker_pdf('antrian_stiker.json', 'stiker_output.pdf', options={'kartu': True, 'kantong': True})
    print("Success generating test PDF")
except Exception as e:
    import traceback
    traceback.print_exc()
