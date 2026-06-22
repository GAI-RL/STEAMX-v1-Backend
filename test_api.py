import urllib.request
import json

req = urllib.request.Request(
    'http://localhost:8002/api/feedback/contact', 
    data=json.dumps({
        'first_name': 'Test', 
        'last_name': 'User', 
        'email': 'test@test.com', 
        'topic': 'General Inquiry', 
        'message': 'Hello'
    }).encode(), 
    headers={'Content-Type': 'application/json'}
)

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode())
except urllib.error.HTTPError as e:
    print(e.read().decode())
