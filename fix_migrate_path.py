import codecs
import os

with codecs.open('migrate_to_relational.py', 'r', 'utf-8') as f:
    code = f.read()

old_path = "conn = sqlite3.connect('katalog.db')"
new_path = "import os\n    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'katalog.db'))"

code = code.replace(old_path, new_path)

with codecs.open('migrate_to_relational.py', 'w', 'utf-8') as f:
    f.write(code)
print("migrate_to_relational.py updated.")
