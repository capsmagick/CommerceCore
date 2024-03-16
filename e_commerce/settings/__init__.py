from .utils import get_env


ENV = get_env()

print('THE ENVIRONMENT IS : ', ENV)

if ENV == 'dev' or ENV == 'development' or ENV == 'local':
    from .local import *

elif ENV == 'prod' or ENV == 'production':
    from .production import *


else:
    raise SystemExit("Invalid Application Environment")
