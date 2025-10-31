import control
from __builtins__ import *


def update_primitives(sx, sy, width, height, ground, entity):
    for j in range(height):
        for i in range(width):
            # place the trees altenatery
            if entity == Entities.Tree:
                if ((i + j) % 2) == 0:
                    continue

            x, y = sx + i, sy + j
            control.move_to(x, y)

            # Grass special case
            if entity == Entities.Grass:
                control.set_ground_type(ground)
                while not can_harvest():
                    if control.use_fertilizer():
                        continue
                    control.maintain_water()
                harvest()
                continue

            if get_entity_type() != None:
                if not can_harvest():
                    control.use_fertilizer()
                harvest()
            control.set_ground_type(ground)
            plant(entity)
            control.maintain_water()


def update_glass(sx, sy, width, height):
    update_primitives(sx, sy, width, height, Grounds.Grassland, Entities.Grass)


def update_bush(sx, sy, width, height):
    update_primitives(sx, sy, width, height, Grounds.Soil, Entities.Bush)


def update_carrot(sx, sy, width, height):
    update_primitives(sx, sy, width, height, Grounds.Soil, Entities.Carrot)


def update_sunflower(sx, sy, width, height):
    update_primitives(sx, sy, width, height, Grounds.Soil, Entities.Sunflower)


def update_tree(sx, sy, width, height):
    update_primitives(sx, sy, width, height, Grounds.Soil, Entities.Tree)


def update_pumpkin(sx, sy, width, height):
    for j in range(height):
        todo_x_list = list(range(sx, sx + width))
        while len(todo_x_list) > 0:
            i = todo_x_list.pop(0)
            x, y = sx + i, sy + j
            control.move_to(x, y)

            while True:
                entity = get_entity_type()
                if (entity == None) or (entity == Entities.Dead_Pumpkin):
                    control.set_ground_type(Grounds.Soil)
                    plant(Entities.Pumpkin)
                    control.maintain_water()
                    todo_x_list.append(i)  # re-check
                    break
                elif entity == Entities.Pumpkin:
                    if not can_harvest():
                        # growing pumpkin
                        if control.use_fertilizer():
                            continue  # re-check immediately
                        else:
                            todo_x_list.append(i)  # re-check after growing
                            break
                    else:
                        # good pumpkin
                        break
                else:
                    # wrong entity
                    if can_harvest():
                        harvest()
                    control.set_ground_type(Grounds.Soil)
                    continue  # re-check immediately

    # done
    harvest()


def sort_cactus(sx, sy, width, height):
    # sort all rows
    for j in range(height):
        for n in range(width):
            for i in range(width - 1 - n):
                x, y = i + sx, j + sy
                control.move_to(x, y)
                s0 = measure()
                control.move_to(x + 1, y)
                s1 = measure()
                if s0 > s1:
                    swap(West)
    # sort all cols
    for i in range(width):
        for n in range(height):
            for j in range(height - 1 - n):
                x, y = i + sx, j + sy
                control.move_to(x, y)
                s0 = measure()
                control.move_to(x, y + 1)
                s1 = measure()
                if s0 > s1:
                    swap(South)


def update_cactus(x, y, width, height):
    # harvest all area
    update_primitives(x, y, width, height, Grounds.Soil, Entities.Cactus)
    # harvest sorted cactus
    sort_cactus(x, y, width, height)
    harvest()


def update_dino():
    sx, sy = 0, 0
    width, height = get_world_size(), get_world_size()

    # hamiltonian cyc not found
    if (width % 2 != 0) or (height % 2 != 0):
        set_world_size(width - 1)
        width, height = width - 1, height - 1

    control.move_to(sx, sy)
    change_hat(Hats.Dinosaur_Hat)

    # move hamiltonian cycle
    need_abort = False
    while not need_abort:
        # saw loop
        # |-| | ......... |
        # | | |           |
        # | |-|           |
        # s
        i = 0
        while (get_pos_x() < (sx + width - 1)) and (not need_abort):
            need_abort = need_abort or not control.move_to(sx + i + 0, sy + height - 1)
            need_abort = need_abort or not control.move_to(sx + i + 1, sy + height - 1)
            need_abort = need_abort or not control.move_to(sx + i + 1, sy + 1)
            i += 2

        # last row
        #
        #
        #
        # s----...........-
        need_abort = need_abort or not control.move_to(sx + width - 1, sy)
        need_abort = need_abort or not control.move_to(sx, sy)

    # finalize
    change_hat(Hats.Straw_Hat)


def solve_maze(sx, sy, px, py, gx, gy, width, height):
    # dx, dy, direction, inv(direction)
    dirs = [
        (1, 0, East, West),
        (0, 1, North, South),
        (-1, 0, West, East),
        (0, -1, South, North),
    ]

    cx, cy = get_pos_x(), get_pos_y()
    # goal
    if (cx == gx) and (cy == gy):
        harvest()
        return True

    # search
    for dx, dy, dir, dir_inv in dirs:
        nx, ny = cx + dx, cy + dy
        if (nx < 0) or (ny < 0) or (width <= nx) or (height <= ny):
            # out of range
            continue
        if (nx == px) and (ny == py):
            # came from
            continue
        if can_move(dir):
            # try next pos
            move(dir)
            # (px, py) -> (cx, cy): update came from
            ret = solve_maze(sx, sy, cx, cy, gx, gy, width, height)
            # goal
            if ret:
                return True

            # pop pos & try others
            move(dir_inv)
    # no goal found
    return False


def update_maze(x, y, width, height):
    sx, sy = x, y  # todo x, y != (0, 0)

    # init maze
    update_primitives(sx, sy, 1, 1, Grounds.Soil, Entities.Bush)
    substance = width * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)

    # solve
    gx, gy = measure()
    # (px, py) = (sx, sy): came from initial pos
    if not solve_maze(sx, sy, sx, sy, gx, gy, width, height):
        # clear maze
        harvest()


####################################################################################
# multi drone


def update_pumpkin_row(sx, y, width):
    todo_x_list = list(range(sx, sx + width))
    while len(todo_x_list) > 0:
        i = todo_x_list.pop(0)
        x = sx + i
        control.move_to(x, y)

        while True:
            entity = get_entity_type()
            if (entity == None) or (entity == Entities.Dead_Pumpkin):
                control.set_ground_type(Grounds.Soil)
                plant(Entities.Pumpkin)
                control.maintain_water()
                todo_x_list.append(i)  # re-check
                break
            elif entity == Entities.Pumpkin:
                if not can_harvest():
                    # growing pumpkin
                    if control.use_fertilizer():
                        continue  # re-check immediately
                    else:
                        todo_x_list.append(i)  # re-check after growing
                        break
                else:
                    # good pumpkin
                    break
            else:
                # wrong entity
                if can_harvest():
                    harvest()
                control.set_ground_type(Grounds.Soil)
                continue  # re-check immediately


def update_pumpkin_mt(sx, sy, width, height):
    drones = []
    for j in range(height):
        y = sy + j

        def fill_row():
            update_pumpkin_row(sx, y, width)

        control.dispatch_mt_task(drones, fill_row)

    control.wait_drones(drones)
    # done
    harvest()


def update_primitives_row(sx, y, width, height, ground, entity):
    for i in range(width):
        # place the trees altenatery
        if entity == Entities.Tree:
            if ((i + y) % 2) == 0:
                continue

        x = sx + i
        control.move_to(x, y)

        # Grass special case
        if entity == Entities.Grass:
            control.set_ground_type(ground)
            while not can_harvest():
                if control.use_fertilizer():
                    continue
                control.maintain_water()
            harvest()
            continue

        if get_entity_type() != None:
            if not can_harvest():
                control.use_fertilizer()
            harvest()
        control.set_ground_type(ground)
        plant(entity)
        control.maintain_water()


def update_primitives_mt(sx, sy, width, height, ground, entity):
    drones = []
    for j in range(height):
        y = sy + j

        def update_row():
            update_primitives_row(sx, y, width, height, ground, entity)

        control.dispatch_mt_task(drones, update_row)
    # wait all drones
    control.wait_drones(drones)


def sort_cactus_row_mt(sx, y, width, height):
    # sort all rows
    for n in range(width):
        for i in range(width - 1 - n):
            x = i + sx
            control.move_to(x, y)
            s0 = measure()
            control.move_to(x + 1, y)
            s1 = measure()
            if s0 > s1:
                swap(West)


def sort_cactus_col_mt(x, sy, width, height):
    # sort all cols
    for n in range(height):
        for j in range(height - 1 - n):
            y = j + sy
            control.move_to(x, y)
            s0 = measure()
            control.move_to(x, y + 1)
            s1 = measure()
            if s0 > s1:
                swap(South)


def sort_cactus_mt(sx, sy, width, height):
    drones = []
    # sort all rows
    for j in range(height):
        y = sy + j

        def sort_row():
            sort_cactus_row_mt(sx, y, width, height)

        control.dispatch_mt_task(drones, sort_row)

    # wait (conflict row x col)
    control.wait_drones(drones)

    # sort all cols
    for i in range(width):
        x = sx + i

        def sort_col():
            sort_cactus_col_mt(x, sy, width, height)

        control.dispatch_mt_task(drones, sort_col)
    # wait all drones
    control.wait_drones(drones)


def update_cactus_mt(x, y, width, height):
    # plant & sort
    update_primitives_mt(x, y, width, height, Grounds.Soil, Entities.Cactus)
    sort_cactus_mt(x, y, width, height)
    harvest()


def solve_maze_mt(sx, sy, px, py, gx, gy, width, height):
    # dx, dy, direction, inv(direction)
    dirs = [
        (1, 0, East, West),
        (0, 1, North, South),
        (-1, 0, West, East),
        (0, -1, South, North),
    ]

    cx, cy = get_pos_x(), get_pos_y()
    # goaled
    if get_entity_type() == Entities.Grass:
        return
    # goal
    if (cx == gx) and (cy == gy):
        harvest()
        return

    # search
    next_candidates = []
    for dx, dy, dir, dir_inv in dirs:
        nx, ny = cx + dx, cy + dy
        if (nx < 0) or (ny < 0) or (width <= nx) or (height <= ny):
            # out of range
            continue
        if (nx == px) and (ny == py):
            # came from
            continue
        if can_move(dir):
            next_candidates.append((dx, dy, dir, dir_inv))

    num_cand = len(next_candidates)
    if num_cand == 0:
        # dead end
        return
    elif num_cand == 1:
        # single candidate
        dx, dy, dir, dir_inv = next_candidates[0]
        move(dir)
        # (px, py) -> (cx, cy): update came from
        solve_maze_mt(sx, sy, cx, cy, gx, gy, width, height)
        return
    else:
        # multiple candidates
        drones = []
        for dx, dy, dir, dir_inv in next_candidates:
            # wait other drone despawn
            while max_drones() - num_drones() <= 0:
                pass

            # define task & spawn
            def task_f():
                move(dir)
                # (px, py) -> (cx, cy): update came from
                solve_maze_mt(sx, sy, cx, cy, gx, gy, width, height)

            control.dispatch_mt_task(drones, task_f)

        # no wait all drones brocking:
        #   if any drone found goal, entity changed to Grass


def update_maze_mt(x, y, width, height):
    sx, sy = x, y  # todo x, y != (0, 0)

    # init maze
    update_primitives(sx, sy, 1, 1, Grounds.Soil, Entities.Bush)
    substance = width * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)

    # solve
    gx, gy = measure()
    # (px, py) = (sx, sy): came from initial pos
    solve_maze_mt(sx, sy, sx, sy, gx, gy, width, height)
    while num_drones() > 1:
        pass
