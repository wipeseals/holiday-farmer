from __builtins__ import *  # noqa: F403

import util


clear()

width = get_world_size()
height = get_world_size()

size = width // 2
util.spawn_update_primitives(0, size, size, size, 8)


def main1():
    while True:
        util.update_pumpkin_mt(size, 0, size, size)


def main2():
    while True:
        util.update_cactus_mt(size, size, size, size)


spawn_drone(main1)
spawn_drone(main2)

do_a_flip()
do_a_flip()
do_a_flip()
do_a_flip()
do_a_flip()
while True:
    util.update_maze(0, 0, size, size)
