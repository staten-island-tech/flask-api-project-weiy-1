import requests

response = requests.get("https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json")
datasomethingidk = response.json()
for datasomethingidk in datasomethingidk:
    print(datasomethingidk['atomicMass'])