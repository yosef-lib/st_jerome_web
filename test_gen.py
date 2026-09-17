from template_stiker import generate_stiker_pdf
# generate default
generate_stiker_pdf('antrian_stiker.json', 'stiker_all.pdf')

# generate barcode only
generate_stiker_pdf('antrian_stiker.json', 'stiker_barcode_only.pdf', {'barcode': True})
