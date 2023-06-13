CONFIG = {
    # Don't forget to remove the old database (flags.sqlite) before each competition.

    # The clients will run sploits on TEAMS and
    # fetch FLAG_FORMAT from sploits' stdout.
    'FLAG_FORMAT': r'[A-Z0-9]{31}=',
    'EXPLOIT_PATH': 'exploits',

    # This configures how and where to submit flags.
    # The protocol must be a module in protocols/ directory.

    'SYSTEM_PROTOCOL': 'ructf_tcp',
    'SYSTEM_HOST': '127.0.0.1',
    'SYSTEM_PORT': 31337,

    'SUBMIT_FLAG_LIMIT': 50,
    'SUBMIT_PERIOD': 5,
    'FLAG_LIFETIME': 5 * 60,

    # Password for the web interface. You can use it with any login.
    # This value will be excluded from the config before sending it to farm clients.
    'SERVER_PASSWORD': '1234',

    # Use authorization for API requests
    'ENABLE_API_AUTH': False,
    'API_TOKEN': '00000000000000000000'
}

def get_config():
    return CONFIG
