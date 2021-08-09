import csv
import numpy as np
from collections import defaultdict
from prettytable import PrettyTable
from collections import Counter

class CSVREADER:
    def __init__(self, filename):
        self.filename = filename
        self.outliers_std = {}
        self.outliers_zscore = {}

    def csv_reader(self):
        csv_file = open(self.filename,'r')
        csv_reader = csv.DictReader(csv_file)
        return csv_reader

    def get_columns(self):
        csv_reader = self.csv_reader()
        columns = [field for field in next(csv_reader)]
        return columns

    def get_rows(self):
        read_csv = self.csv_reader()
        rows = []
        for row in read_csv:
            rows.append(row)
        return rows

    def separateColumns(self):
        columns_numerical = defaultdict(list)
        columns = defaultdict(list)
        columns_categorical = defaultdict(list)
        csv_reader = self.csv_reader()

        for row in csv_reader:
          for (k, v) in row.items():
            try:
              a = float(v)
              columns_numerical[k].append(a)
            except:
              columns_categorical[k].append(v)
            finally:
              columns[k].append(v)
        return columns, columns_numerical, columns_categorical


    def dictStatistics(self):
        columns, columns_numerical, columns_categorical= self.separateColumns()
        stats = {'Mean': {}, 'Median': {}, 'q75': {}, 'q25': {}, 'Minimum': {}, 'Maximum':{}}
        for key, value in columns_numerical.items():
            data = np.array(list(map(float, value)))
            stats['Mean'][key], mean = np.round(np.mean(data))
            stats['Median'][key], median = np.percentile(data, 50)
            stats['q75'][key], q75 = np.percentile(data, 75)
            stats['q25'][key], q25 = np.percentile(data, 25)
            stats['Minimum'][key], minimum = np.min(data)
            stats['Maximum'][key], maximum = np.max(data)
        return  stats

    def numericalStatistics(self):
        count, mean, median, q75, q25, minimum, maximum, std = ([] for i in range(8))
        columns, columns_numerical, columns_categorical= self.separateColumns()
        for key, value in columns_numerical.items():
            data = np.array(list(map(float, value)))
            count.append(len(data))
            mean.append(np.round(np.mean(data), 3))
            median.append(np.round(np.percentile(data, 50), 3))
            q75.append(np.round(np.percentile(data, 75), 3))
            q25.append(np.round(np.percentile(data, 25), 3))
            minimum.append(np.round(np.min(data), 3))
            maximum.append(np.round(np.max(data), 3))
            std.append(np.round(np.std(data), 3))
        return count, mean, median, q75, q25, minimum, maximum, std

    def categoricalStatistics(self):
      columns, columns_numerical, columns_categorical= self.separateColumns()
      count = []
      keys = []
      for key, value in columns_categorical.items():
          keys.append(Counter(value).keys())
          count.append(Counter(value).values())
      return count, keys

    def zscoreOutlier(self):
      columns, numerical_cols, categorcal_cols = self.separateColumns()
      for key, value in numerical_cols.items():
        data = np.array(list(map(float, value)))
        data_mean, data_std = np.mean(data), np.std(data)
        cut_off = data_std * 3
        lower, upper = data_mean - cut_off, data_mean + cut_off
        outliers = [x for x in data if x < lower or x > upper]
        self.outliers_std[key] = round(((len(outliers)/len(value)) * 100), 3)
      return self.outliers_std


    def iqrOutlier(self):
      columns, numerical_cols, categorcal_cols = self.separateColumns()
      for key, value in numerical_cols.items():
        data = np.array(list(map(float, value)))
        q25, median, q75 = np.percentile(data, 25), np.percentile(data, 75), np.percentile(data, 75)
        iqr = q75 - q25
        cut_off = iqr * 1.5
        lower, upper = q25 - cut_off, q75 + cut_off
        outliers = [x for x in data if x < lower or x > upper]
        outliers_removed = [x for x in data if x >= lower and x <= upper]
        self.outliers_zscore[key] = round(((len(outliers)/len(value)) * 100), 3)
      return self.outliers_zscore

    def save_csv(self):
      columns, numerical_cols, categorcal_cols = self.separateColumns()
      field_names = [key for key, value in numerical_cols.items()]
      field_names.insert(0,'Statistics')
      csvfile = "/content/drive/MyDrive/Datasets_learning_kaggle/statistics.csv"
      try:
        with open(csvfile, 'w') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=field_names)
          writer.writeheader()
          for key, value in self.statistics().items():
            value['Statistics'] = key
            writer.writerow(value)
      except IOError:
        print("Input Output Error")

    def tabulating_num_statistics(self):
        columns, numerical_cols, categorcal_cols = self.separateColumns()
        count, mean, median, q75, q25, minimum, maximum, std = self.numericalStatistics()
        col_names = [key for key, value in numerical_cols.items()]
        x = PrettyTable()
        x.add_column("Filed name",col_names)
        x.add_column("Count", count)
        x.add_column("Mean",mean)
        x.add_column("Median",median)
        x.add_column("Standard deviation", std)
        x.add_column("Minimum",minimum)
        x.add_column("Maximum",maximum)
        x.add_column("First Quantile",q25)
        x.add_column("Third Quantile",q75)
        return x

    def tabulating_cat_statistics(self):
      counts, keys = pd.categoricalStatistics()
      x = PrettyTable()
      count = [j for i in counts for j in i ]
      key = [j for i in keys for j in i ]
      x.add_column('Keys', key)
      x.add_column('Count', count)
      return x

pd = CSVREADER('/content/drive/MyDrive/Datasets_learning_kaggle/insurance.csv')
print("Tabulating the numerical statistics.")
print(pd.tabulating_num_statistics())
print()
print("Tabularing the categorical statistics.")
print(pd.tabulating_cat_statistics())
print()
print('Printing the percentage of outliers using zscore:')
print(pd.zscoreOutlier())
print()
print('Printing the percentage of outlers using IQR: ')
print(pd.iqrOutlier())
