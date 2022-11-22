import pandas as pd
import config
import numpy as np
import time

class GraphReader:
    def __init__(self):
        self.cache = {'tension': None,
                      'shear': None}

    def get_datapoint(
            self,
            load_case,
            t_over_D=None,
            e_over_D=None,
            line_number=None,
            Aav_over_Abr=None,
            **kwargs
    ):
        if self.cache[load_case] is None:
            if load_case == 'shear':
                self.read_table(load_case, config.shear_factors_path)
            elif load_case == 'tension':
                self.read_table(load_case, config.tension_factors_path)
        datapoint = None
        if t_over_D is not None and e_over_D is not None and load_case == 'shear':
            datapoint = self.get_datapoint_from_table(load_case, t_over_D, e_over_D)
        elif line_number is not None and Aav_over_Abr is not None and load_case == 'tension':
            datapoint = self.get_datapoint_from_table(load_case, line_number, Aav_over_Abr)
        return datapoint

    def get_datapoint_from_table(self, load_case, key, x_coordinate):
        try:
            table = np.array(self.cache[load_case][key])
        except KeyError:
            return None
        if x_coordinate >= 0:
            for i, raw_datapoint in enumerate(table):
                if raw_datapoint[0] > x_coordinate:
                    x_start = table[i-1][0]
                    x_end = raw_datapoint[0]
                    y_start = table[i-1][1]
                    y_end = raw_datapoint[1]
                    return self.interpolate(x_coordinate, x_start, x_end, y_start, y_end)

    def read_table(self, load_case, filepath):
        """
        :return: a table
        """
        table = pd.read_excel(filepath, sheet_name=None)
        self.cache[load_case] = table

    def interpolate(self, value, x_start, x_end, y_start, y_end):
        slope = (y_end-y_start)/(x_end-x_start)
        return y_start + slope*(value-x_start)


graph_reader = GraphReader()
time_zero = time.time()
print(graph_reader.get_datapoint(
    load_case='tension',
    line_number='9',
    Aav_over_Abr=1
))
#Hello