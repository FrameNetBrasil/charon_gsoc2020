#activate_this = '/home/framenetbr/charon/flask/venv/bin/activate'
#with open(activate_this) as file_:
#    exec(file_.read(), dict(__file__=activate_this))

import sys

#sys.path.insert(0, '/home/framenetbr/.local/lib/python3.6/site-packages')
sys.path.insert(0, '/home/framenetbr/charon/public')
#from track_objects import app as application
from server import application
