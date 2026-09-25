import app
app.app.testing = True
with app.app.test_client() as client:
    # Test WITHOUT login - must return 401 JSON, not 302
    res = client.delete('/api/bibliografi/1')
    print("No session -> status:", res.status_code)
    print("No session -> body:", res.data.decode()[:100])
    print("No session -> content-type:", res.content_type)
