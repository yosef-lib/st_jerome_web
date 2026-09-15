import csv
import database
import io
from datetime import datetime

def generate_biblio_csv():
    conn = database.get_db_connection()
    buku_list = conn.execute('SELECT * FROM buku').fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    headers = [
        "Title", "GMD", "Edition", "ISBN/ISSN", "Publisher", "Publish Year", 
        "Collation", "Series Title", "Call Number", "Language", "Place", 
        "Classification", "Notes", "Image", "Attachment", "Author", "Subject", "Item Code"
    ]
    writer.writerow(headers)

    for buku in buku_list:
        call_number = f"{buku['klasifikasi']} {buku['cutter']} {buku['huruf_judul']}".strip()
        
        row = [
            buku['judul'],             
            buku['gmd'],               
            buku['edisi'],             
            buku['isbn'],              
            buku['penerbit'],          
            buku['tahun_terbit'],      
            buku['deskripsi_fisik'],   
            buku['judul_seri'],        
            call_number,               
            buku['bahasa'],            
            buku['tempat_terbit'],     
            buku['klasifikasi'],       
            buku['catatan'],           
            "",                        
            "",                        
            buku['pengarang'],         
            buku['subjek'],            
            buku['no_induk']           
        ]
        writer.writerow(row)
    
    return output.getvalue()

def generate_item_csv():
    conn = database.get_db_connection()
    buku_list = conn.execute('SELECT * FROM buku').fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # SLiMS Item Export Headers generally align with what the user pasted.
    # We will output without headers because the user's sample didn't have headers for item,
    # OR we can output standard headers. Let's output with standard headers to be safe for SLiMS import,
    # wait, the user said "seperti yg saya unduh tadi". Let's omit headers for Item if that's what SLiMS gave them.
    # Actually, SLiMS 9 Item CSV Export DOES have headers usually. Let's just put headers.
    headers = [
        "item_code", "call_number", "coll_type_name", "item_status_name", 
        "receipt_date", "supplier_name", "order_no", "location_name", 
        "invoice_date", "invoice_no", "fund_name", "price", "price_currency", 
        "add_date", "last_update", "title"
    ]
    writer.writerow(headers)

    for buku in buku_list:
        call_number = f"{buku['klasifikasi']} {buku['cutter']} {buku['huruf_judul']}".strip()
        today = datetime.now().strftime("%Y-%m-%d")
        tgl_terima = buku['tgl_terima'] if buku['tgl_terima'] else today
        
        row = [
            buku['no_induk'],          # item_code
            call_number,               # call_number
            "Textbook",                # coll_type_name
            "Available",               # item_status_name
            tgl_terima,                # receipt_date
            "",                        # supplier_name
            "",                        # order_no
            buku['lokasi'],            # location_name (STPD / IMAVI)
            tgl_terima,                # invoice_date
            "",                        # invoice_no
            "",                        # fund_name
            "0",                       # price
            "Rupiah",                  # price_currency
            tgl_terima,                # add_date
            today,                     # last_update
            buku['judul']              # title
        ]
        writer.writerow(row)
    
    return output.getvalue()
