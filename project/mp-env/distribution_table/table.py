import pandas as pd
import numpy as np


class groupedTable:

    def __init__(self, name: str, dataframe):
        self.name = name
        self.df = dataframe
        self.simple_range = self.df.max() - self.df.min()
        self.length = self.df.shape[0]
        self.column_name = self.df.columns[0]
        self.number_classes = self.calculate_number_classes()
        self.amplitude = self.calculate_amplitude()
        self.array_intervals = self.generate_intervals()
        self.array_abs_freq = self.generate_abs_freq()
        self.array_acum_freq = self.generate_acum_freq()
        self.array_rel_abs_freq = self.generate_rel_abs_freq()
        self.array_rel_acum_freq = self.generate_rel_acum_freq()
        self.array_class_mark = self.generate_class_mark()
        self.array_percentage = self.generate_percentage_col()
        self.table = self.generate_table()

    def calculate_number_classes(self):
        self.number_classes = int(np.ceil(np.sqrt(self.length))) if self.length < 30 else int(
            np.ceil(1 + (3.322 * np.log10(self.length))))
        return self.number_classes

    def calculate_amplitude(self):
        self.amplitude = self.simple_range / self.number_classes
        return self.amplitude

    def generate_intervals(self):
        self.array_intervals = np.empty((self.number_classes, 2), dtype=float)
        self.array_intervals[0][0] = self.df.min().iloc[0]
        self.array_intervals[0][1] = self.df.min().iloc[0] + \
            self.amplitude.iloc[0]
        aux_col1 = self.df.min().iloc[0]
        aux_col2 = self.df.min().iloc[0] + self.amplitude.iloc[0]

        for i in range(1, self.number_classes):
            aux_col1 += self.amplitude
            self.array_intervals[i][0] = aux_col1.iloc[0]

        for i in range(1, self.number_classes):
            aux_col2 += self.amplitude
            self.array_intervals[i][1] = aux_col2.iloc[0]

        return self.array_intervals

    # Note: the last interval needs to be closed on both sides
    def count_last_interval(self, array, interval):
        counts = 0

        for i in array:
            if np.float32(interval[0]) <= np.float32(i) <= np.float32(interval[1]):
                counts += 1

        return counts

    # This function only counts the frequency of a value given an interval
    def count_range_in_list(self, array, interval):
        counts = 0

        for i in array:
            if np.float32(i) != np.float32(array[-1]):
                if np.float32(interval[0]) <= np.float32(i) < np.float32(interval[1]):
                    counts += 1

        return counts

    def generate_abs_freq(self):
        self.array_abs_freq = np.empty((self.number_classes), dtype=int)

        for i in range(self.number_classes):
            self.array_abs_freq[i] = self.count_range_in_list(
                self.df[self.column_name].values, self.array_intervals[i])

        self.array_abs_freq[-1] = self.count_last_interval(
            self.df[self.column_name].values, self.array_intervals[-1])

        return self.array_abs_freq

    def generate_acum_freq(self):
        self.array_acum_freq = np.empty((self.number_classes), dtype=int)
        aux = 0

        for i in range(self.number_classes):
            aux += self.array_abs_freq[i]
            self.array_acum_freq[i] = aux

        return self.array_acum_freq

    def generate_rel_abs_freq(self):
        self.array_rel_abs_freq = self.array_abs_freq / self.length

        return self.array_rel_abs_freq

    def generate_rel_acum_freq(self):
        self.array_rel_acum_freq = self.array_acum_freq / self.length

        return self.array_rel_acum_freq

    def generate_class_mark(self):
        self.array_class_mark = np.empty((self.number_classes), dtype=float)

        for i in range(self.number_classes):
            self.array_class_mark[i] = np.sum(
                self.array_intervals[i], dtype=float) / 2

        return self.array_class_mark

    def generate_percentage_col(self):
        self.array_percentage = self.array_rel_abs_freq * 100

        return self.array_percentage

    # Takes all the arrays and turns it into a dataframe
    def generate_table(self):
        table_dic = {
            self.column_name: np.arange(1, self.number_classes + 1, dtype=int),
            'Intervals': [str(np.around(i, 2)) for i in self.array_intervals],
            'Absolute frequency': self.array_abs_freq,
            'Cumulative frequency': self.array_acum_freq,
            'Absolute relative frequency': self.array_rel_abs_freq,
            'Cumulative relative frequency': self.array_rel_acum_freq,
            'Class mark': self.array_class_mark,
            'Percentage': self.array_percentage
        }

        self.table = pd.DataFrame(data=table_dic)
        self.table = self.table.set_index(self.column_name)

        return self.table
