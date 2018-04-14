#!/usr/bin/env python

import os
from flask_script import Manager
from server import create_app

app = create_app(os.environ.get('CONFIG') or 'default')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
