from app import app
import sqlite3

# 1. Prepare data
conn = sqlite3.connect('katalog.db')
conn.execute("DELETE FROM sirkulasi WHERE no_induk = '8037/22'")
conn.execute("INSERT INTO sirkulasi (no_induk, member_id, loan_date, due_date, return_date) VALUES ('8037/22', '04920002', '2026-09-01 00:00:00', '2026-09-15 00:00:00', NULL)")
conn.commit()
conn.close()

# 2. Test request
app.config['TESTING'] = True
client = app.test_client()

with client.session_transaction() as sess:
    sess['logged_in'] = True
    sess['username'] = 'admin'

response = client.post('/api/sirkulasi/return', json={'book_id': '8037/22'})
print("Status:", response.status_code)
print("Data:", response.get_data(as_text=True))
