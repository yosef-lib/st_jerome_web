from template_stiker import generate_stiker_pdf
try:
    generate_stiker_pdf('antrian_stiker.json', 'stiker_output.pdf')
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
