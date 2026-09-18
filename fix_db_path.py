import codecs
import os

with codecs.open('database.py', 'r', 'utf-8') as f:
    code = f.read()

old_path = "DB_NAME = 'katalog.db'"
new_path = "DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'katalog.db')"

code = code.replace(old_path, new_path)

with codecs.open('database.py', 'w', 'utf-8') as f:
    f.write(code)
print("database.py updated.")
