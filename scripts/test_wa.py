import requests
res = requests.post('http://127.0.0.1:5001/api/wa_webhook', json={
    'from': '6282257943768@c.us',
    'body': '2',
    'sender_name': 'Yosef'
})
print(res.status_code)
print(res.text)
