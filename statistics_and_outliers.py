import csv
import numpy as np
from prettytable import PrettyTable

class CSVREADER:
    def __init__(self,filename):
        self.filename = filename
        

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


    def head(self,i):
        self.i = i
        columns = self.columns()
        rows = self.rows()
        print('\n First {} rows are:\n'.format(i))
        for row in rows[:i+1]:
            print(','.join(item for item in row))
   

    def shape(self):
        csv_reader = self.read_csv()
        fields = next(csv_reader)
        rows = []
        for row in csv_reader:
            rows.append(row)
        return(len(rows),len(fields))



    def info(self):
        pass


    def mean(self,cols):
        self.cols = cols
        columns = self.columns()
        rows = self.rows()
        mean=None
        if type(cols).__name__ == "str":
            try:
                index = columns.index(cols)
                rows = np.array(rows[1:]).astype(np.float)
                extract_rows = rows[:,index]
                mean = np.mean(extract_rows,axis=0)
            except Exception as e:
                print("{} not found in the columns".format(cols))
        elif type(cols).__name__ == "list" and cols==columns:
            rows = np.array(rows[1:]).astype(np.float)
            mean = np.mean(rows,axis=0)
        else:
            print("Other data types are not allowed for cols")
        return mean



    def median(self,cols):
        self.cols = cols
        columns = self.columns()
        rows = self.rows()
        median=None
        if type(cols).__name__ == "str":
            try:
                index = columns.index(cols)
                rows = np.array(rows[1:]).astype(np.float)
                extract_rows = rows[:,index]
                median = np.median(extract_rows,axis=0)
            except Exception as e:
                print("{} not found in the columns".format(cols))
        elif type(cols).__name__ == "list" and cols==columns:
            rows = np.array(rows[1:]).astype(np.float)
            median= np.median(rows,axis=0)
        else:
            print("Other data types are not allowed for cols")
        return median


    def minimum(self,cols):
        self.cols = cols
        columns = self.columns()
        rows = self.rows()
        min=None
        if type(cols).__name__ == "str":
            try:
                index = columns.index(cols)
                rows = np.array(rows[1:]).astype(np.float)
                extract_rows = rows[:,index]
                min = np.min(extract_rows,axis=0)
            except Exception as e:
                print("{} not found in the columns".format(cols))
        elif type(cols).__name__ == "list" and cols==columns:
            rows = np.array(rows[1:]).astype(np.float)
            min= np.min(rows,axis=0)
        else:
            print("Other data types are not allowed for cols")
        return min

    
    def maximum(self,cols):
        self.cols = cols
        columns = self.columns()
        rows = self.rows()
        max=None
        if type(cols).__name__ == "str":
            try:
                index = columns.index(cols)
                rows = np.array(rows[1:]).astype(np.float)
                extract_rows = rows[:,index]
                max = np.max(extract_rows,axis=0)
            except Exception as e:
                print("{} not found in the columns".format(cols))
        elif type(cols).__name__ == "list" and cols==columns:
            rows = np.array(rows[1:]).astype(np.float)
            max= np.max(rows,axis=0)
        else:
            print("Other data types are not allowed for cols")
        return max


    
    def std(self,cols):
        self.cols = cols
        columns = self.columns()
        rows = self.rows()
        std_deviation=None
        if type(cols).__name__ == "str":
            try:
                index = columns.index(cols)
                rows = np.array(rows[1:]).astype(np.float)
                extract_rows = rows[:,index]
                std_deviation = np.std(extract_rows,axis=0)
            except Exception as e:
                print("{} not found in the columns".format(cols))
        elif type(cols).__name__ == "list" and cols==columns:
            rows = np.array(rows[1:]).astype(np.float)
            std_deviation= np.std(rows,axis=0)
        else:
            print("Other data types are not allowed for cols")
        return std_deviation

    
    def first_quantile(self,cols):
        self.cols = cols
        columns = self.columns()
        rows = self.rows()
        q1=None
        if type(cols).__name__ == "str":
            try:
                index = columns.index(cols)
                rows = np.array(rows[1:]).astype(np.float)
                extract_rows = rows[:,index]
                q1 = np.percentile(extract_rows,25,axis=0)
            except Exception as e:
                print("{} not found in the columns".format(cols))
        elif type(cols).__name__ == "list" and cols==columns:
            rows = np.array(rows[1:]).astype(np.float)
            q1= np.percentile(rows,25,axis=0)
        else:
            print("Other data types are not allowed for cols")
        return q1




    def third_quantile(self,cols):
        self.cols = cols
        columns = self.columns()
        rows = self.rows()
        q3=None
        if type(cols).__name__ == "str":
            try:
                index = columns.index(cols)
                rows = np.array(rows[1:]).astype(np.float)
                extract_rows = rows[:,index]
                q3 = np.percentile(extract_rows,75,axis=0)
            except Exception as e:
                print("{} not found in the columns".format(cols))
        elif type(cols).__name__ == "list" and cols==columns:
            rows = np.array(rows[1:]).astype(np.float)
            q3= np.percentile(rows,75,axis=0)
        else:
            print("Other data types are not allowed for cols")
        return q3
        

    


    def describe(self,cols):
        self.cols = cols
        mean = self.mean(cols)
        median = self.median(cols)
        minimum = self.minimum(cols)
        maximum = self.maximum(cols)
        standard_deviation = self.std(cols)
        first_quantile = self.first_quantile(cols)
        third_quantile = self.third_quantile(cols)
        x = PrettyTable()
        x.add_column("Filed name",cols)
        x.add_column("Mean",mean)
        x.add_column("Median",median)
        x.add_column("Minimum",minimum)
        x.add_column("Maximum",maximum)
        x.add_column("Standard Deviation",standard_deviation)
        x.add_column("First Quantile",first_quantile)
        x.add_column("Third Quantile",third_quantile)
        return x



pd = CSVREADER('diabetes.csv')
columns = pd.columns()
pd.head(5)
print(pd.shape())
print(pd.describe(columns))
# print(pd.mean('Age'))
# print(pd.median('Age'))
# print(pd.minimum('Age'))
# print(pd.maximum('Age'))
# print("Mean is {}".format(pd.mean(columns)))
# print("Median is {}".format(pd.median(columns)))
# print("Minimum value is {}".format(pd.minimum(columns)))
# print("Maximum value is {}".format(pd.maximum(columns)))

# print("Standard deviation is {}".format(pd.std(columns)))
# print("First quantile is {}".format(pd.first_quantile(columns)))
# print("Third quantile is {}".format(pd.third_quantile(columns)))





