import pandas as pd
import numpy as np

def main():
	train = pd.read_csv('discretized_files/train.csv')
	test = pd.read_csv('discretized_files/test.csv')
	validate = pd.read_csv('discretized_files/validate.csv')

	datasets = [train, test, validate]

	# outcome is 1 for home team win, 0 otherwise
	columns = [
		'OUTCOME',
		'FOR1_HOME',
		'FOR1_AST',
		'FOR1_BLK',
		'FOR1_FG3A',
		'FOR1_FG3M',
		'FOR1_FGA',
		'FOR1_FGM',
		'FOR1_FTA',
		'FOR1_FTM',
		'FOR1_MIN',
		'FOR1_PF',
		'FOR1_PTS',
		'FOR1_REB',
		'FOR1_STL',
		'FOR1_TO',		
		'FOR2_HOME',
		'FOR2_AST',
		'FOR2_BLK',
		'FOR2_FG3A',
		'FOR2_FG3M',
		'FOR2_FGA',
		'FOR2_FGM',
		'FOR2_FTA',
		'FOR2_FTM',
		'FOR2_MIN',
		'FOR2_PF',
		'FOR2_PTS',
		'FOR2_REB',
		'FOR2_STL',
		'FOR2_TO',
		'CENTER_HOME',
		'CENTER_AST',
		'CENTER_BLK',
		'CENTER_FG3A',
		'CENTER_FG3M',
		'CENTER_FGA',
		'CENTER_FGM',
		'CENTER_FTA',
		'CENTER_FTM',
		'CENTER_MIN',
		'CENTER_PF',
		'CENTER_PTS',
		'CENTER_REB',
		'CENTER_STL',
		'CENTER_TO',
		'GUARD1_HOME',
		'GUARD1_AST',
		'GUARD1_BLK',
		'GUARD1_FG3A',
		'GUARD1_FG3M',
		'GUARD1_FGA',
		'GUARD1_FGM',
		'GUARD1_FTA',
		'GUARD1_FTM',
		'GUARD1_MIN',
		'GUARD1_PF',
		'GUARD1_PTS',
		'GUARD1_REB',
		'GUARD1_STL',
		'GUARD1_TO',
		'GUARD2_HOME',
		'GUARD2_AST',
		'GUARD2_BLK',
		'GUARD2_FG3A',
		'GUARD2_FG3M',
		'GUARD2_FGA',
		'GUARD2_FGM',
		'GUARD2_FTA',
		'GUARD2_FTM',
		'GUARD2_MIN',
		'GUARD2_PF',
		'GUARD2_PTS',
		'GUARD2_REB',
		'GUARD2_STL',
		'GUARD2_TO',
		'6MAN_HOME',
		'6MAN_AST',
		'6MAN_BLK',
		'6MAN_FG3A',
		'6MAN_FG3M',
		'6MAN_FGA',
		'6MAN_FGM',
		'6MAN_FTA',
		'6MAN_FTM',
		'6MAN_MIN',
		'6MAN_PF',
		'6MAN_PTS',
		'6MAN_REB',
		'6MAN_STL',
		'6MAN_TO'
	]

	counter = 0
	curr_row = []
	max_mins = (-1, None)
	for i in range(len(datasets)):
		all_data = []
		for j, data in datasets[i].iterrows():
			if np.isnan(data['OUTCOME']):
				counter = 0
				populate_row(max_mins[1], curr_row)
				all_data.append(curr_row)
				continue
			if counter == 0:
				curr_row = []
				max_mins = (-1, None)
				curr_row.append(int(data['OUTCOME']))
			if counter > 4:
				if data['MIN'] > max_mins[0]:
					max_mins = (data['MIN'], data)
			else:
				populate_row(data, curr_row)
				counter += 1

		datasets[i] = pd.DataFrame(all_data, columns=columns)

	datasets[0].to_csv('for_bayesian_files/train.csv', index=False)
	datasets[1].to_csv('for_bayesian_files/test.csv', index=False)
	datasets[2].to_csv('for_bayesian_files/validate.csv', index=False)

def populate_row(data, curr_row):
	curr_row.append(int(data['HOME']))
	curr_row.append(int(data['AST']))
	curr_row.append(int(data['BLK']))
	curr_row.append(int(data['FG3A']))
	curr_row.append(int(data['FG3M']))
	curr_row.append(int(data['FGA']))
	curr_row.append(int(data['FGM']))
	curr_row.append(int(data['FTA']))
	curr_row.append(int(data['FTM']))
	curr_row.append(int(data['MIN']))
	curr_row.append(int(data['PF']))
	curr_row.append(int(data['PTS']))
	curr_row.append(int(data['REB']))
	curr_row.append(int(data['STL']))
	curr_row.append(int(data['TO']))


if __name__ == '__main__':
    main()
