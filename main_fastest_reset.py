import worker
from __builtins__ import *

scenarios = [
    (Unlocks.Speed, 0),  # Hay: 20
    (Unlocks.Expand, 0),  # Hay: 30
    (Unlocks.Plant, 0),  # Hay: 50
    (Unlocks.Speed, 1),  # Wood: 20
    (Unlocks.Expand, 1),  # Wood: 20
    (Unlocks.Carrots, 0),  # Wood: 50
    (Unlocks.Expand, 2),  # Wood: 30, Carrot: 20
    (Unlocks.Trees, 0),  # Wood: 50, Carrot: 70
    (Unlocks.Watering, 0),  # Wood: 50
]


def prod_hay(num_needed):
    w, h = get_world_size(), get_world_size()
    current = num_items(Items.Hay)
    while (num_items(Items.Hay) - current) < num_needed:
        worker.update_primitives_mt(0, 0, w, h, Grounds.Grassland, Entities.Grass)


def prod_wood(num_needed):
    w, h = get_world_size(), get_world_size()
    entity = Entities.Bush
    if num_unlocked(Unlocks.Trees) > 0:
        entity = Entities.Tree

    current = num_items(Items.Wood)
    while (num_items(Items.Wood) - current) < num_needed:
        worker.update_primitives_mt(0, 0, w, h, Grounds.Soil, entity)


def prod_carrots(num_needed):
    w, h = get_world_size(), get_world_size()
    # carrot production need hay and wood first
    prod_hay(num_needed)
    prod_wood(num_needed)
    current = num_items(Items.Carrot)
    while (num_items(Items.Carrot) - current) < num_needed:
        worker.update_primitives_mt(0, 0, w, h, Grounds.Soil, Entities.Carrot)


prod_table = {
    Items.Hay: prod_hay,
    Items.Wood: prod_wood,
    Items.Carrot: prod_carrots,
}


for unlock_target, level in scenarios:
    costs = get_cost(unlock_target, level)
    quick_print("Unlock:", unlock_target, "\tLevel:", level, "\tCosts:", costs)

    for key in costs:
        amount = costs[key]
        prod_table[key](amount)
    if not unlock(unlock_target):
        quick_print("Failed to unlock:", unlock_target, "Level:", level)
        break

while True:
    do_a_flip()  # just to keep the program running
    pass
