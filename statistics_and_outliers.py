import csv
import numpy as np
from collections import defaultdict

class CSVREADER:
    def __init__(self, filename):
        self.filename = filename
        self.fields = []
        self.outliers_std = {}
        self.outliers_zscore = {}
        #values needs to be the ones of the actual calculation, this is the dummy value.
        self.final_stats  = [{'Statistics': 'mean', 'age': 10, 'bmi': 20, 'children': 15, 'charges': 100}, {'Statistics': 'median', 'age': 15, 'bmi': 2, 'children': 20, 'charges': 105}]



    def csv_reader(self):
        csv_file = open(self.filename,'r')
        csv_reader = csv.DictReader(csv_file)
        return csv_reader

    def get_header(self):
        csv_reader = self.csv_reader()
        self.fields = [field for field in next(csv_reader)]
        return self.fields

    def getColumns(self):
        columns_numerical = defaultdict(list)
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
        return columns_numerical, columns_categorical

    def stdOutlier(self):
      numerical_cols, categorcal_cols = self.getColumns()
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
      numerical_cols, categorcal_cols = self.getColumns()
      for key, value in numerical_cols.items():
        data = np.array(list(map(float, value)))
        q25, q75 = np.percentile(data, 25), np.percentile(data, 75)
        iqr = q75 - q25
        cut_off = iqr * 1.5
        lower, upper = q25 - cut_off, q75 + cut_off
        outliers = [x for x in data if x < lower or x > upper]
        outliers_removed = [x for x in data if x >= lower and x <= upper]
        self.outliers_zscore[key] = round(((len(outliers)/len(value)) * 100), 3)
      return self.outliers_zscore

    def visualization(self):
      numerical_cols, categorcal_cols = self.getColumns()
      field_names = [keys for keys, value in numerical_cols.items()]
      field_names.insert(0,'Statistics')
      try:
        with open('/content/drive/MyDrive/Datasets_learning_kaggle/Statistics.csv', 'w') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=field_names)
          writer.writeheader()
          for data in self.final_stats:
            writer.writerow(data)
      except IOError:
        print("Input Output Error")

    def shape(self):
        pass

pd = CSVREADER('/content/drive/MyDrive/Datasets_learning_kaggle/insurance.csv')
# pd.csv_reader()
# print(pd.zscoreOutlier())
# print(pd.stdOutlier())
pd.visualization()
