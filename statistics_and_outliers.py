
import csv
import numpy as np
from collections import defaultdict
from prettytable import PrettyTable

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

    def rows(self):
        read_csv = self.csv_reader()
        rows = []
        for row in read_csv:
            rows.append(row)
        return rows

    def getColumns(self):
        columns_numerical = defaultdict(list)
        columns = defaultdict(list)
        columns_categorical = defaultdict(list)
        csv_reader = self.csv_reader()
        self.fields = [field for field in next(csv_reader)]
        # print('Field names are: ' + ', '.join(field for field in self.fields))
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

    def count(self):
        count_dict = {}
        columns, columns_numerical, columns_categorical= self.getColumns()
        for key, value in columns.items():
            count_dict[key] = len(value)
        return count_dict

    def statistics(self):
        columns, columns_numerical, columns_categorical= self.getColumns()
        stats = {'Mean': {}, 'Median': {}, 'q75': {}, 'q25': {}, 'Minimum': {}, 'Maximum':{}}
        for key, value in columns_numerical.items():
            data = np.array(list(map(float, value)))
            stats['Mean'][key] = np.round(np.mean(data))
            stats['Median'][key] = np.percentile(data, 50)
            stats['q75'][key] = np.percentile(data, 75)
            stats['q25'][key] = np.percentile(data, 25)
            stats['Minimum'][key] = np.min(data)
            stats['Maximum'][key] = np.max(data)
        return  stats


    def stdOutlier(self):
      columns, numerical_cols, categorcal_cols = self.getColumns()
      for key, value in numerical_cols.items():
        data = np.array(list(map(float, value)))
        data_mean, data_std = np.mean(data), np.std(data)
        cut_off = data_std * 3
        lower, upper = data_mean - cut_off, data_mean + cut_off
        outliers = [x for x in data if x < lower or x > upper]
        self.outliers_std[key] = round(((len(outliers)/len(value)) * 100), 3)
      return self.outliers_std


    # identify outliers with interquartile range
    def zscoreOutlier(self):
      columns, numerical_cols, categorcal_cols = self.getColumns()
      for key, value in numerical_cols.items():
        data = np.array(list(map(float, value)))
        q25, median, q75 = np.percentile(data, 25), np.percentile(data, 75), np.percentile(data, 75)
        iqr = q75 - q25
        cut_off = iqr * 1.5
        lower, upper = q25 - cut_off, q75 + cut_off
        outliers = [x for x in data if x < lower or x > upper]
        outliers_removed = [x for x in data if x >= lower and x <= upper]
        self.outliers_zscore[key] = round(((len(outliers)/len(value)) * 100), 3)
      return q25, median, q75, self.outliers_zscore

    def save_csv(self):
      columns, numerical_cols, categorcal_cols = self.getColumns()
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

    # def visualization(self):
    #     columns, numerical_cols, categorcal_cols = self.getColumns()
    #     stats = self.statistics()
    #     x = Prettytable()
    #     for i in range(6):
    #       x.add_column()

pd = CSVREADER('/content/drive/MyDrive/Datasets_learning_kaggle/insurance.csv')
pd.statistics()
