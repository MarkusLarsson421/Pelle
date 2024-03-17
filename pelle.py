import json
import requests

parameters = {
    "id": "bs_sage",
}

status = {
    "map_name": "",
    "players": -1,
    "round_duration": -1,
    "security_level": "",
    "shuttle_mode": "",
    "shuttle_timer": -1,
    "round_id": -1,
    "gamestate": -1,
    "admins": -1,
}

json_data = "Empty."
old_round_id:int = status["round_id"]


def update_api():
    print("Updating API...")
    response = requests.get("https://api.beestation13.com/stats/bs_sage", params=parameters)
    print(f"Response code: {response.status_code}.")
    response.raise_for_status()
    if response.status_code != 204:
        global json_data, old_round_id
        json_data = response.json()
        for x in status.keys():
            status[x] = json_data[x]
        if old_round_id == -1:
            old_round_id = status["round_id"]
    print(f"Update completed.")


def check_for_new_round():
    global old_round_id
    result:bool = status["round_id"] == old_round_id
    r_id = status["round_id"]
    print(f"Result: {result}\n"
          f"Round ID: {r_id}\n"
          f"Old round ID: {old_round_id}")
    if not result:
        old_round_id = status["round_id"]
        return True
    return False


def get_status():
    print(get_json())
    return status


def get_json():
    return json.dumps(json_data, sort_keys=True, indent=4)


def next_round():
    global old_round_id
    old_round_id += 1
