import pandas as pd

data = pd.read_csv('sector_calc_input.txt')

data['num_cells'] = data['cell_id'].str.extract('(\d+)')
data['sector'] = data['num_cells'].astype(int)
data.loc[data['band'] == 3, 'sector'] = (data['sector'] / 2).astype(int)
data['site'] = data['cell_id'].str.extract('([a-zA-Z]+)')
data['sector'] = ("1-" + data['sector'].astype(str)).astype(str)
data = data[['cell_id','azimuth','band','sector']]

print(data)
data.to_csv('output.txt', index=False)
