import codecs

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

old_barcode = '''                # --- DRAW BARCODE LABEL ---
                x_barcode = x_stiker + stiker_w + spine_gap
                y_barcode = y_base + (item_h - barcode_h) # Top-aligned
                
                # Draw outer border
                c.setStrokeColor(colors.black)
                c.setLineWidth(1.0)
                c.rect(x_barcode, y_barcode, barcode_w, barcode_h)
                
                # Header "PERPUSTAKAAN IMAVI"
                c.setFillColor(colors.black)
                c.setFont("Helvetica-Bold", 7)
                c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.4*cm, "PERPUSTAKAAN IMAVI")
                
                # Title (Truncated to 50 chars max)
                full_title = buku.get('judul', '')
                if len(full_title) > 50:
                    trunc_title = full_title[:47] + "..."
                else:
                    trunc_title = full_title
                c.setFont("Helvetica", 6.5)
                c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.8*cm, trunc_title)
                
                # Barcode Number
                barcode_val = buku.get('no_induk', '')
                c.setFont("Helvetica-Bold", 7.5)
                c.drawCentredString(x_barcode + barcode_w/2, y_barcode + 0.2*cm, barcode_val)
                
                # Barcode Graphic
                if barcode_val:
                    bw = 1.2
                    max_width = barcode_w - 0.4*cm
                    bc = code128.Code128(barcode_val, barHeight=1.1*cm, barWidth=bw)
                    while bc.width > max_width and bw > 0.2:
                        bw -= 0.05
                        bc = code128.Code128(barcode_val, barHeight=1.1*cm, barWidth=bw)
                    
                    bc_x = x_barcode + (barcode_w - bc.width)/2
                    bc_y = y_barcode + 0.6*cm
                    bc.drawOn(c, bc_x, bc_y)'''

new_barcode = '''                # --- DRAW BARCODE LABEL ---
                x_barcode = x_stiker + stiker_w + spine_gap
                y_barcode = y_base + (item_h - barcode_h) # Top-aligned
                
                # Header background
                header_h = 0.6 * cm
                c.setFillColorRGB(0.85, 0.85, 0.85)
                c.rect(x_barcode, y_barcode + barcode_h - header_h, barcode_w, header_h, fill=1, stroke=0)
                
                # Draw outer border and header line
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.5)
                c.rect(x_barcode, y_barcode, barcode_w, barcode_h)
                c.line(x_barcode, y_barcode + barcode_h - header_h, x_barcode + barcode_w, y_barcode + barcode_h - header_h)
                
                # Header "PERPUSTAKAAN IMAVI"
                c.setFillColor(colors.black)
                c.setFont("Helvetica-Bold", 7.5)
                c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.45*cm, "PERPUSTAKAAN IMAVI")
                
                # Title (Wrapped into 2 lines)
                full_title = buku.get('judul', '')
                trunc_title = full_title[:50]
                if len(trunc_title) > 25:
                    split_idx = trunc_title.rfind(' ', 0, 26)
                    if split_idx == -1: 
                        split_idx = 25
                    line1 = trunc_title[:split_idx].strip()
                    line2 = trunc_title[split_idx:].strip()
                    if len(full_title) > 50:
                        line2 += "..."
                else:
                    line1 = trunc_title
                    line2 = ""
                
                c.setFont("Helvetica", 6.5)
                c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.95*cm, line1)
                if line2:
                    c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 1.25*cm, line2)
                
                # Barcode Number
                barcode_val = buku.get('no_induk', '')
                c.setFont("Helvetica-Bold", 7.5)
                c.drawCentredString(x_barcode + barcode_w/2, y_barcode + 0.15*cm, barcode_val)
                
                # Barcode Graphic
                if barcode_val:
                    bw = 1.2
                    max_width = barcode_w - 0.4*cm
                    bc = code128.Code128(barcode_val, barHeight=1.2*cm, barWidth=bw)
                    while bc.width > max_width and bw > 0.2:
                        bw -= 0.05
                        bc = code128.Code128(barcode_val, barHeight=1.2*cm, barWidth=bw)
                    
                    bc_x = x_barcode + (barcode_w - bc.width)/2
                    bc_y = y_barcode + 0.45*cm
                    bc.drawOn(c, bc_x, bc_y)'''

code = code.replace(old_barcode, new_barcode)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)

print("success")
