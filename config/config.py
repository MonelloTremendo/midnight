CONFIG = {
    'FLAG_FORMAT': r'[A-Z0-9]{31}=',
    'EXPLOIT_PATH': 'exploits',

    'SYSTEM_PROTOCOL': 'ructf_tcp',
    'SYSTEM_HOST': '127.0.0.1',
    'SYSTEM_PORT': 31337,

    'SUBMIT_FLAG_LIMIT': 50,
    'SUBMIT_PERIOD': 5,
    'FLAG_LIFETIME': 5 * 60,

    'SERVER_PASSWORD': '1234',

    'ENABLE_API_AUTH': False,
    'API_TOKEN': '00000000000000000000'
}

def get_config():
    return CONFIG
