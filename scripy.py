import requests
import json
from actions import actions_str

users_url = 'https://rem.dbwebb.se/api/users'
session = requests.Session()

def handle_request_status(code: int, action: dict):
    if code == 200:
        print(f'Success: {action["s"]}')
    else:
        print(f'Error: failed to {action["e"]}')

def get_users(url: str):
    users = session.get(url)
    return json.loads(users.content)['data']

def delete_user_api(id: int):
    request = session.delete(f"{users_url}/{id}")
    handle_request_status(request.status_code, { 's': 'user deleted', 'e': 'delete user' })

def add_user_api(dict):
    request = session.post(users_url, json=dict)
    handle_request_status(request.status_code, { 's': 'user added', 'e':'add user' })


def update_user_api(dict, user_id: int):
    request = session.put(f"{users_url}/{user_id}", json=dict)
    handle_request_status(request.status_code, { 's': 'user updated', 'e': 'update user' } )

def get_valid_user_id(action: str):
    users = get_users(users_url)
    user_id = None

    while True:
        user_input = input(f'Enter the id of the user to {action}, or "quit" to go back: ')
        try:
            user_id = int(user_input)
        except ValueError:
            pass

        if user_id in [user['id'] for user in users]:
            break
        elif user_input == "quit":
            return None
    return user_id


def get_user_details():
    data = get_users(users_url)
    print('users:')
    for user in data:
        print(f"{user['id']}: {user['firstName']} {user['lastName']}")

    return data

def delete_user():
    user_id = get_valid_user_id('delete')
    delete_user_api(user_id)


def input_user_name():
    inputs = ['firstName', 'lastName']
    user_dict = {}
    for attr in inputs:
        while True:
            user_dict[attr] = input(f'Enter the {attr}: ')

            if len(user_dict[attr]) > 0:
                break
    return user_dict



def add_user():
    user_dict = input_user_name()
    add_user_api(user_dict)

def update_user():
    user_id = get_valid_user_id('update')
    if user_id:
        user_dict = input_user_name()
        update_user_api(user_dict, user_id)


def get_action():
    action_map = {
        '1': get_user_details,
        '2': delete_user,
        '3': add_user,
        '4': update_user
    }

    while True:
        action = input(actions_str)

        if str(action) in action_map.keys():
            action_map[action]()
        elif action == "quit":
            break
def main():
    get_action()


main()