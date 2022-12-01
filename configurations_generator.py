import pandas as pd
import numpy as np
from configuration import Configuration
from config import *
from materials_list import materials_list

def generate_configurations() -> list[Configuration]:
    """
    This function generates a list of all configurations that matches the requirements for forces.
    :return: A list of all the configurations.
    """

    configurations = []
    bolt_types = read_table("bolts.csv")

    for fastener_material in materials_list:
        for lug_material in materials_list:
            if lug_material != fastener_material:
                for bolt_type in bolt_types:
                    D_2 = bolt_type[1]*0.001
                    e_1 = 1.5 * D_2
                    e_2 = 1.5 * D_2
                    e_3 = t_1 + 0.5 * D_2
                    num_rows_max = find_number_of_rows(fastener_material, e_1, D_2, w)
                    S_x = find_S_x(fastener_material, D_2)
                    num_columns_max = 2
                    for num_rows in range(2, num_rows_max+1):
                        for num_columns in range(1, num_columns_max+1):
                            try:
                                S_z = (1 / (num_rows - 1)) * (w - 2 * e_1)
                            except ZeroDivisionError:
                                S_z = 0
                            coordinates = find_coordinates(
                                h=h,
                                D_2=D_2,
                                t_1=t_1,
                                e_1=e_1,
                                e_2=e_2,
                                S_z=S_z,
                                S_x=S_x,
                                num_rows=num_rows,
                                num_columns=num_columns
                            )
                            configurations.append(Configuration(coordinates, bolt_type[2]*0.001, D_2, bolt_type[3], fastener_material, lug_material))
    return configurations

def find_S_x(material: str, D_2):
    if materials_list[material]['type'] == 'metal':
        return 2*D_2
    else:
        return 4*D_2

def find_coordinates(h, D_2, t_1, e_1, e_2, S_z, S_x, num_rows, num_columns):
    coordinates_list = []
    x_coord = e_2
    y_coord = 0
    z_coord = e_1
    for i in range(2):
        for j in range(num_columns):
            z_coord = e_1
            for k in range(num_rows):
                coordinates_list.append([x_coord, y_coord, z_coord])
                z_coord += S_z
            x_coord += S_x
        # middle of lug
        x_coord += 2*2*t_1+h+D_2  # two extra t_1 for spacing
    coordinates_list = np.array(coordinates_list)
    return coordinates_list


def find_number_of_rows(material: str, e_1, D_2, w):
    if materials_list[material]['type'] == 'metal':
        m = 2
    else:
        m = 4

    w_rc = 2*e_1 + m*D_2
    n = 2
    while True:
        if w_rc > w:
            n = n-1
            break
        else:
            w_rc = w_rc + m*D_2
            n = n+1
    return n


def read_table(filepath):
    table = pd.read_csv(filepath)
    return table.values.tolist()

generate_configurations()
coordinates =find_coordinates(
    h=1,
    D_2=2,
    t_1=1,
    e_1=1,
    e_2=1,
    S_z=1,
    S_x=1,
    num_rows=5,
    num_columns=5
)

#configurations = generate_configurations()
#for configuration in configurations:
#    print(configuration.material, len(configuration.fastener_positions), len(D))