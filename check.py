import requests, json

with open("creds.json") as handle: creds = json.loads(handle.read())
#print(creds)

headers = {'Api-Key': creds['apiKey'],'Client-Key':creds['clientKey']}
req = requests.get('https://api.oneprovider.com/vm/locations', headers=headers)
#print(req.status_code)
#print(f"Got {req.text} as response")

response = req.json()
for region,data in response['response'].items():
    #print(region,data)
    for country in data:
        #print(country)
        #print(countryData)
        if country['country'] in creds['seek']:
            if country['available_sizes']:
                print(f"{country['country']} is available")
                if os.path.isfile(country['location_id']): continue
                #OneProvider has not always the cheapest package available in a certain location, so we try to buy the smallest one
                #1055 is debian 12 btw
                data = {"location_id": country['id'],"instance_size": min(country['available_sizes']),"template": "1055","hostname": "seek.code.run.com"}
                req = requests.post('https://api.oneprovider.com/vm/create', headers=headers, json=data)
                if req.status_code == 200:
                    with open(country['location_id'], 'w') as file: file.write(f"purchased package {min(country['available_sizes'])}")
            else:
                print(f"{country['country']} is not available")

