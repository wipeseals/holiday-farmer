import util
from __builtins__ import *

clear()

width = get_world_size()
height = get_world_size()
while True:
    util.update_pumpkin(0, 0, width, height)
