def reward_calculator(input_params):
    """ 
    Reward Function based on Waypoint Model
    """
    import math
    import numpy as np
    
    # AWS DeepRacer predefined parameters
    all_wheels_on_track = input_params['all_wheels_on_track']
    closest_waypoints = input_params['closest_waypoints']
    distance_from_center = input_params['distance_from_center']
    is_offtrack = input_params['is_offtrack']
    progress = input_params['progress']
    speed = input_params['speed']
    steering_angle = input_params['steering_angle']
    steps = input_params['steps']
    track_width = input_params['track_width']
    waypoints = input_params['waypoints']
    
    # Define dynamic parameters based on steps and progress status
    TURN_THRESHOLD_SPEED = 5 + steps / 1000
    SPEED_THRESHOLD_SLOW = 1.2 + progress / 100
    SPEED_THRESHOLD_FAST = 2.4 + progress / 100
    TURN_THRESHOLD_STRAIGHT = 24 + steps / 1000
    STEERING_THRESHOLD = 10 + steps / 1000
    FUTURE_STEP_SPEED = 5 + int(steps / 100)
    FUTURE_STEP_STRAIGHT = 7 + int(steps / 100)
    TOTAL_NUM_STEPS = 665 + int(progress / 2)

    def calculate_corner(waypoints, nearest_waypoints, future_step):
        previous_point = waypoints[nearest_waypoints[0]]
        next_point = waypoints[nearest_waypoints[1]]
        future_point = waypoints[min(len(waypoints) - 1, nearest_waypoints[1] + future_step)]

        current_heading = math.degrees(math.atan2(previous_point[1] - next_point[1], previous_point[0] - next_point[0]))
        future_heading = math.degrees(math.atan2(previous_point[1] - future_point[1], previous_point[0] - future_point[0]))

        heading_diff = abs(current_heading - future_heading)

        if heading_diff > 180:
            heading_diff = 360 - heading_diff

        future_dist = np.linalg.norm([next_point[0] - future_point[0], next_point[1] - future_point[1]])

        return heading_diff, future_dist

    def determine_speed(waypoints, nearest_waypoints, future_step):
        heading_diff, future_dist = calculate_corner(waypoints, nearest_waypoints, future_step)

        if heading_diff < TURN_THRESHOLD_SPEED:
            is_fast = True
        else:
            is_fast = False

        return is_fast

    def determine_straight_path(waypoints, nearest_waypoints, future_step):
        heading_diff, future_dist = calculate_corner(waypoints, nearest_waypoints, future_step)

        if heading_diff < TURN_THRESHOLD_STRAIGHT:
            is_straight = True
        else:
            is_straight = False

        return is_straight
    
    if is_offtrack:
        reward_val = 1e-3
        return float(reward_val)

    reward_val = 1 - (distance_from_center / (track_width / 2)) ** (1 / 4)

    if (steps % 50) == 0 and progress / 100 > (steps / TOTAL_NUM_STEPS):
        reward_val += progress - (steps / TOTAL_NUM_STEPS) * 100

    is_straight_path = determine_straight_path(waypoints, closest_waypoints, FUTURE_STEP_STRAIGHT)
    if is_straight_path and abs(steering_angle) < STEERING_THRESHOLD:
        reward_val += 0.31

    is_fast_speed = determine_speed(waypoints, closest_waypoints, FUTURE_STEP_SPEED)

    if is_fast_speed and speed > SPEED_THRESHOLD_FAST and abs(steering_angle) < STEERING_THRESHOLD:
        reward_val += 2.1

    elif not is_fast_speed and speed < SPEED_THRESHOLD_SLOW:
        reward_val += 0.51

    if not all_wheels_on_track:
        reward_val -= 0.51

    reward_val = max(reward_val, 1e-3)
    return float(reward_val)
