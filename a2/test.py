def expectimax(level, p_r, p_c, w_rs, w_cs, food_r, food_c):
    cache_key = (level, p_r, p_c, tuple(w_rs), tuple(w_cs), food_r, food_c)
    if cache_key in expectimax_cache:
        return expectimax_cache[cache_key]
    # Calculate average distance from all ghosts
    avg_ghost_distance = sum([get_distance(p_r, p_c, w_r, w_c) for w_r, w_c in zip(w_rs, w_cs)]) / len(w_rs)

    # If any ghost meets Pacman
    if any([get_distance(p_r, p_c, w_r, w_c) == 0 for w_r, w_c in zip(w_rs, w_cs)]):
        utility = -2000
        expectimax_cache[cache_key] = utility - avg_ghost_distance
        return utility

    if level == 0:
        utility = -get_distance(p_r, p_c, food_r, food_c)
        expectimax_cache[cache_key] = utility
        return utility

    # pacman's move
    if level % (number_of_ghost + 1) == 0:
        max_utility = -float('inf')
        for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
            new_x, new_y = p_r + delta_x, p_c + delta_y
            if is_valid_move(new_x, new_y):
                min_ = min([get_distance(new_x, new_y, w_r, w_c) for w_r, w_c in zip(w_rs, w_cs)])
                penalty = 0
                if min_ <= 2:
                    penalty -= 20
                # if min_ == 2:
                #     penalty = -10
                # elif min_ == 1:
                #     penalty = -100
                # elif min_ == 0:
                #     penalty = -2000

                utility = expectimax(level - 1, new_x, new_y, w_rs[:], w_cs[:], food_r, food_c) + penalty
                max_utility = max(max_utility, utility)
        expectimax_cache[cache_key] = max_utility
        return max_utility

    else:  # ghosts' moves
        ghost_idx = (level % (number_of_ghost + 1)) - 1
        w_r, w_c = w_rs[ghost_idx], w_cs[ghost_idx]

        total_utility = 0
        num_moves = 0
        for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
            new_x, new_y = w_r + delta_x, w_c + delta_y
            if is_valid_move(new_x, new_y):
                new_w_rs = w_rs[:ghost_idx] + [new_x] + w_rs[ghost_idx + 1:]
                new_w_cs = w_cs[:ghost_idx] + [new_y] + w_cs[ghost_idx + 1:]
                utility = expectimax(level - 1, p_r, p_c, new_w_rs, new_w_cs, food_r, food_c)
                total_utility += utility
                num_moves += 1

        utility = total_utility / num_moves if num_moves > 0 else 0
        expectimax_cache[cache_key] = utility
        return utility
