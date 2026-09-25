import app
app.app.testing = True
with app.app.test_client() as client:
    # Test DELETE without login - should get 401 JSON, not 302
    res = client.delete('/api/bibliografi/9999')
    print("No login:", res.status_code, res.data.decode()[:80])
    
    # Test with login
    with client.session_transaction() as sess:
        sess['logged_in'] = True
    res2 = client.delete('/api/bibliografi/9999')
    print("With login:", res2.status_code, res2.data.decode()[:80])
