import app
app.app.testing = True
with app.app.test_client() as client:
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['role'] = 'admin'
    # Test DELETE with exact error trapping
    import traceback
    try:
        res = client.delete('/api/bibliografi/5000')
        print("Status:", res.status_code)
        print("Data:", res.data.decode())
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
