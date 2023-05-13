import numpy as np
import sys

FILE = sys.argv[1] if len(sys.argv) > 1 else "file5.txt"


def parse_file(text_in):
    max_dist, _, *points, _ = text_in.split("\n")
    return {
        "max_dist": int(max_dist),
        "points": list(map(
            lambda point_str: (int(point_str.split(" ")[0]), int(point_str.split(" ")[1])),
            points
        ))
    }


def point_dist(pointA, pointB):
    return np.sqrt((pointA[0] - pointB[0]) * (pointA[0] - pointB[0]) + (pointA[1] - pointB[1]) * (pointA[1] - pointB[1]))


distance_map = {
}


def create_distance_map(points):
    for point in points:
        dist_from_center = int(point_dist(point, (0, 0)))

        if dist_from_center in distance_map.keys():
            distance_map[dist_from_center].append(point)
        else:
            distance_map[dist_from_center] = [point]


def points_from_distance_map(distance_from_center, dist_range):
    out = []
    for key in distance_map.keys():
        if distance_from_center - dist_range < key < distance_from_center + dist_range + 1:
            out += distance_map[key]

    return out


previous_in_range = {
}


def points_arround(position, dist, points):
    global previous_in_range
    out = []

    if position in previous_in_range.keys():
        points = previous_in_range[position]
    else:
        points = points_from_distance_map(point_dist(position, (0, 0)), dist)

    for point in points:
        if point_dist(position, point) <= dist:
            out.append(point)

    previous_in_range[position] = out

    return out


def get_next_point(visited_points, points, remaining_dist):
    global previous_in_range

    max_score = 0
    best_point = -1

    start_position = points[visited_points[-1]]

    if start_position in previous_in_range.keys():
        points = previous_in_range[start_position]

    remaining_points = []
    for i in range(len(points)):
        if i not in visited_points:
            remaining_points.append(i)

    for i in remaining_points:
        if i in visited_points:
            continue

        if point_dist(start_position, points[i]) > remaining_dist:
            continue

        points_arround_list = points_arround(start_position, remaining_dist, list(map(lambda index: points[index], remaining_points)))

        points_arround_qty = len(points_arround_list)

        score = points_arround_qty / point_dist(start_position, points[i])

        if score > max_score:
            best_point = i
            max_score = score

    return best_point


f_in = open(f"in/{FILE}", "r")
text_in = f_in.read()

text_out = text_in

data = parse_file(text_in)

crossed_dist = 0
remaining_dist = data["max_dist"]

max_score = 0
best_point = 0

create_distance_map(data["points"])

for i in range(len(data["points"])):
    if len(points_arround(data["points"][i], remaining_dist, data["points"])) > max_score:
        best_point = i


visited_points = [best_point]

while remaining_dist >= 0:
    print("=" * 5)
    next_point = get_next_point(visited_points, data["points"], remaining_dist)

    remaining_dist -= point_dist(data["points"][visited_points[-1]], data["points"][next_point])

    visited_points.append(next_point)

    print(" ".join(list(map(lambda i: str(i), visited_points))))

visited_points = list(filter(lambda i: i != -1, visited_points))
str_points = list(map(lambda i: str(i), visited_points))

f_out = open(f"out/{FILE}", "w")
f_out.write(" ".join(str_points))
