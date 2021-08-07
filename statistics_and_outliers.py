import csv

class CSVREADER:
    def __init__(self):
        pass

    def read_csv(self,filename):
        self.filename = filename
        csv_file = open(filename,'r')
        csv_reader = csv.reader(csv_file)
        return csv_reader


    def head(self,i):
        self.i = i
        csv_reader = self.read_csv(self.filename)
        fields = next(csv_reader)
        rows = []
        for row in csv_reader:
            rows.append(row)
        # printing the field names
        print('Field names are:' + ', '.join(field for field in fields))
        #  printing first 5 rows
        print('\n First {} rows are:\n'.format(i))
        for row in rows[:i]:
            print(','.join(item for item in row))

    def getColumns(self):
        columns_numerical = defaultdict(list)
        columns_categorical = defaultdict(list)
        csv_reader = csv.DictReader(open(self.filename, 'r'))
        for row in csv_reader:
          for (k, v) in row.items():
            if k in ['age', 'bmi', 'children', 'charges']:
              columns_numerical[k].append(v)
            else:
              columns_categorical[k].append(v)
        return columns_numerical, columns_categorical

    def shape(self):
        pass

class Outliers:
  def __init__(self, numerical_columns):
    self.numerical_columns = numerical_columns
    self.outliers_std = {}
    self.outliers_zscore = {}

  def stdOutlier(self):
    for key, value in self.numerical_columns.items():
      data = np.array(list(map(float, value)))
      data_mean, data_std = np.mean(data), np.std(data)
      cut_off = data_std * 3
      lower, upper = data_mean - cut_off, data_mean + cut_off
      outliers = [x for x in data if x < lower or x > upper]
      self.outliers_std[key] = round(((len(outliers)/len(value)) * 100), 3)

    return self.outliers_std

  # identify outliers with interquartile range
  def zscoreOutlier(self):
    for key, value in self.numerical_columns.items():
      data = np.array(list(map(float, value)))
      q25, q75 = np.percentile(data, 25), np.percentile(data, 75)
      iqr = q75 - q25
      cut_off = iqr * 1.5
      lower, upper = q25 - cut_off, q75 + cut_off
      outliers = [x for x in data if x < lower or x > upper]
      outliers_removed = [x for x in data if x >= lower and x <= upper]
      self.outliers_zscore[key] = round(((len(outliers)/len(value)) * 100), 3)
    return self.outliers_zscore


pd = CSVREADER()
pd.read_csv('diabetes.csv')
pd.head(5)

outliers = Outliers(cols_numerical)
print(outliers.stdOutlier())
print(outliers.zscoreOutlier())
