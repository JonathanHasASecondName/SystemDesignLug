import numpy as np
from copy import deepcopy

from configuration import Configuration
from configurations_generator import find_coordinates

def calculate_cgs(coordinate_array):
    """
    input: a numpy array with the coordinates of one configuration stored as for example [[0, 0, 0], [0, 0, 1], etc.]
    with [x, y, z]
    """
    return np.mean(coordinate_array, axis=0)

def calculate_normal_force_per_fastener(coordinate_array, forces):
    # simply find the magnitude of the vector forces x and y per fastener
    vector_forces = calculate_normal_vector_force_per_fastener(coordinate_array, forces)
    return np.linalg.norm(vector_forces, axis=1)

def calculate_normal_vector_force_per_fastener(coordinate_array, forces):
    """
    Input: a numpy array with the coordinates of one configuration and a numpy array of the forces.
    """
    forces = deepcopy(forces)  # if we do not copy the forces, it will fuck up other things, as the original array
                               # gets set to zero, which we obviously do not want
    forces[0] = 0  # ignore forces in the x direction, as that is not what this checks for
    forces[2] = 0  # ignore forces in the x direction, as that is not what this checks for
    fastener_forces = forces/len(coordinate_array)
    return np.tile(fastener_forces, reps=(len(coordinate_array), 1))

def calculate_total_moment(coordinate_array: np.array, forces: np.array, forces_location: np.array):
    cgs = calculate_cgs(coordinate_array)
    total_moment = np.cross((forces_location-cgs), forces)  # positive moment defined as caused by a positive force in
                                                            # the z-direction away from the spacecraft
    return total_moment

def calculate_moment_force_per_fastener(coordinate_array: np.array, forces: np.array, forces_location: np.array):
    # TODO validate this shit, I wrote it at 12 pm
    total_moment = calculate_total_moment(coordinate_array, forces, forces_location)
    # note r_i in eq. 4.6 refers to distance from axis of the cg. to the row (for M_x) or column (M_y) of the bolt
    r_i = coordinate_array-cgs
    r_ix, r_iy, r_iz = np.hsplit(r_i, 3)  # split the array into three parts
    y_forces_due_to_X_moment = -total_moment[0]*r_iz/np.sum(r_iz*r_iz)
    y_forces_due_to_Z_moment = total_moment[2]*r_ix/np.sum(r_ix*r_ix)
    # print(y_forces_due_to_Z_moment)
    # print(coordinate_array)
    return np.transpose(y_forces_due_to_X_moment+y_forces_due_to_Z_moment)  # get the correct shape for summing later

def calculate_total_force_per_fastener(coordinate_array: np.array, forces: np.array, forces_location: np.array):
    normal_forces = calculate_normal_force_per_fastener(coordinate_array, forces)
    moment_forces = calculate_moment_force_per_fastener(coordinate_array, forces, forces_location)
    return normal_forces+moment_forces

def calculate_t2(coordinate_array, D_o, tau_yield, forces, force_location):
    force_array = calculate_total_force_per_fastener(coordinate_array, forces, force_location)
    t2 = force_array/(D_o*np.pi*tau_yield)  # the actual formula
    t2 = abs(t2)  # take the absolute value to make picking the minimum thickness possible
    min_thickness = max(t2)

    # The line below can be commented out during actual iteration
    print('the minimum thickness for out-of-plane load is ', min_thickness*1000, 'mm')
    return max(min_thickness, 0.001)  # 1 mm to take manufacturing into account

def check_thickness(coordinate_array, D2, sigma_br, forces, t2, forces_location):
    # check for a given thickness whether it satisfies the
    return t2 > calculate_t2(coordinate_array, D2, sigma_br, forces, forces_location)

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
cgs = calculate_cgs(coordinate_array)
forces_location = np.array([cgs[0], w/2, cgs[2]])
forces = np.array([1000, 0, 0])
print(forces)
print(coordinate_array)
print(calculate_total_force_per_fastener(coordinate_array, forces, forces_location))
