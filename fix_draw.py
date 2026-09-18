import codecs, re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

pattern = r"if comp\['type'\] == 'identitas':.*?current_x \+= comp\['w'\] \+ gap_x"
new_draw = '''if comp['type'] == 'identitas':
                        draw_identitas(c, current_x, y_base, item_h, buku)
                    elif comp['type'] == 'punggung':
                        draw_punggung(c, current_x, y_base, item_h, buku)
                    elif comp['type'] == 'barcode':
                        draw_barcode(c, current_x, y_base, item_h, buku)
                    elif comp['type'] == 'kartu':
                        draw_kartu_buku(c, current_x, y_base + item_h - comp['h'], buku)
                    elif comp['type'] == 'kantong':
                        draw_kantong_buku(c, current_x, y_base + item_h - comp['h'])
                    
                    current_x += comp['w'] + gap_x'''

code, count = re.subn(pattern, new_draw, code, flags=re.DOTALL)
print(f"Replaced {count} times")

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
