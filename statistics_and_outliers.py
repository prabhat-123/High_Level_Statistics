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

        

    def shape(self):
        pass


pd = CSVREADER()
pd.read_csv('diabetes.csv')
pd.head(5)




