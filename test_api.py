import requests
import json
url = 'https://www.googleapis.com/books/v1/volumes?q=intitle:"Kitab Hukum Kanonik"'
res = requests.get(url)
print(res.status_code)
if res.status_code == 200:
    data = res.json()
    items = data.get('items', [])
    if items:
        vol = items[0].get('volumeInfo', {})
        print("Title:", vol.get('title'))
        print("Image:", vol.get('imageLinks', {}).get('thumbnail'))
