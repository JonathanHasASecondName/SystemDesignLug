import numpy as np
from sklearn.preprocessing import normalize

from configuration import Configuration
from configurations_generator import find_coordinates

def calculate_cgs(coordinate_array):
    """
    input: a numpy array with the coordinates of one configuration stored as for example [[0, 0, 0], [0, 0, 1], etc.]
    with [x, y, z]
    """
    return np.mean(coordinate_array, axis=0)

def calculate_force_per_fastener(coordinate_array, forces, moments):
    # simply find the magnitude of the vector forces x and y per fastener
    vector_forces = calculate_vector_force_per_fastener(coordinate_array, forces)
    moment_forces = calculate_moment_force_per_fastener(coordinate_array, moments)
    return np.linalg.norm(vector_forces+moment_forces, axis=1)

def calculate_vector_force_per_fastener(coordinate_array, forces):
    """
    Input: a numpy array with the coordinates of one configuration and a numpy array of the forces.
    """
    forces[1] = 0  # ignore forces in the y direction, as that is not what this checks for
    fastener_forces = forces/len(coordinate_array)
    return np.tile(fastener_forces, reps=(len(coordinate_array), 1))

def calculate_moment_force_per_fastener(coordinate_array, moments):
    cgs = calculate_cgs(coordinate_array)
    relative_positions = coordinate_array-cgs
    absolute_distances = np.linalg.norm(relative_positions, axis=1)  # r_i
    squared_distance_sum = np.sum(absolute_distances*absolute_distances)  # r_i squared
    moment_force_magnitudes = moments[1]*absolute_distances/squared_distance_sum  # formula 4.4 from the manual
    normalized_position_vectors = normalize(relative_positions, axis=1, norm='l1')  # necessary for finding force vector

    x_norm_positions, y_norm_positions, z_norm_positions = np.hsplit(normalized_position_vectors, 3)
    # rotate the position vectors by 90 deg to get the right direction
    rotated_norm_pos_vectors = np.concatenate((-z_norm_positions, y_norm_positions, x_norm_positions), axis=1)
    # multiply each direction vector by the magnitude of the force in that fastener
    return moment_force_magnitudes.reshape(len(normalized_position_vectors), 1)*rotated_norm_pos_vectors

def calculate_t2(coordinate_array, D2, sigma_br, forces, moments):
    force_array = calculate_force_per_fastener(coordinate_array, forces, moments)
    t2 = force_array/(sigma_br*D2)  # the actual formula
    t2 = abs(t2)  # take the absolute value to make picking the minimum thickness possible
    min_thickness = max(t2)

    # The line below can be commented out during actual iteration
    print('the minimum thickness for bearing is ', min_thickness*1000, 'mm')
    return max(min_thickness, 0.001)  # 1 mm to take manufacturing into account

def check_thickness(coordinate_array, D2, sigma_br, forces, t2):
    # check for a given thickness whether it satisfies the
    return t2 > calculate_t2(coordinate_array, D2, sigma_br, forces)

num_rows = 2
num_columns = 2
e_1 = 0.015
w = 0.05
S_z = (1 / (num_rows - 1)) * (w - 2 * e_1)
coordinate_array = find_coordinates(
    h=0.01,
    D_2=0.005,
    t_1=0.002,
    e_1=0.015,
    e_2=0.015,
    S_z=S_z,
    S_x=0.01,
    num_rows=2,
    num_columns=1
)
forces = np.array([0, 0, 0])
moments = np.array([0, 100, 0])
D2=0.008
sigma_br=670000000
print(calculate_t2(coordinate_array, D2, sigma_br, forces, moments))
