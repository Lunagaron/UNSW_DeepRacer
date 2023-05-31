def reward_function(params):
    """
    Sample Reward Function Verifying Track Waypoints
    """

    # Gets the information of the track
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    center_variance = distance_from_center / track_width

    # Creates a personalised racing line - based on the circuit information sourced above from AWS DeepRacer community
    left = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 64, 65,
            66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 103,
            104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116]
    center = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 45, 46, 60, 61, 62, 63, 91, 92, 93, 94,
              95, 96, 97, 98, 99, 100, 101, 102, 117, 118]
    right = [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]

    # Creates a personalised speed recommendation for various parts of the track
    fast = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
            56, 57, 58, 59, 60, 61, 62, 63, 64, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 113, 114,
            115, 116, 117, 118]
    moderate = [20, 21, 22, 23, 42, 43, 44, 45, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 88, 89,
                110, 111, 112]
    slow = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 81, 82, 83, 84, 85, 86, 87, 104,
            105, 106, 107, 108, 109]

    # Set a default reward initialization
    reward = 1e-3

    # Penalizes model if wheels are off track
    if params["all_wheels_on_track"]:
        reward += 10
    else:
        reward -= 10

    # Rewards model for being in the correct part of the pre-defined track
    closest_waypoint = params["closest_waypoints"][1]
    if closest_waypoint in left and params["is_left_of_center"]:
        reward += 10
    elif closest_waypoint in right and not params["is_left_of_center"]:
        reward += 10
    elif closest_waypoint in center and center_variance < 0.4:
        reward += 10
    else:
        reward -= 10

    # Rewards model for travelling at the correct speed in the track
    if closest_waypoint in fast:
        if params["speed"] > 2:
            reward += 10
        else:
            reward -= 10
    elif closest_waypoint in moderate:
        if 1.5 < params["speed"] <= 2:
            reward += 10
        else:
            reward -= 10
    elif closest_waypoint in slow:
        if params["speed"] <= 1.5:
            reward += 10
        else:
            reward -= 10

    return float(reward)
