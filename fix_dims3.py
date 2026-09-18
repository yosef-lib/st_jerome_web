import codecs, re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

# Fix Card Dimension
code = code.replace("'type': 'kartu', 'w': 8.0*cm, 'h': 13.1*cm", "'type': 'kartu', 'w': 8.6*cm, 'h': 13.1*cm")
code = code.replace("card_w = 8.0 * cm", "card_w = 8.6 * cm")

# Fix Kantong Dimension
# Old kantong component width was 10.5*cm, now needs to be 11.1*cm (9.1 main + 2 flaps)
code = code.replace("'type': 'kantong', 'w': 10.5*cm, 'h': 9.0*cm", "'type': 'kantong', 'w': 11.1*cm, 'h': 9.0*cm")

old_kantong_draw = '''    c.rect(x, y + 1*cm, 1*cm, 8*cm, fill=1) # left flap
    c.rect(x + 9.5*cm, y + 1*cm, 1*cm, 8*cm, fill=1) # right flap
    c.rect(x + 1*cm, y, 8.5*cm, 1*cm, fill=1) # bottom flap
    
    c.setFillColorRGB(0, 0, 0)
    
    # Main pocket Dashed
    c.setDash(6, 3)
    c.rect(x + 1*cm, y + 1*cm, 8.5*cm, 8*cm)
    c.setDash(1, 0) # reset
    
    # Header
    main_x = x + 1*cm
    main_y = y + 1*cm
    main_w = 8.5*cm'''

new_kantong_draw = '''    c.rect(x, y + 1*cm, 1*cm, 8*cm, fill=1) # left flap
    c.rect(x + 10.1*cm, y + 1*cm, 1*cm, 8*cm, fill=1) # right flap
    c.rect(x + 1*cm, y, 9.1*cm, 1*cm, fill=1) # bottom flap
    
    c.setFillColorRGB(0, 0, 0)
    
    # Main pocket Dashed
    c.setDash(6, 3)
    c.rect(x + 1*cm, y + 1*cm, 9.1*cm, 8*cm)
    c.setDash(1, 0) # reset
    
    # Header
    main_x = x + 1*cm
    main_y = y + 1*cm
    main_w = 9.1*cm'''

code = code.replace(old_kantong_draw, new_kantong_draw)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
