import csv
import numpy as np

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


    
    def std(self):
        pass
    


    def describe(self):
        pass


pd = CSVREADER('diabetes.csv')
columns = pd.columns()
pd.head(5)
print(pd.shape())
print(pd.mean('Age'))
# print(pd.mean(columns))
print(pd.median('Age'))
print(pd.minimum('Age'))
print(pd.maximum('Age'))