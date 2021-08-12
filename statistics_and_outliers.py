import csv
import ast
from pathlib import Path
from collections import Counter
from collections import defaultdict

import numpy as np
from prettytable import PrettyTable

class CSVREADER:
    def __init__(self, filename):
        self.filename = filename
        self.outliers_std = {}
        self.outliers_zscore = {}
        self.columns_numerical = defaultdict(list)
        self.columns = defaultdict(list)
        self.columns_categorical = defaultdict(list)

    def csv_reader(self):
        csv_file = open(self.filename,'r')
        csv_reader = csv.DictReader(csv_file)
        return csv_reader

    def read_csv(self):
        csv_file = open(self.filename,'r')
        csv_reader = csv.reader(csv_file)
        return csv_reader

    def columns(self):
        csv_reader = self.read_csv()
        fields = next(csv_reader)
        columns = [field for field in fields]
        return columns


    def rows(self):
        csv_reader = self.read_csv()
        rows = []
        for row in csv_reader:
            rows.append(row)
        return rows

    def getColumns(self):
        rows = self.rows()
        columns = self.columns()
        rows = np.array(rows[1:])
        rows_separation = np.split(rows,len(columns),axis=1)
        rows_numerical = []
        columns_numerical = []
        rows_categorical = []
        columns_categorical = []
        for i in range(len(columns)):
            try:
                rows_numerical.append([float(a) for a in rows_separation[i]])
                columns_numerical.append(columns[i])
            except:
                rows_categorical.append(str(rows_separation[i]))
                columns_categorical.append(columns[i])
        return rows_numerical,columns_numerical,rows_categorical,columns_categorical


    def head(self,i):
        self.i = i
        columns = self.columns()
        rows = self.rows()
        rows = rows[1:i+1]
        x = PrettyTable()
        x.field_names = columns
        x.add_rows(rows)
        return x


    def shape(self):
        csv_reader = self.read_csv()
        fields = next(csv_reader)
        rows = []
        for row in read_csv:
            rows.append(row)
        return(len(rows),len(fields))


    def count(self):
        non_missing_counts= None
        rows_numerical,columns_numerical,rows_categorical,columns_categorical= self.getColumns()
        rows = np.array(rows_numerical).astype(np.float)
        split_rows = np.split(rows,len(columns_numerical),axis=0)
        non_missing_counts = []
        for split in split_rows:
            nmc = np.count_nonzero(~np.isnan(split))
            non_missing_counts.append(nmc)
        return non_missing_counts


    def mean(self):
        [rows_numerical,columns_numerical,rows_categorical,columns_categorical] = self.getColumns()
        mean = np.nanmean(rows_numerical,axis=1)
        return np.round(mean,decimals = 2)

    def median(self):
        [rows_numerical,columns_numerical,rows_categorical,columns_categorical] = self.getColumns()
        median = np.nanmedian(rows_numerical,axis=1)
        return np.round(median,decimals=2)

    def minimum(self):
        [rows_numerical,columns_numerical,rows_categorical,columns_categorical] = self.getColumns()
        minimum = np.nanmin(rows_numerical,axis=1)
        return minimum


    def maximum(self):
        [rows_numerical,columns_numerical,rows_categorical,columns_categorical] = self.getColumns()
        maximum = np.nanmax(rows_numerical,axis=1)
        return maximum

    def standard_deviation(self):
        [rows_numerical,columns_numerical,rows_categorical,columns_categorical] = self.getColumns()
        standard_deviation = np.nanstd(rows_numerical,axis=1)
        return np.round(standard_deviation,decimals=2)


    def first_quantile(self):
        [rows_numerical,columns_numerical,rows_categorical,columns_categorical] = self.getColumns()
        first_quantile = np.nanpercentile(rows_numerical,25,axis=1)
        return np.round(first_quantile,decimals=2)

    def third_quantile(self):
        [rows_numerical,columns_numerical,rows_categorical,columns_categorical] = self.getColumns()
        third_quantile = np.nanpercentile(rows_numerical,75,axis=1)
        return np.round(third_quantile,decimals=2)

    def describe(self):
        rows_numerical,columns_numerical,rows_categorical,columns_categorical = self.getColumns()
        count = self.count()
        mean = self.mean()
        median = self.median()
        minimum = self.minimum()
        maximum = self.maximum()
        standard_deviation = self.standard_deviation()
        first_quantile = self.first_quantile()
        third_quantile = self.third_quantile()
        table = PrettyTable()
        tabltable.add_column("Filed name",columns_numerical)
        table.add_column("Counts",count)
        table.add_column("Mean",mean)
        table.add_column("Median",median)
        table.add_column("Minimum",minimum)
        table.add_column("Maximum",maximum)
        table.add_column("Standard Deviation",standard_deviation)
        table.add_column("First Quantile",first_quantile)
        table.add_column("Third Quantile",third_quantile)
        return table

    def zscoreOutlier(self):
        rows_numerical,columns_numerical,rows_categorical,columns_categorical = self.getColumns()
        data_mean = np.nanmean(rows_numerical,axis=1)
        data_std = np.nanstd(rows_numerical,axis=1)
        cut_off = data_std * 3
        lower = data_mean - cut_off
        upper = data_mean + cut_off
        zscore_outlier = []
        for i in range(len(rows_numerical)):
            outliers = [x for x in rows_numerical[i] if x < lower[i] or x > upper[i]]
            outliers_percent = round(((len(outliers)/len(rows_numerical[i])) * 100), 3)
            zscore_outlier.append(outliers_percent)
        return zscore_outlier

    def iqrOutlier(self):
        rows_numerical,columns_numerical,rows_categorical,columns_categorical = self.getColumns()
        q1 = np.nanpercentile(rows_numerical,25,axis=1)
        q3 = np.nanpercentile(rows_numerical,75,axis=1)
        iqr = q3 - q1
        cut_off = iqr * 1.5
        lower = q1 - cut_off
        upper = q3 + cut_off
        iqr_outlier = []
        for i in range(len(rows_numerical)):
            outliers = [x for x in rows_numerical[i] if x < lower[i] or x > upper[i]]
            outliers_percent = round(((len(outliers)/len(rows_numerical[i])) * 100), 3)
            iqr_outlier.append(outliers_percent)
        return iqr_outlier

    def visualize_outlier(self):
        rows_numerical,columns_numerical,rows_categorical,columns_categorical = self.getColumns()
        zscore_outlier = self.ZscoreOutlier()
        iqr_outlier = self.IQROutlier()
        x = PrettyTable()
        x.add_column("Filed name",columns_numerical)
        x.add_column("Z-score Outlier in %",zscore_outlier)
        x.add_column("IQR Outlier in %",iqr_outlier)
        return x

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

    def categoricalStatistics(self):
      columns, columns_numerical, columns_categorical= self.separateColumns()
      count = []
      keys = []
      for key, value in columns_categorical.items():
          keys.append(Counter(value).keys())
          count.append(Counter(value).values())
      return count, keys

    def tabulating_cat_statistics(self):
        counts, keys = pd.categoricalStatistics()
        table     = PrettyTable()
        count = [j for i in counts for j in i ]
        key = [j for i in keys for j in i ]
        table.add_column('Keys', key)
        table.add_column('Count', count)
        return table


    # def iqrOutlier(self):
    #   self.separateColumns()
    #   for key, value in self.columns_numerical.items():
    #     data = np.array(list(map(float, value)))
    #     q25, median, q75 = np.percentile(data, 25), np.percentile(data, 75), np.percentile(data, 75)
    #     iqr = q75 - q25
    #     cut_off = iqr * 1.5
    #     lower, upper = q25 - cut_off, q75 + cut_off
    #     outliers = [x for x in data if x < lower or x > upper]
    #     outliers_removed = [x for x in data if x >= lower and x <= upper]
    #     self.outliers_zscore[key] = round(((len(outliers)/len(value)) * 100), 3)
    #   return self.outliers_zscore

    def save_csv(self):
      self.separateColumns()
      field_names = [key for key, value in columns_numerical.items()]
      field_names.insert(0,'Statistics')
      csvfile = "statistics.csv"
      try:
        with open(csvfile, 'w') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=field_names)
          writer.writeheader()
          for key, value in self.statistics().items():
            value['Statistics'] = key
            writer.writerow(value)
      except IOError:
        print("Error while writing into the file.")

    def tabulating_num_statistics(self):
        z_value = []
        self.separateColumns()
        z_outlier = self.zscoreOutlier()
        i_outlier = self.iqrOutlier()
        zscore_value = list(z_outlier.values())
        iqr_value = list(i_outlier.values())
        count, mean, median, q75, q25, minimum, maximum, std = self.numericalStatistics()
        col_names = [key for key, value in self.columns_numerical.items()]
        print(self.columns_numerical)
        table = PrettyTable()
        table.add_column("Filed name",col_names)
        table.add_column("Count", count)
        table.add_column("Mean",mean)
        table.add_column("Median",median)
        table.add_column("Standard deviation", std)
        table.add_column("Minimum",minimum)
        table.add_column("Maximum",maximum)
        table.add_column("First Quantile",q25)
        table.add_column("Third Quantile",q75)
        table.add_column("Outliers_zscore(%)",zscore_value)
        table.add_column("Outliers_iqr(%)",iqr_value)
        return table

    # def tabulating_cat_statistics(self):
    #   counts, keys = pd.categoricalStatistics()
    #   x = PrettyTable()
    #   count = [j for i in counts for j in i ]
    #   key = [j for i in keys for j in i ]
    #   x.add_column('Keys', key)
    #   x.add_column('Count', count)
    #   return x

path = Path('./insurance.csv')
pd = CSVREADER(path)
print("Tabulating the numerical statistics.")
print(pd.tabulating_num_statistics())

print("Tabularing the categorical statistics.")
print(pd.tabulating_cat_statistics())
print('Printing the percentage of outliers using zscore:')
print(pd.zscoreOutlier())

print('Printing the percentage of outlers using IQR: ')
print(pd.iqrOutlier())