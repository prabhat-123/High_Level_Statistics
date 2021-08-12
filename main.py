from statistics_and_outliers import CSVREADER
import os

root_dir = os.getcwd()
data_path = os.path.join(root_dir,'datasets')
csv_data = CSVREADER(os.path.join(data_path,'tips.csv'))
csv_data.read_csv()
columns = csv_data.columns()
print(csv_data.count())
print(csv_data.columns())
print(csv_data.shape())
[rows_numerical, columns_numerical, rows_categorical, columns_categorical] = csv_data.getColumns()
print(csv_data.describe())
print(csv_data.head(head_index_num = 5))
print(csv_data.visualize_outlier())
columns, columns_numerical, columns_categorical = csv_data.separateColumns()
print(csv_data.tabulating_cat_statistics())