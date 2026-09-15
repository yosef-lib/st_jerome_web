def cleanse_author(author_name):
    """
    Simulasi fungsi AI Agent (Hermes/Clario) untuk membersihkan dan 
    menyelaraskan nama pengarang yang tidak konsisten.
    """
    if not author_name:
        return ""
    
    # Dummy logika AI untuk Franz Magnis Suseno
    name_lower = author_name.lower()
    if "magnis" in name_lower and "suseno" in name_lower:
        return "F. Magnis Suseno"
    
    # Kapitalisasi standar sebagai fallback pembersihan
    return author_name.title()

def fix_call_number(klasifikasi, cutter, huruf_judul):
    """
    Simulasi AI Agent merekonstruksi elemen call number yang hilang/rusak.
    """
    fixed_k = klasifikasi.strip() if klasifikasi else "000"
    fixed_c = cutter.strip().upper() if cutter else "XXX"
    fixed_h = huruf_judul.strip().lower() if huruf_judul else "x"
    
    return fixed_k, fixed_c, fixed_h

def generate_narrative(total_koleksi, total_baca, pop_subject, deficit_subject, total_stpd, total_imavi, dominant_author, dominant_title):
    """
    Simulasi AI Agent (Hermes/Clario) menyusun narasi justifikasi evaluasi 
    semesteran untuk pimpinan dengan pemisahan lokasi.
    """
    narasi = (
        f"Laporan Analisis Koleksi & Strategi Pengadaan:\n\n"
        f"Berdasarkan analisis data riil, perpustakaan saat ini memiliki total {total_koleksi} eksemplar buku, "
        f"yang terdistribusi menjadi {total_stpd} koleksi di lokasi STPD dan {total_imavi} koleksi di lokasi IMAVI. "
        f"Keterbacaan in-house sejauh ini tercatat sebanyak {total_baca} aktivitas.\n\n"
        f"Klasifikasi dominan dan terpopuler saat ini berada di {pop_subject}, dengan pengarang terbanyak "
        f"adalah {dominant_author}. Judul buku yang paling mendominasi koleksi adalah '{dominant_title}'.\n\n"
        f"💡 Saran Strategis Kedepan:\n"
        f"1. Penyeimbangan Lokasi: Evaluasi kembali distribusi buku antara STPD dan IMAVI, pastikan "
        f"subjek-subjek fundamental terwakili secara merata di kedua lokasi.\n"
        f"2. Ekspansi Subjek: Kelas {deficit_subject} terdeteksi memiliki koleksi yang paling minim. "
        f"Sebaiknya anggaran pengadaan semester depan difokuskan untuk memperkaya literatur pada kelas ini.\n"
        f"3. Optimalisasi Keterbacaan: Mengingat angka in-house reading saat ini, disarankan untuk mengadakan program "
        f"bedah buku dari pengarang {dominant_author} guna menstimulasi minat baca mahasiswa."
    )
    return narasi
