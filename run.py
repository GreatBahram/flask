# run.py

import os

# local imports
from flask_todo import create_app

config_name = os.environ.get('FLASK_CONFIG', 'development')

app =  create_app(config_name)

if __name__ == "__main__":
    app.run()
