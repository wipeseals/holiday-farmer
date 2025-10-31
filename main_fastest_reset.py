import worker
from __builtins__ import *

scenarios = [
    (Unlocks.Speed, 0),
    (Unlocks.Speed, 1),
    (Unlocks.Speed, 2),
    (Unlocks.Speed, 3),
]


def prod_hay(num_needed):
    w, h = get_world_size(), get_world_size()
    prod_per_iter = w * h
    num_iters = (num_needed + prod_per_iter - 1) // prod_per_iter

    for _ in range(num_iters):
        worker.update_primitives_mt(0, 0, w, h, Grounds.Grassland, Entities.Grass)


prod_table = {
    Items.Hay: prod_hay,
}


for unlock_target, level in scenarios:
    costs = get_cost(unlock_target, level)
    quick_print("Unlock:", unlock_target, "Level:", level, "Costs:", costs)

    for key in costs:
        amount = costs[key]
        prod_table[key](amount)
    unlock(unlock_target)

while True:
    pass
