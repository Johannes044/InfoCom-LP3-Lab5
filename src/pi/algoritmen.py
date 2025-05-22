import heapq

from No_fly_zone import halve_zone

NO_FLY_ZONES = [
    {
        "min_lon": 13.182460,
        "max_lon": 13.214460,
        "min_lat": 55.702952,
        "max_lat": 55.720952
    },
    {
        "min_lon": 13.197878,
        "max_lon": 13.229878,
        "min_lat": 55.708623,
        "max_lat": 55.726623
    }
]

def is_in_no_fly_zone(lon, lat):
    r2 = [z for zone in NO_FLY_ZONES for z in halve_zone(zone)]
    reduced_zones = [z for zone in r2 for z in halve_zone(zone)]
    for zone in reduced_zones:
        if zone["min_lon"] <= lon <= zone["max_lon"] and zone["min_lat"] <= lat <= zone["max_lat"]:
            return True
    return False

def interpolate_path(path, steps_per_segment=10):
    smooth_path = []
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        for s in range(steps_per_segment):
            t = s / steps_per_segment
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            smooth_path.append((x, y))
    smooth_path.append(path[-1])  # include final point
    return smooth_path


def heuristic(a, b):
    # Manhattan distance works for grid-based movement
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def a_star(start, goal, step_size=0.0005, max_iter=100000):#0.0001 är cirka 11 meter steg if to jumping.
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    directions = [
        (step_size, 0), (-step_size, 0),
        (0, step_size), (0, -step_size),
        (step_size, step_size), (-step_size, step_size),
        (step_size, -step_size), (-step_size, -step_size)
    ]

    iterations = 0

    while open_set and iterations < max_iter:
        iterations += 1
        current = heapq.heappop(open_set)[1]

        # Check if goal reached (very close is enough)
        if heuristic(current, goal) < step_size:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for dx, dy in directions:
            neighbor = (round(current[0] + dx, 7), round(current[1] + dy, 7))  # round to avoid float drift

            if is_in_no_fly_zone(*neighbor):
                continue

            tentative_g_score = g_score[current] + heuristic(current, neighbor)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found


start = (13.1800, 55.7030)   # Sydväst om zonerna
goal = (13.2330, 55.7270)    # Nordost om zonerna

path = a_star(start, goal)

newpath = interpolate_path(p)

if newpath:
    for p in path:
        print(p)
else:
    print("Ingen väg hittades!")
