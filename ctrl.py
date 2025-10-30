from __builtins__ import *


def move_to(x, y):
    cx, cy = get_pos_x(), get_pos_y()
    # need move pos
    dx = x - cx
    dy = y - cy

    for i in range(abs(dx)):
        if dx < 0:
            if not move(West):
                return False
        elif not move(East):
            return False

    for j in range(abs(dy)):
        if dy < 0:
            if not move(South):
                return False
        elif not move(North):
            return False

    return True


def set_ground_type(ground):
    if get_ground_type() != ground:
        till()


def maintain_water():
    if num_items(Items.Water) == 0:
        return False

    if get_water() < 0.1:
        use_item(Items.Water)
    return True


def use_fertilizer():
    if num_items(Items.Fertilizer) == 0:
        return False
    use_item(Items.Fertilizer)
    return True


def wait_drones(wait_drones):
    while len(wait_drones) > 0:
        d = wait_drones.pop(0)
        # check again later
        if not has_finished(d):
            wait_drones.append(d)
            continue


def dispatch_mt_task(drones, task_f, run_own_if_no_drone=True):
    d = spawn_drone(task_f)
    # success spawn
    if d:
        drones.append(d)
        return True

    if run_own_if_no_drone:
        # run single thread
        task_f()
        return True

    # failed to spawn and not run own
    return False
