WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Added following for facebook and twitter login.
#OAUTH_CREDENTIALS = {
#    'facebook': {
#        'id': '960211174038529',
#        'secret': '8f091b402e2892606839b4cdcdc6b21a'
#    }
#}