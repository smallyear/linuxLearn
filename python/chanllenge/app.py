import os
from flask import Flask
import json

def create_app():

    app = Flask('rmon')

    file = os.environ.get('RMON_CONFIG')

    configs = ''

    with open(file) as f:
        for config in f:
            config = config.strip()
            if config.startswith('#'):
                continue
            else:
                configs += config
    data = json.loads(configs)

    for key in data:
        app.config[key.upper()] = data.get(key)

    return app

    return app
