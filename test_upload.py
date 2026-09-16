import csv
import re
import sqlite3

def run():
    biblio_map = {}
    with open('senayan_biblio_export.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        headers = next(reader, None)
        for row in reader:
            if len(row) < 18: continue
            title = row[0]
            item_code_raw = row[17]
            codes = re.findall(r'<(.*?)>', item_code_raw)
            if not codes and item_code_raw.strip():
                codes = [item_code_raw.strip()]
            for code in codes:
                biblio_map[code] = {'title': title}
                
    print(f"Loaded {len(biblio_map)} biblios")
    
    count = 0
    with open('senayan_item_export.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        headers = next(reader, None)
        for row in reader:
            if len(row) < 10: continue
            count += 1
            
    print(f"Found {count} items")

run()
