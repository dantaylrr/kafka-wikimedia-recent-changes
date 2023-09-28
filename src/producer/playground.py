import json

with open('/Users/daniel.taylor/github-projects/kafka-wikimedia-recent-changes/tests/events/event.json', 'rb') as f:
    content = json.loads(f.read())

print(content)