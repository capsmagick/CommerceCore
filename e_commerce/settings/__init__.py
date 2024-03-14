def get_env():
    import os

    dir_name = os.path.dirname(__file__)
    path = os.path.join(dir_name, '.dj-env')
    if not os.path.exists(path):
        raise SystemExit(".dj-env is not present. Please create one.")

    fp = open(path)
    mode = fp.read().strip()
    fp.close()

    return mode


ENV = get_env()

print('THE ENVIRONMENT IS : ', ENV)

if ENV == 'dev' or ENV == 'development' or ENV == 'local':
    from .local import *

elif ENV == 'prod' or ENV == 'production':
    from .production import *


else:
    raise SystemExit("Invalid Application Environment")
