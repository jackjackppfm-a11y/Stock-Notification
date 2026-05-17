import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1505513729842876488/6-duu5eA62N4mX9r9dcfrNI9rABa-xVoLTpAODvrLMQ5TtLJpBhIE4eKWAAL4kBvvTko"

message = {
    "content": "good!!!"
}

response = requests.post(WEBHOOK_URL, json=message)

print(response.status_code)