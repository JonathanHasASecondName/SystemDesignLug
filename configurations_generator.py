import pandas as pd
from configuration import Configuration
from config import *

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
        for num_rows in range(1, max_rows):
            for num_columns in range(1, max_columns):
                print(bolt_type[0], num_rows, num_columns)
                # Start defining single configuration
                D_2 = bolt_type[1]
                e_1 = 1.5*D_2
                e_2 = 1.5*D_2
                e_3 = t_1 + 0.5*D_2
                S_x =
                try:
                    S_z = (1/(num_rows-1))*(w-2*e_1)
                except ZeroDivisionError:
                    S_z = 0
                num_fasteners = 2*(num_columns*num_rows)
                fastener_positions = []

                for row in range(num_rows):
                    for column in range(num_columns):
                        x_i = None
                        z_i = None
                        fastener_positions.append((x_i,z_i))

    """
    CODE GOES ABOVE
    """
    return configurations

def find_coordinates(start_x, start_y, h, t1, e_1, e_2)


def read_table(filepath):
    table = pd.read_csv(filepath)
    return table.values.tolist()

generate_configurations()