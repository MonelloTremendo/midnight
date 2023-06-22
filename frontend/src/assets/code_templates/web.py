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
