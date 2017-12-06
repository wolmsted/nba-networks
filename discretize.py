import pandas as pd
import numpy as np


def main():
	train = pd.read_csv('csv_files/train.csv')
	test = pd.read_csv('csv_files/test.csv')
	validate = pd.read_csv('csv_files/validate.csv')

	datasets = [train, test, validate]

	# max value in each bucket
	max_values = {
		'AST' : 15,
		'PTS' : 30,
		'REB' : 15,
		'FG3A' : 12,
		'FG3M' : 9,
		'FGA' : 30,
		'FGM' : 15,
		'FTA' : 24,
		'FTM' : 15,
		'TO' : 9,
		'BLK' : 6,
		'STL' : 6,
		'MIN' : 42,
		'PF' : 6
	}

	positions = {'C': 1, 'F': 2, 'G': 3}
	for i in range(len(datasets)):
		datasets[i] = datasets[i].drop('NAME', axis=1).drop('TEAM_CITY', axis=1).drop('DATE', axis=1).drop('DREB', axis=1) \
		.drop('FG3_PCT', axis=1).drop('FG_PCT', axis=1).drop('FT_PCT', axis=1).drop('OREB', axis=1)
		for j, row in datasets[i].iterrows():
			if row['AST'] is None or np.isnan(row['AST']):
				continue
			for key in max_values.keys():
				datasets[i].set_value(j, key, discretize(max_values, key, row[key])) 
			if row['START_POSITION'] not in positions:
				datasets[i].set_value(j, 'START_POSITION', 4)
			else:
				datasets[i].set_value(j, 'START_POSITION', positions[row['START_POSITION']])

	datasets[0].to_csv('discretized_files/train.csv', index=False)
	datasets[1].to_csv('discretized_files/test.csv', index=False)
	datasets[2].to_csv('discretized_files/validate.csv', index=False)

def discretize(max_values, stat, value):
	max_val = max_values[stat]
	buckets = [max_val / 3, max_val / 2, max_val]
	if value < buckets[0]:
		return 1
	elif value < buckets[1]:
		return 2
	elif value < buckets[2]:
		return 3
	else:
		return 4



if __name__ == '__main__':
    main()
