import requests
resp = requests.post('https://textbelt.com/text', {
  'phone': '256742067406',
  'message': 'Hello world',
  'key': 'textbelt',
})
print(resp.json())
