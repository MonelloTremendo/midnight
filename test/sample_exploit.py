#!/usr/bin/env python3

import random
import string

for _ in range(10):
    print("".join(random.choice(string.ascii_uppercase) for _ in range(31)) + "=", flush=True)