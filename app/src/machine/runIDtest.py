
import requests

url = "http://cloud.formula-kart.org/api/machine/v1/runs"
body = {"machine_id": 1, "start_at": "2024-04-04T16:42:43.717Z"}

run = requests.post(url, json=body)
runId = run.json()["run"]["id"]
print(runId)
