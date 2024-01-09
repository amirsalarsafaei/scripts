import requests
from tqdm import tqdm
import json

user_id = 0
private_token = ''
gitlab_host = ''

headers = {"PRIVATE-TOKEN": private_token}

authored_merge_requests = []

for page in tqdm(range(1, 10000)):
    resp = requests.get(f"https://{gitlab_host}/api/v4/merge_requests?page={page}&per_page=100&user_id={user_id}", headers=headers)
    try:
        resp.raise_for_status()
        resp_json = resp.json()
        if not resp_json or len(resp_json) == 0:
            break
        authored_merge_requests += resp_json
    except Exception:
        break


json.dump(authored_merge_requests, open("./authored_merge_requests.json", mode='w'), indent=4)
