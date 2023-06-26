//import default_py from "../assets/code_templates/default.py";
//import randomFlags_py from "../assets/code_templates/random_flags.py";
//import web_py from "../assets/code_templates/web.py";

const default_py = `\
#!/usr/bin/env python3

`;

const randomFlags_py = `\
#!/usr/bin/env python3

import random
import string

for _ in range(10):
    print("".join(random.choice(string.ascii_uppercase) for _ in range(31)) + "=", flush=True)
`;

const web_py = `\
#!/usr/bin/env python3

import requests, sys, random, string, json
import faker
from fake_useragent import UserAgent

host = sys.argv[1]


def headers():
  # fake user_agent
  user_agent = UserAgent().random
  return {
      'User-Agent': user_agent,
  }


# get flagsid
flagids = requests.get('http://10.10.0.1:8081/flagIds').json()
flagids = flagids['CApp'][host]


for flagid in flagids:
    flagid = json.loads(flagid)

    # start a session
    s = requests.Session()

    # random user e psw
    username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(10, 16)))
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(10, 16)))
    # or
    fake = faker.Faker()
    username = fake.name()
    password = fake.password()

    # register request
    r = s.post(f"http://{host}:8080/api/users/register", json={
        "username": username,
        "password": password,
    }, headers=headers(), timeout=5)

    
    print('output', flush=True)

`;

export default {
    api_url: import.meta.env.VITE_API_URL,
    websocket_url: import.meta.env.VITE_API_URL + "/ws",
    // api_url: 'http://100.125.5.92:8000',
    // websocket_url: 'http://100.125.5.92:8000/ws',
    FLAG_WARNING_LIMIT: 10,
    TEAMS_WARNING_LIMIT: 1, // in %
    templates: [
        {
            "name": "Empty",
            "source": default_py
        },
        {
            "name": "Random",
            "source": randomFlags_py
        },
        {
            "name": "Web - Faker - Flagids",
            "source": web_py
        }
    ],
};