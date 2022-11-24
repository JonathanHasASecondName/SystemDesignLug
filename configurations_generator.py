import pandas as pd
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
    max_columns = 3 + 1
    """
    CODE GOES BELOW
    """

    # NB: num_rows and num_columns
    for bolt_type in bolt_types:
        max_rows = max_columns # Change this later
        D_2 = bolt_type[1]
        e_1 = 1.5 * D_2
        e_2 = 1.5 * D_2
        e_3 = t_1 + 0.5 * D_2
        num_rows = find_number_of_rows('steel', e_1, D_2, w)
        num_columns = 1
        try:
            S_z = (1 / (num_rows - 1)) * (w - 2 * e_1)
        except ZeroDivisionError:
            S_z = 0
        coordinates = find_coordinates(
            h=h,
            t_1=t_1,
            e_1=e_1,
            e_2=e_2,
            S_z=S_z,
            S_x=2*D_2,
            num_rows=num_rows,
            num_columns=num_columns
        )

    """
    CODE GOES ABOVE
    """
    return configurations

def find_coordinates(h, t_1, e_1, e_2, S_z, S_x, num_rows, num_columns):
    coordinates_list = []
    x_coord = e_2
    y_coord = 0
    z_coord = e_1
    e_3 =
    for i in range(2):
        for j in range(num_columns):
            z_coord = e_1
            for k in range(num_rows):
                coordinates_list.append([x_coord, y_coord, z_coord])
                z_coord += S_z
            x_coord += S_x
        #middle of lug
        x_coord += 2*2*t_1+h+e_3 # two extra t_1 for spacing
    return coordinates_list


def find_number_of_rows(material: str, e_1, D_2, w):
    if materials_list[material]['type'] == 'metal':
        m = 2
    else:
        m=4

    w_rc = 2*e_1 + m*D_2
    n=2
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

