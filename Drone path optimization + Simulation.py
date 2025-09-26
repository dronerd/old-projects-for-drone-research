import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import itertools
import math
import random
from itertools import combinations

# First, set the parameters

# Setting the number of iterations to collect data
num_iterations = 100
# Maximum number of delivery destinations per delivery cluster
number_of_coordinates_in_clusters = 4
# Weight of the delivery item per package (g)
weight_per_package = 750
# Drone weight (g)
drone_weight = 2400
# Number of available drones
num_usable_drone = 15
# Number of delivery destinations
drone_coordinates_number = 50
# Drone flight speed (km/h)
drone_flight_speed = 45
# Radius of the delivery area (km)
radius = 10
# Air density
air_density = 1.2
# Flight altitude (m)
flight_height = 100
# Ascent speed during takeoff (m/s)
takeoff_speed = 5
# Descent speed during landing (m/s)
landing_speed = 2.5

# Next, configure the necessary functions

# Setting the function for calculating the distance between two points
def distance_between_two_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Setting the function for calculating the total path distance
def total_distance(path, points):
    total = 0
    for i in range(len(path) - 1):
        total += distance_between_two_points(points[path[i]], points[path[i + 1]])
    total += distance_between_two_points(points[path[-1]], points[path[0]])
    return total

# Setting the function for calculating the shortest path (TSP)
def find_shortest_path(points):
    shortest_distance = float('inf')
    shortest_path = None
    for perm in itertools.permutations(range(len(points))):
        dist = total_distance(perm, points) + distance_between_two_points(points[perm[-1]], (0, 0))
        if dist < shortest_distance:
            shortest_distance = dist
            shortest_path = perm
    return shortest_path

# Setting the function to randomly select delivery destination coordinates
def generate_coordinates(drone_coordinates_number):
    coordinates_list = []
    for _ in range(drone_coordinates_number):
        while True:
            x = random.uniform(-radius, radius)
            y = random.uniform(-radius, radius)
            if math.sqrt(x**2 + y**2) <= radius:
                coordinates_list.append((x, y))
                break
    return coordinates_list

# Setting the function to perform K-Means clustering
def cluster_points(points, number_of_coordinates_in_clusters):
    num_drones = max(1, len(points) // number_of_coordinates_in_clusters)
    kmeans = KMeans(n_clusters=num_drones, n_init=10, random_state=0).fit(points)
    centroids = kmeans.cluster_centers_
    assignments = kmeans.labels_
    drone_points = [[] for _ in range(num_drones)]
    for i, point in enumerate(points):
        drone_points[assignments[i]].append(point)
    # If the number of delivery destinations in one cluster is too many, split that cluster
    extra_clusters = []
    for cluster in drone_points:
        while len(cluster) > number_of_coordinates_in_clusters:
            extra_cluster = cluster[number_of_coordinates_in_clusters:]
            cluster[:] = cluster[:number_of_coordinates_in_clusters]
            extra_clusters.append(extra_cluster)
    drone_points = [cluster for cluster in drone_points if len(cluster) > 0]
    drone_points.extend(extra_clusters)
    return drone_points

# Function to calculate intersections of flight paths 
# (calculated as line segments. Using straight lines would also consider far-off intersections)
def segment_intersection(p1, p2, q1, q2):
    # Helper function to determine if a point is within the range of the line segment
    def is_between(a, b, c):
        return min(a, b) <= c <= max(a, b)
    # Calculate the intersections
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = q1
    x4, y4 = q2
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  # In cases where lines are parallel or overlapping
    xi = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    yi = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
    # Determine whether the intersection point lies within the range of both line segments
    if is_between(x1, x2, xi) and is_between(y1, y2, yi) and is_between(x3, x4, xi) and is_between(y3, y4, yi):
        return (xi, yi)
    return None

# Function to find intersections of flight paths
def find_intersections(paths):
    intersections = []
    path1, path2 = paths
    for i in range(len(path1) - 1):  # Check all segments of the first selected path
        for j in range(len(path2) - 1):  # Check all segments of the second selected path
            intersection = segment_intersection(path1[i], path1[i + 1], path2[j], path2[j + 1])
            if intersection:
                intersections.append(intersection)
    return intersections

# Function to find all intersections between different flight paths
# Using the combinations library, create pairs of sublists in drone_paths_rounded to search for intersections. 
# For example, if there are 6 flight paths, check 6C2 = 15 combinations.
def find_all_intersections(drone_paths_rounded, flight_heights):
    intersections = []
    path_intersections = {i: [] for i in range(len(drone_paths_rounded))}
    for (i, path1), (j, path2) in combinations(enumerate(drone_paths_rounded), 2):
        inters = find_intersections([path1, path2])
        for inter in inters:
            # Check the altitudes of the two paths being examined
            height1 = flight_heights[i]
            height2 = flight_heights[j]
            # Check if differing altitudes can avoid collision; if they do not collide, set height_flag = 1 to indicate it
            height_flag = 1 if height1 != height2 else 0
            # Append height_flag to the end
            extended_inter = (inter[0], inter[1], height_flag)
            path_intersections[i].append(extended_inter)
            path_intersections[j].append(extended_inter)
            intersections.append(extended_inter)
    return intersections, path_intersections

# Function to remove data with coordinates (0, 0) from the path_intersections list
def filter_path_intersections_for_zeros(path_intersections):
    filtered_paths = {}
    for key, coordinates in path_intersections.items():
        filtered_coordinates = [coord for coord in coordinates if any(c != 0.0 for c in coord[:2])]
        if filtered_coordinates:
            filtered_paths[key] = filtered_coordinates
    return filtered_paths


# Function to count the number of intersection marks ("X") in each flight path
# (counts if the third element is 0; does not count if it is 1)
def calculate_number_of_intersections(path_intersections_without_zeros_rounded):
    max_key = max(path_intersections_without_zeros_rounded.keys())
    number_of_intersections_each_path = [
        sum(1 for element in path_intersections_without_zeros_rounded.get(i, []) if element[2] != 1)
        for i in range(max_key + 1)
    ]
    return number_of_intersections_each_path

# Setting up the function to display the paths on image
def plot_assigned_paths_with_intersections(drone_assignments, drone_paths, flight_heights):
    plt.figure(figsize=(22, 16), dpi=100)
    colors = ['black', 'silver', 'maroon', 'purple', 'fuchsia', 'green', 'olive',
              'navy', 'blue', 'teal', 'aqua', 'orange', 'blueviolet', 'brown', 'burlywood', 'cadetblue',
              'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'crimson', 'cyan', 'darkblue',
              'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen',
              'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
              'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick',
              'floralwhite', 'forestgreen', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'greenyellow',
              'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush',
              'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow',
              'lightgray', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue',
              'lightslategray', 'lightsteelblue', 'lightyellow', 'limegreen', 'linen', 'magenta', 'mediumaquamarine',
              'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
              'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin',
              'navajowhite', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen',
              'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue',
              'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna',
              'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato',
              'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellowgreen']

    for i, drone_points in enumerate(drone_assignments):
        x = [point[0] for point in drone_points]
        y = [point[1] for point in drone_points]
        plt.scatter(x, y, color=colors[i], s=40, label=f'Drone {i+1} Assigned Balls')

        drone_path = drone_paths[i]
        flight_height = flight_heights[i % len(flight_heights)]  # Repeat based on the length of the list
        x_path = [point[0] for point in drone_path]
        y_path = [point[1] for point in drone_path]
        plt.plot(x_path, y_path, color=colors[i], linestyle='-', linewidth=2, label=f'Drone {i+1} Path')

        # Display the flight altitude next to the flight path
        for j in range(len(drone_path) - 1):
            mid_x = (drone_path[j][0] + drone_path[j + 1][0]) / 2
            mid_y = (drone_path[j][1] + drone_path[j + 1][1]) / 2
            plt.text(mid_x, mid_y, f"{flight_height}m", fontsize=10, color=colors[i])

    # Display the intersection points of the flight paths
    for ix, iy, height_flag in intersections_without_zeros_rounded:
        color = 'red' if height_flag == 0 else 'blue'  # Determine the color based on height_flag, red and blue
        plt.scatter(ix, iy, color=color, s=50, marker='x', linewidth=3, zorder=5, label='Intersection')

    plt.title('Drone Assigned Paths with Intersections', fontsize=18)
    plt.xlabel('X-coordinate', fontsize=12)
    plt.ylabel('Y-coordinate', fontsize=12)
    plt.legend(loc='upper left', bbox_to_anchor=(1.10, 1), fontsize=10)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()

# Function to plot the delivery destinations
def plot_assigned_points(drone_assignments):
    plt.figure(figsize=(22, 16), dpi=100)
    colors = ['black', 'silver', 'maroon', 'purple', 'fuchsia', 'green', 'olive',
              'navy', 'blue', 'teal', 'aqua', 'orange', 'blueviolet', 'brown', 'burlywood', 'cadetblue',
              'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'crimson', 'cyan', 'darkblue',
              'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen',
              'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
              'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick',
              'floralwhite', 'forestgreen', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'greenyellow',
              'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush',
              'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow',
              'lightgray', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue',
              'lightslategray', 'lightsteelblue', 'lightyellow', 'limegreen', 'linen', 'magenta', 'mediumaquamarine',
              'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
              'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin',
              'navajowhite', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen',
              'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue',
              'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna',
              'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato',
              'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellowgreen']
    for i, drone_points in enumerate(drone_assignments):
        x = [point[0] for point in drone_points]
        y = [point[1] for point in drone_points]
        plt.scatter(x, y, color=colors[i], s=60, label=f'Drone {i+1} Dots')

    plt.title('Drone Assigned Points', fontsize=18)
    plt.xlabel('X-coordinate', fontsize=12)
    plt.ylabel('Y-coordinate', fontsize=12)
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()

# Setting up the function to calculate the total travel distance for clustered delivery routes
def total_distance_new_method(path):
    total = 0
    for i in range(len(path) - 1):
        total += distance_between_two_points(path[i], path[i+1])
    return total

# Setting up the function to calculate the total travel distance using a round-trip method for each point
def calculate_conventional_travel_distances(coordinates_list):
    distances = []
    for (x, y) in coordinates_list:
        distance = 2 * round(math.sqrt(x**2 + y**2), 1)
        distances.append(distance)
    total_conventional_distance = round(sum(distances),1)
    return distances, total_conventional_distance

# Setting up the function to calculate energy consumption using the CMU power consumption model based on the number of packages being transported
def CMU_Energy_Consumption(number_of_packages):
    energy_for_takeoff = ( 80.4 * (weight_per_package / 1000 * number_of_packages + drone_weight / 1000) ** 1.5 / air_density ** 0.5 + 13.8 ) * (flight_height / takeoff_speed / 3600)
    energy_per_minute_cruise = 68.9 * (weight_per_package / 1000 * number_of_packages + drone_weight / 1000) ** 1.5 / air_density ** 0.5 + 16.8
    energy_for_landing = ( 71.5 * (weight_per_package / 1000 * number_of_packages + drone_weight / 1000) ** 1.5 / air_density ** 0.5 - 24.3 ) * (flight_height / landing_speed / 3600)
    return energy_for_takeoff, energy_per_minute_cruise, energy_for_landing

# Calculate the energy consumption per meter of travel (J/m) based on the number of packages being transported
object_five_takeoff_energy_consumption, object_five_cruise_energy_consumption, object_five_landing_energy_consumption = CMU_Energy_Consumption(5)
object_four_takeoff_energy_consumption, object_four_cruise_energy_consumption, object_four_landing_energy_consumption = CMU_Energy_Consumption(4)
object_three_takeoff_energy_consumption, object_three_cruise_energy_consumption, object_three_landing_energy_consumption = CMU_Energy_Consumption(3)
object_two_takeoff_energy_consumption, object_two_cruise_energy_consumption, object_two_landing_energy_consumption = CMU_Energy_Consumption(2)
object_one_takeoff_energy_consumption, object_one_cruise_energy_consumption, object_one_landing_energy_consumption = CMU_Energy_Consumption(1)
object_zero_takeoff_energy_consumption, object_zero_cruise_energy_consumption, object_zero_landing_energy_consumption = CMU_Energy_Consumption(0)

# Setting up the function to convert the number of packages being transported into a list of energy consumption efficiency 
# (used for energy consumption calculation)
def convert_to_energy_efficiency(num_carrying_objects_list):
    conversion = {
        5: object_five_cruise_energy_consumption,
        4: object_four_cruise_energy_consumption,
        3: object_three_cruise_energy_consumption,
        2: object_two_cruise_energy_consumption,
        1: object_one_cruise_energy_consumption,
        0: object_zero_cruise_energy_consumption
    }
    return [[conversion[num] for num in sublist] for sublist in num_carrying_objects_list]

# Setting up the function to convert the number of packages being transported into the energy consumption required for takeoff and landing 
# (used for energy consumption calculation)
def convert_to_takeoff_and_land_energy_efficiency(num_carrying_objects_list):
    conversion_takeoff_and_landing = {
        5: object_five_takeoff_energy_consumption + object_five_landing_energy_consumption,
        4: object_four_takeoff_energy_consumption + object_four_landing_energy_consumption,
        3: object_three_takeoff_energy_consumption + object_three_landing_energy_consumption,
        2: object_two_takeoff_energy_consumption + object_two_landing_energy_consumption,
        1: object_one_takeoff_energy_consumption + object_one_landing_energy_consumption,
        0: object_zero_takeoff_energy_consumption + object_zero_landing_energy_consumption
    }
    return [[conversion_takeoff_and_landing[num] for num in sublist] for sublist in num_carrying_objects_list]

# Setting up the function to calculate energy consumption for each path during transportation
def calculate_energy_consumption(travel_time_in_path, energy_efficiency_per_path):
    return [[round(travel_time * efficiency, 1) for travel_time, efficiency in zip(travel_time, efficiencies)]
            for travel_time, efficiencies in zip(travel_time_in_path, energy_efficiency_per_path)]

# Setting up the function to calculate the total energy consumption for clustered delivery routes
def calculate_sums(energy_consumption_for_each_path_phase):
    energy_total_sublist = [round(sum(sublist), 1) for sublist in energy_consumption_for_each_path_phase]
    energy_total = round(sum(energy_total_sublist), 1)
    return energy_total_sublist, energy_total

# Function to reorder delivery paths so that the total distance difference is minimized
def reorder_group(group, total_times):
    path_total_times = [(i, group[i][-1]) for i in range(len(group))]
    path_total_times.sort(key=lambda x: x[1])
    reordered_group = [group[i] for i, _ in path_total_times]
    reordered_total_times = [total_times[i] for i, _ in path_total_times]
    return reordered_group, reordered_total_times

# Function to plot histogram and box plot for clustered delivery routes
def plot_delivery_times_histogram_and_boxplot(times):
    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=10, edgecolor='black')
    plt.title('Delivery time for new method')
    plt.xlabel('Time(minutes)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
    plt.figure(figsize=(8, 6))
    plt.boxplot(times, vert=False, patch_artist=True, notch=True)
    plt.title('Delivery time for new method')
    plt.xlabel('Time（minutes)')
    plt.grid(True)
    plt.show()

# Function to plot histogram and box plot for conventional delivery routes
def plot_conventional_delivery_times(times):
    # Display histogram
    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=10, edgecolor='black')
    plt.title("Delivery time for conventional method")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Frequency")
    plt.show()
    # Display box plot
    plt.figure(figsize=(8, 6))
    plt.boxplot(times, vert=False)
    plt.title("Delivery time for conventional method")
    plt.xlabel("Time (miutes)")
    plt.show()

# Preparation of lists to store the results
total_travel_distance_new_method = []
total_travel_distance_conventional_method = []
total_energy_consumption_new_method_MJ = []
total_energy_consumption_new_method_kWh = []
total_energy_consumption_conventional_method_MJ = []
total_energy_consumption_conventional_method_kWh = []
average_delivery_time_new_method = []
average_delivery_time_conventional_method = []
median_delivery_time_new_method = []
median_delivery_time_conventional_method = []
all_times_new_method = []
all_times_conventional_method = []

# Function to calculate average of data list
def calculate_average(data_list):
    if len(data_list) > 0:
        return sum(data_list) / len(data_list)
    else:
        return 0

# Function to calculate normalized histogram for a given data
def normalized_histogram(data, bins, num_iterations):
    counts, bin_edges = np.histogram(data, bins=bins)
    counts = counts / num_iterations
    return counts, bin_edges

# Setting for the maximum number of delivery points per cluster.
# If it exceeds the range, the loop result will be invalid.
valid_range = set(range(number_of_coordinates_in_clusters+1))

# Main loop starts
for iteration in range(num_iterations+1):
    # Step 1: Randomly select delivery destination coordinates
    ping_pong_balls = generate_coordinates(drone_coordinates_number)

    # Step 2: Use K-Means clustering to divide delivery destinations into clusters
    points = ping_pong_balls
    drone_assignments = cluster_points(points, number_of_coordinates_in_clusters)
    
    # Step 3: Use TSP to calculate the shortest paths for drones to follow
    drone_paths = []
    for drone_points in drone_assignments:
        shortest_path_indices = find_shortest_path(drone_points)
        shortest_path_coordinates = [(0, 0)] + [drone_points[i] for i in shortest_path_indices] + [(0, 0)]
        drone_paths.append(shortest_path_coordinates)
    # Round drone paths to two decimal places    
    drone_paths_rounded = [[(round(x, 2), round(y, 2)) for x, y in path] for path in drone_paths]
    
    # Step 4: Find and save flight path intersections
    # Create list for flight heights based on number of paths created
    flight_heights = [flight_height] * len(drone_paths_rounded)
    intersections, path_intersections = find_all_intersections(drone_paths_rounded, flight_heights)
    path_intersections_without_zeros = filter_path_intersections_for_zeros(path_intersections)
    path_intersections_without_zeros_rounded = {key: [(round(x[0], 2), round(x[1], 2), x[2]) for x in value] for key, value in path_intersections_without_zeros.items()}
    # Round intersection coordinates and filter out (0.0, 0.0) points
    intersections_without_zeros = [intersection for intersection in intersections if not (intersection[0] == -0.0 and intersection[1] == -0.0)]
    intersections_without_zeros_rounded = [(round(intersection[0], 2), round(intersection[1], 2), intersection[2]) for intersection in intersections_without_zeros]
    # Count intersections for each path
    number_of_intersections_each_path = calculate_number_of_intersections(path_intersections_without_zeros_rounded)
   
    # Step 5: Calculate distances for each drone's delivery path
    distance_travelled_in_path = []
    for path in drone_paths:
        distances = []
        for i in range(len(path) - 1):
            distance = distance_between_two_points(path[i], path[i + 1])
            rounded_distance = round(distance, 4)
            distances.append(rounded_distance)
        distance_travelled_in_path.append(distances)
    
    # Step 6: Calculate total travel distance for clustered delivery routes
    total_distances = []
    for path in drone_paths:
        total = total_distance_new_method(path)
        rounded_total = round(total, 1)
        total_distances.append(rounded_total)
    total_distance_all_drones = sum(total_distances)
    rounded_total_distance = round(total_distance_all_drones, 1)
   
    # Step 7: Repeat until all intersection elements have 1 as the third element
    while any(element[2] == 0 for element in intersections_without_zeros_rounded):
        # Step 7-1: Find and save flight path intersections again
        intersections, path_intersections = find_all_intersections(drone_paths_rounded, flight_heights)
        path_intersections_without_zeros = filter_path_intersections_for_zeros(path_intersections)
        # Round intersection coordinates and filter out (0.0, 0.0) points again
        path_intersections_without_zeros_rounded = {key: [(round(x[0], 2), round(x[1], 2), x[2]) for x in value] for key, value in path_intersections_without_zeros.items()}
        intersections_without_zeros = [intersection for intersection in intersections if not (intersection[0] == -0.0 and intersection[1] == -0.0)]
        intersections_without_zeros_rounded = [(round(intersection[0], 2), round(intersection[1], 2), intersection[2]) for intersection in intersections_without_zeros]
        if all(element[2] == 1 for element in intersections_without_zeros_rounded):  # if all 1, end loop here
            break
        # Step 7-2: Identify path with most intersections
        number_of_intersections_each_path = calculate_number_of_intersections(path_intersections_without_zeros_rounded)
        max_intersections = max(number_of_intersections_each_path)
        indices_with_max_intersections = [idx for idx, value in enumerate(number_of_intersections_each_path) if value == max_intersections]
        # Out of identified paths, choose the one with shortest total distance
        min_distance = float('inf')
        best_index = None
        for idx in indices_with_max_intersections:
            if total_distances[idx] < min_distance:
                min_distance = total_distances[idx]
                best_index = idx
        max_path_index = best_index + 1
        # Step 7-3: Increase altitude of path with most intersections by 5m
        flight_heights[max_path_index -1 ] += 5
    
    # Step 8: Calculate total travel distance for conventional delivery method
    distances, total_conventional_distance = calculate_conventional_travel_distances(ping_pong_balls)
    
    # Step 9: Calculate delivery time for each destination in the clustered route
    # Using the drone's flight speed, convert delivery distances into delivery times.
    travel_time_in_path = [[round((dist / drone_flight_speed), 4) for dist in sublist] for sublist in distance_travelled_in_path]
    time_per_one_takeoff_and_landing = (flight_height / takeoff_speed / 3600) + (flight_height / landing_speed / 3600)
    travel_time_in_path_including_takeoff_and_landing = [[round(time + time_per_one_takeoff_and_landing, 4) for time in sublist] for sublist in travel_time_in_path]
    groups = [travel_time_in_path_including_takeoff_and_landing[i:i + num_usable_drone] for i in range(0, len(travel_time_in_path_including_takeoff_and_landing), num_usable_drone)]
    group_assignments = {}
    time_for_receiving_package = []
    for i, sublist in enumerate(groups[0]):
        cumulative_sum = 0
        new_sublist = []
        for time in sublist:
            cumulative_sum += time
            new_sublist.append(cumulative_sum)
        time_for_receiving_package.append(new_sublist)
        group_assignments[f"Path {i+1}"] = {"group": 1, "combined_with": None}
    # Combine the generated drone delivery paths so that the differences in total length are minimized.
    for group_idx in range(1, len(groups)):
        total_time_prev_group = [path[-1] for path in time_for_receiving_package[-num_usable_drone:]]
        reordered_group, reordered_prev_times = reorder_group(groups[group_idx], total_time_prev_group)
        time_for_receiving_package_group = []
        for i in range(len(reordered_group)):
            corresponding_time_prev = reordered_prev_times[i % len(reordered_prev_times)]
            cumulative_sum = corresponding_time_prev
            new_sublist = []
            for time in reordered_group[i]:
                cumulative_sum += time
                new_sublist.append(cumulative_sum)
            time_for_receiving_package_group.append(new_sublist)
            group_assignments[f"Path {sum(len(g) for g in groups[:group_idx]) + i+1}"] = {
                "group": group_idx + 1,
                "combined_with": i % len(reordered_prev_times) + 1
            }
        time_for_receiving_package.extend(time_for_receiving_package_group)
    time_for_evaluation = [time[:-1] for time in time_for_receiving_package]
    all_times = [round(time,4) for sublist in time_for_evaluation for time in sublist]
    # Calculate the average and median of the delivery times.
    average_time = np.mean(all_times)
    median_time = np.median(all_times)
    std_dev_time = np.std(all_times)
    
    # Step 10: Calculate the elapsed time to reach each delivery destination using a round-trip delivery method.
    time_flight_conventional = [round(d / drone_flight_speed + ( 2 * flight_height / takeoff_speed / 3600) + (2 * flight_height / landing_speed / 3600) , 4) for d in distances]
    grouped_times = []
    for i in range(0, len(time_flight_conventional), num_usable_drone):
        grouped_times.append(time_flight_conventional[i:i + num_usable_drone])
    for group_idx in range(1, len(grouped_times)):
        previous_group = grouped_times[group_idx - 1]
        current_group = sorted(grouped_times[group_idx])
        previous_group_sorted = sorted(previous_group, reverse=True)
        balanced_group = []
        for j in range(len(current_group)):
            if j % 2 == 0:
                balanced_time = previous_group_sorted[j] + current_group[j]
            else:
                balanced_time = previous_group_sorted[-(j + 1)] + current_group[-(j + 1)]
            balanced_group.append(balanced_time)
        grouped_times[group_idx] = balanced_group
    all_times_conventional = [round(time, 4) for group in grouped_times for time in group]
    average_time_conventional = np.mean(all_times_conventional)
    std_dev_time_conventional = np.std(all_times_conventional)
    median_time_conventional = np.median(all_times_conventional)
   
    # Step 11: Save the number of packages being carried during delivery in a list (for preparing power consumption calculation).
    num_carrying_objects_list = []
    for sublist in drone_assignments:
        sublist_result = []
        for i in range(len(sublist)):
            sublist_result.append(len(sublist) - i)
        sublist_result.append(0)
        num_carrying_objects_list.append(sublist_result)
    # Check the maximum number of destinations within a cluster. If it exceeds the range, stop the loop here and restart from the beginning.
    if any(num not in valid_range for sublist in num_carrying_objects_list for num in sublist):
        print("Failed to calculate the flight path, returning to the beginning of the loop")
        continue
   
    # Step 12: Calculate the total power consumption for the clustered delivery routes.
    energy_efficiency_per_path = convert_to_energy_efficiency(num_carrying_objects_list)
    energy_consumption_for_each_path_phase = calculate_energy_consumption(travel_time_in_path, energy_efficiency_per_path)
    energy_total_sublist, energy_total = calculate_sums(energy_consumption_for_each_path_phase)
    energy_takeoff_and_landing = convert_to_takeoff_and_land_energy_efficiency(num_carrying_objects_list)
    flattened_energy_takeoff_and_landing_list = [value for sublist in energy_takeoff_and_landing for value in sublist]
    total_energy_takeoff_and_landing = sum(flattened_energy_takeoff_and_landing_list)
    new_method_total_energy_consumption = energy_total + total_energy_takeoff_and_landing
    energy_total_MJ = round(new_method_total_energy_consumption / 1000 , 4) # Conversion from kJ to MJ
    energy_total_kWh = round(new_method_total_energy_consumption / 3600 , 4)  # Conversion to kWh
   
    # Step 13: Calculate the total power consumption using the round-trip delivery method.
    conventional_energy_consumption_for_each_path = [
        t * (0.5 * (object_one_cruise_energy_consumption + object_zero_cruise_energy_consumption))
        for t in time_flight_conventional]
    energy_total_conventional_cruise = sum(conventional_energy_consumption_for_each_path)
    energy_per_path_takeoff_and_landing = (
    object_one_landing_energy_consumption +
    object_one_takeoff_energy_consumption +
    object_zero_landing_energy_consumption +
    object_zero_takeoff_energy_consumption
    )
    energy_total_conventional_takeoff_and_landing = drone_coordinates_number * (energy_per_path_takeoff_and_landing)
    energy_total_conventional = energy_total_conventional_cruise + energy_total_conventional_takeoff_and_landing
    energy_total_conventional_MJ = round(energy_total_conventional / 1000 , 4)
    energy_total_conventional_kWh = round(energy_total_conventional / 3600, 4)
    
    # Step 14: Save all calculated results to the list before starting a new loop.
    total_travel_distance_new_method.append(rounded_total_distance)
    total_travel_distance_conventional_method.append(total_conventional_distance)
    total_energy_consumption_new_method_MJ.append(energy_total_MJ)
    total_energy_consumption_new_method_kWh.append(round(energy_total_kWh, 2))
    total_energy_consumption_conventional_method_MJ.append(energy_total_conventional_MJ)
    total_energy_consumption_conventional_method_kWh.append(round(energy_total_conventional_kWh, 1))
    average_delivery_time_new_method.append(round(average_time,4))
    average_delivery_time_conventional_method.append(round(average_time_conventional,4))
    median_delivery_time_new_method.append(round(median_time,4))
    median_delivery_time_conventional_method.append(round(median_time_conventional,4))
    all_times_new_method.extend(all_times)
    all_times_conventional_method.extend(all_times_conventional)
    print("Path calculation successful: ", iteration, "iteration")

# End of loop

# Display the results of the final loop: 
plot_assigned_points(drone_assignments)
plot_assigned_paths_with_intersections(drone_assignments, drone_paths, flight_heights)

# Output the list of intersections in the flight paths.
print("Intersections list:")
for intersection in intersections_without_zeros_rounded:
    print(intersection)

# Output number of intersections in each path
print("Number of collision intersections in each flight path: ", number_of_intersections_each_path)
print(f"The path with the most intersections is path {max_path_index}, with {max_intersections} intersections")

# print out delivery destinations assigned to each dorne
rounded_drone_assignments = [
    [(round(x, 2), round(y, 2)) for (x, y) in group]
    for group in drone_assignments
]
print("Delivery destinations assigned to each drone: ")
for i in rounded_drone_assignments:
    print(i)

# Print out delivery paths for each drone
print("Coordinates traversed in each flight path: ")
for i in drone_paths_rounded:
    print(i)

# Calculate average
average_total_travel_distance_new_method = calculate_average(total_travel_distance_new_method)
average_total_travel_distance_conventional_method = calculate_average(total_travel_distance_conventional_method)
average_total_energy_consumption_new_method_MJ = calculate_average(total_energy_consumption_new_method_MJ)
average_total_energy_consumption_new_method_kWh = calculate_average(total_energy_consumption_new_method_kWh)
average_total_energy_consumption_conventional_method_MJ = calculate_average(total_energy_consumption_conventional_method_MJ)
average_total_energy_consumption_conventional_method_kWh = calculate_average(total_energy_consumption_conventional_method_kWh)
average_delivery_time_new_method = calculate_average(average_delivery_time_new_method)
average_delivery_time_conventional_method = calculate_average(average_delivery_time_conventional_method)
average_median_delivery_time_new_method = calculate_average(median_delivery_time_new_method)
average_median_delivery_time_conventional_method = calculate_average(median_delivery_time_conventional_method)

# Print average
print(f"Average energy consumption across all experiments（New method) - MJ : {average_total_energy_consumption_new_method_MJ}")
print(f"Average energy consumption across all experiments (Conventional method) - MJ :  {average_total_energy_consumption_conventional_method_MJ}")
print(f"Average delivery time across all experiments（New method) - Time : {average_delivery_time_new_method}")
print(f"Average delivery time across all experiments（Conventional Method) - Time :  {average_delivery_time_conventional_method}")

# Display the histogram
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
bins = 10
counts_new, bin_edges_new = normalized_histogram(all_times_new_method, bins, num_iterations)
counts_conventional, bin_edges_conventional = normalized_histogram(all_times_conventional_method, bins, num_iterations)
axes[0].bar(bin_edges_new[:-1], counts_new, width=np.diff(bin_edges_new), alpha=0.7, label='New Method', color='blue', align='edge')
axes[0].bar(bin_edges_conventional[:-1], counts_conventional, width=np.diff(bin_edges_conventional), alpha=0.7, label='Conventional Method', color='red', align='edge')
axes[0].set_title('Histogram')
axes[0].set_xlabel('Hours')
axes[0].set_ylabel('Frequency / Iterations')
axes[0].legend()

# Display the boxplot
data = [all_times_new_method, all_times_conventional_method]
axes[1].boxplot(data, labels=['New Method', 'Conventional Method'])
axes[1].set_title('Boxplot')
axes[1].set_ylabel('Hours')
plt.tight_layout()
plt.show()
