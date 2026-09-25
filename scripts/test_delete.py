import app
app.app.testing = True
with app.app.test_client() as client:
    with client.session_transaction() as sess:
        sess['logged_in'] = True
    res = client.delete('/api/bibliografi/1')
    print(res.status_code, res.data)
