import numpy as np

from configuration import Configuration
from configurations_generator import find_coordinates

def calculate_cgs(coordinate_array):
    """
    input: a numpy array with the coordinates of one configuration stored as for example [[0, 0, 0], [0, 0, 1], etc.]
    with [x, y, z]
    """
    return np.mean(coordinate_array, axis=0)

def calculate_force_per_fastener(coordinate_array, forces):
    # simply find the magnitude of the vector forces x and y per fastener
    vector_forces = calculate_vector_force_per_fastener(coordinate_array, forces)
    return np.linalg.norm(vector_forces, axis=1)

def calculate_vector_force_per_fastener(coordinate_array, forces):
    """
    Input: a numpy array with the coordinates of one configuration and a numpy array of the forces.
    """
    forces[1] = 0  # ignore forces in the y direction, as that is not what this checks for
    fastener_forces = forces/len(coordinate_array)
    return np.tile(fastener_forces, reps=(len(coordinate_array), 1))

def calculate_t2(coordinate_array, D2, sigma_br, forces):
    force_array = calculate_force_per_fastener(coordinate_array, forces)
    t2 = force_array/(sigma_br*D2)  # the actual formula
    t2 = abs(t2)  # take the absolute value to make picking the minimum thickness possible
    min_thickness = max(t2)

    # The line below can be commented out during actual iteration
    print('the minimum thickness for bearing is ', min_thickness*1000, 'mm')
    return max(min_thickness, 0.001)  # 1 mm to take manufacturing into account
