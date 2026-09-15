import database
import csv
import io

raw_biblio = """Title,GMD,Edition,ISBN/ISSN,Publisher,Publish Year,Collation,Series Title,Call Number,Language,Place,Classification,Notes,Image,Attachment,Author,Subject,Item Code
"sswswswdwdwdwdwdw","Text","","979-3739-34-7","kanisius","1965","187hlm;17.5x11cm","","100 BAS w","Indonesia","Yogyakarta","100 BAS w","","","","<Soelistyo, Basuki>","<filsafat barat-sejarah>","<0001/25>"
"Meneladan Bunda Maria Dalam Melakukan Panca Tugas Gereja","E-book","","","Komisi Anak Keuskpan Surabaya","2026","","","264 KEU  m","Indonesia","Surabaya","264 KEU  m","","cover_meneladan-bunda-maria-dalam-melakukan-panca-tugas-gereja-20260511130207.jpg","","<Komisi Anak Keuskupan Surabaya>","","<0016/26>"
"Novena Pentakosta 2026 Tema; Roh Kudus Menjadi Dasar Kedewasaan Iman Umat Allah","Text","","","","2026","88 Halaman","","264 KEU n","Indonesia","Surabaya","264 KEU n","","cover_novena-pentakosta-2026-tema-roh-kudus-menjadi-dasar-kedewasaan-iman-u-20260511123647.jpg","","<Komisi Liturgi Keuskupan Surabaya>","","<0015/26>"
"Humanae Vitae (Kehidupan Manusia)","E-book","","","Dokpen KWI","1968","37 Halaman","","200 PAU h","Indonesia","Jakarta","200 PAU h","","cover_humanae-vitae-kehidupan-manusia-20260511110917.jpg","","<Paus Paulus VI>","","<0013/26>"
"Perayaan Paskah dan Persiapannya [Judul asli:Litterae Circulares de Festis Paschalibus Praeparandis et Celebrandis]","E-book","","","","","42 hlm","","","Indonesia","Jakarta","","","cover_perayaan-paskah-dan-persiapannya-judul-asli-litterae-circulares-de-fe-20260511122302.jpg","","<Go, Piet (ptj)><Congregatio pro Cultu Divino>","","<0014/26>"
"Ekologi Integral Dalam Kehidupan Keluarga","E-book","","","Departemen Dokumentasi dan Penerangan  Konferensi Waligereaja Indonesia","","86 hlm","","200 EKO e","Indonesia","Jakarta","200 EKO e","","cover_ekologi-integral-dalam-kehidupan-keluarga-20260511105137.jpg","","<Dikasteri untuk Awam, Keluarga dan Kehidupan><Purwono, Antonius>","","<0012/26>"
"A history of Philosophy; Logical Positivism and Existentialism Volume 11","Text","Vol. 1 Cet. 15","978-0-8264-6905-2","Bloomsbury","2019","ix, 230 hlm.; 13.7 cm x 21.6 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-logical-positivism-and-existentialism-volume-20260511103206.jpg","","<Copleston, Frederick>","","<0011/26>"
"A History  Of Philosophy; Russian Philosophy Volume 10","Text","Vol. 10 Cet. 11","978-0-8264-6904-5","Bloomsbury","2019","x, 445 hlm.13.7 cm x 21.6 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-russian-philosophy-volume-10-20260511102616.jpg","","<Copleston, Frederick>","","<0010/26>"
"A History Of Philosophy ; 19 and 20 th century French Philosophy  Volume 9","Text","Vol. 9 Cet. 11","978-0-8264-6903-8","Bloomsbury","2015","xvii, 480 hlm.; 13.8 cm x 21.6 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-19-and-20-th-century-french-philosophy-volu-20260511101936.jpg","","<Copleston, Frederick>","","<0009/26>"
"A History of Philosophy; Utilitarianism to early analytic philosophy Volume 8","Text","Vol. 8 Cet. 11","978-0-8264-6902-1","Bloomsbury","2019","xiii, 577 hlm.; 13.7 cm x 21.5 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-utilitarianism-to-early-analytic-philosophy-v-20260511101518.jpg","","<Copleston, Frederick>","","<0008/26>"
"A History of Philosophy; 18th and 19 th Century German Philosophy Volume 7","Text","Vol. 7, Cet. 2019","978-0-8264-6901-4","Bloomsbury","2019","xi, 496 hlm.; 13.7 cm x 21.6 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-18th-and-19-th-century-german-philosophy-volu-20260511100624.jpg","","<Copleston, Frederick>","","<0007/26>"
"A History Of Philosophy ; The Enlightenment Voltaire to Kant Volume 6","Text","Vol. 6 Cet. 10","978-0-8264-6900-7","Bloomsbury","1960","ix, 509 hlm;13.9 cm x 21.5 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-the-enlightenment-voltaire-to-kant-volume-6-20260511100119.jpg","","<Copleston, Frederick>","","<0006/26>"
"A History Of Philosophy; British Philosophy Hobes to Hume Volume 5","Text","Vol 5, Cet. 12","978-0-8264-6899-4","Bloomsbury","2013","viii, 440 hlm;13.7 cm x 21.6 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-british-philosophy-hobes-to-hume-volume-5-20260511094718.jpg","","<Copleston, Frederick>","","<0005/26>"
"A History Of Philosophy; the rationalist descartes to leibniz Volume 4","Text","Vol. 4 Cet. 13","978-0-8264-6898-7","Bloomsbury","2019","xi, 370 hlm.;13.7 cm x 21.6 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-the-rationalist-descartes-to-leibniz-volume-4-20260511093722.jpg","","<Copleston, Frederick>","","<0004/26>"
"A History of Philosophy; late medieval and renassance philosophy Volume 3","Text","Vol. 3 Cet. 13","978-0-8264-6897-0","Bloomsbury","2019","","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-late-medieval-and-renassance-philosophy-volum-20260511085755.jpg","","<Copleston, Frederick>","","<0003/26>"
"A History Of Philosophy ; Medieval Philosophy  Volume 2","Text","Vol. 2 Cet. 11","978-0-8264-6896-3","Bloomsbury","2019","x, 614 hlm.; 13.7 x 21 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-medieval-philosophy-volume-2-20260511085314.jpg","","<Copleston, Frederick>","","<0002/26>"
"A History Of  Philosophy : Greece And Rome  Volume 1","Text","Vol. 1 Cet. 11","978-0-8264-6895-6","Bloomsbury","1946","x, 521 hlm.; 13.9 x 21.5 cm","","190 COP a","English","London","190 COP a","","cover_a-history-of-philosophy-greece-and-rome-volume-1-20260511083859.jpg","","<Copleston, Frederick>","<Philosophy><Greece><ROME>","<0001/26>"
"""

conn = database.get_db_connection()
stream = io.StringIO(raw_biblio.strip())
reader = csv.DictReader(stream)
for row in reader:
    item_code = row.get('Item Code', '').strip('<>')
    title = row.get('Title', '')
    author = row.get('Author', '').strip('<>')
    
    # Asumsi lokasi, default STPD jika tidak disebutkan
    lokasi = "STPD"
    
    try:
        conn.execute('''
            INSERT INTO buku (no_induk, judul, pengarang, lokasi, status_buku, gmd, edisi, isbn, penerbit, tahun_terbit, deskripsi_fisik, bahasa, tempat_terbit, klasifikasi)
            VALUES (?, ?, ?, ?, 'SLIMS_IMPORT', ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item_code, title, author, lokasi,
            row.get('GMD'), row.get('Edition'), row.get('ISBN/ISSN'), row.get('Publisher'), row.get('Publish Year'),
            row.get('Collation'), row.get('Language'), row.get('Place'), row.get('Classification')
        ))
    except Exception as e:
        print(f"Error inserting {item_code}: {e}")

conn.commit()
conn.close()
print("Data seeded successfully.")
