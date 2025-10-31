import worker
from __builtins__ import *

scenarios = [
    # startup
    (Unlocks.Speed, 0),  # Hay: 20
    (Unlocks.Expand, 0),  # Hay: 30
    (Unlocks.Plant, 0),  # Hay: 50
    (Unlocks.Speed, 1),  # Wood: 20
    (Unlocks.Expand, 1),  # Wood: 20
    (Unlocks.Carrots, 0),  # Wood: 50
    (Unlocks.Expand, 2),  # Wood: 30, Carrot: 20
    (Unlocks.Trees, 0),  # Wood: 50, Carrot: 70
    (Unlocks.Watering, 0),  # Wood: 50
    (Unlocks.Speed, 2),  # Wood: 50, Carrot: 50
    (Unlocks.Expand, 3),  # Wood: 100, Carrot: 50
    (Unlocks.Grass, 1),  # Hay: 300
    (Unlocks.Trees, 1),  # Hay: 300
    (Unlocks.Grass, 2),  # Wood: 500
    (Unlocks.Trees, 2),  # Hay: 1.2k
    (Unlocks.Trees, 3),  # Hay: 4.8k
    (Unlocks.Carrots, 1),  # Wood: 250
    (Unlocks.Speed, 3),  # Carrot: 500
    (Unlocks.Watering, 2),  # Wood: 250
    # use fertilizer faster
    (Unlocks.Fertilizer, 0),  # Wood: 500
    (Unlocks.Watering, 3),  # Wood: 500
    (Unlocks.Carrots, 2),  # Wood: 1.25k
    (Unlocks.Fertilizer, 1),  # Wood: 1.5k
    (Unlocks.Pumpkins, 0),  # Wood: 500, Carrot: 200
    (Unlocks.Pumpkins, 1),  # Carrot: 1k
    (Unlocks.Expand, 4),  # Pumpkin: 1k
    (Unlocks.Speed, 4),  # Carrot: 1k
    (Unlocks.Grass, 3),  # Wood: 2.5k
    (Unlocks.Watering, 4),  # Wood: 3.2k
    (Unlocks.Carrots, 3),  # Wood: 6.25k
    (Unlocks.Pumpkins, 2),  # Carrot: 4k
    (Unlocks.Fertilizer, 2),  # Wood: 9k
    (Unlocks.Expand, 5),  # Pumpkin: 8k
    (Unlocks.Trees, 4),  # Hay: 19.2k
    (Unlocks.Grass, 4),  # Wood: 12.5k
    (Unlocks.Trees, 5),  # Hay: 76.8k
    (Unlocks.Grass, 5),  # Wood: 62.5k
    (Unlocks.Fertilizer, 3),  # Wood: 64k
    (Unlocks.Carrots, 4),  # Wood: 31.2k
    # unlock megafarm
    (Unlocks.Mazes, 0),  # Weird_Substance: 1k
    (Unlocks.Cactus, 0),  # Pumpkin: 5k
    (Unlocks.Mazes, 1),  # Cactus: 12k
    (Unlocks.Pumpkins, 3),  # Carrot: 16k
    (Unlocks.Cactus, 1),  # Pumpkin: 20k
    (Unlocks.Pumpkins, 4),  # Carrot: 64k
    (Unlocks.Megafarm, 0),  # Gold: 2k
    (Unlocks.Megafarm, 1),  # Gold: 8k
    (Unlocks.Trees, 6),  # Hay: 307k
    (Unlocks.Grass, 6),  # Wood: 312k
    (Unlocks.Carrots, 5),  # Wood: 156k
    (Unlocks.Pumpkins, 5),  # Carrot: 256k
    (Unlocks.Expand, 6),  # Pumpkin: 64k
    (Unlocks.Cactus, 2),  # Pumpkin: 120k
    (Unlocks.Mazes, 2),  # Cactus: 72k
    (Unlocks.Cactus, 3),  # Pumpkin: 720k
    (Unlocks.Megafarm, 2),  # Gold: 128k
    (Unlocks.Dinosaurs, 0),  # Cactus: 2k
    (Unlocks.Dinosaurs, 1),  # Cactus:
    (Unlocks.Dinosaurs, 2),  # Cactus:
    (Unlocks.Dinosaurs, 3),  # Cactus:
    (Unlocks.Dinosaurs, 4),  # Cactus:
    ####
    (Unlocks.Megafarm, 3),  # Gold:
    (Unlocks.Megafarm, 4),  # Gold:
    #
    # after megafarm
    (Unlocks.Expand, 7),  # Pumpkin: 512k
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
    prod_cost = max(w * h, num_needed)
    # carrot production need hay and wood first
    prod_hay(prod_cost)
    prod_wood(prod_cost)
    current = num_items(Items.Carrot)
    while (num_items(Items.Carrot) - current) < num_needed:
        worker.update_primitives_mt(0, 0, w, h, Grounds.Soil, Entities.Carrot)


def prod_pumpkins(num_needed):
    w, h = get_world_size(), get_world_size()
    prod_cost = max(w * h, num_needed)
    # pumpkin production need hay, wood and carrot first
    prod_carrots(prod_cost)

    current = num_items(Items.Pumpkin)
    while (num_items(Items.Pumpkin) - current) < num_needed:
        worker.update_pumpkin_mt(0, 0, w, h)


def prod_cactus(num_needed):
    w, h = get_world_size(), get_world_size()
    prod_cost = max(w * h, num_needed)
    # cactus production need pumpkin first
    prod_pumpkins(prod_cost)

    current = num_items(Items.Cactus)
    while (num_items(Items.Cactus) - current) < num_needed:
        worker.update_cactus_mt(0, 0, w, h)


def prod_gold(num_needed):
    w, h = get_world_size(), get_world_size()

    current = num_items(Items.Gold)
    while (num_items(Items.Gold) - current) < num_needed:
        if max_drones() < 16:
            worker.update_maze(0, 0, w, h)
        else:
            worker.update_maze_mt(0, 0, w, h)


prod_table = {
    Items.Hay: prod_hay,
    Items.Wood: prod_wood,
    Items.Carrot: prod_carrots,
    Items.Pumpkin: prod_pumpkins,
    Items.Cactus: prod_cactus,
    Items.Gold: prod_gold,
}

prev_time = get_time()
for unlock_target, level in scenarios:
    costs = get_cost(unlock_target, level)
    current_time = get_time()
    time_diff = current_time - prev_time
    prev_time = current_time
    quick_print(
        "Time:",
        current_time,
        "Lap Time:",
        time_diff,
        "Unlock:",
        unlock_target,
        "Level:",
        level,
        "Costs:",
        costs,
    )

    for key in costs:
        amount = costs[key]
        current = num_items(key)
        if current < amount:
            prod_table[key](amount - current)
    if not unlock(unlock_target):
        quick_print("Failed to unlock:", unlock_target, "Level:", level)
        break

while True:
    do_a_flip()  # just to keep the program running
    pass
