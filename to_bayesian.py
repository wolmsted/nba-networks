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
		'HOME_FOR1_HOME',
		'HOME_FOR1_AST',
		'HOME_FOR1_BLK',
		'HOME_FOR1_FG3A',
		'HOME_FOR1_FG3M',
		'HOME_FOR1_FGA',
		'HOME_FOR1_FGM',
		'HOME_FOR1_FTA',
		'HOME_FOR1_FTM',
		'HOME_FOR1_MIN',
		'HOME_FOR1_PF',
		'HOME_FOR1_PTS',
		'HOME_FOR1_REB',
		'HOME_FOR1_STL',
		'HOME_FOR1_TO',		
		'HOME_FOR2_HOME',
		'HOME_FOR2_AST',
		'HOME_FOR2_BLK',
		'HOME_FOR2_FG3A',
		'HOME_FOR2_FG3M',
		'HOME_FOR2_FGA',
		'HOME_FOR2_FGM',
		'HOME_FOR2_FTA',
		'HOME_FOR2_FTM',
		'HOME_FOR2_MIN',
		'HOME_FOR2_PF',
		'HOME_FOR2_PTS',
		'HOME_FOR2_REB',
		'HOME_FOR2_STL',
		'HOME_FOR2_TO',
		'HOME_CENTER_HOME',
		'HOME_CENTER_AST',
		'HOME_CENTER_BLK',
		'HOME_CENTER_FG3A',
		'HOME_CENTER_FG3M',
		'HOME_CENTER_FGA',
		'HOME_CENTER_FGM',
		'HOME_CENTER_FTA',
		'HOME_CENTER_FTM',
		'HOME_CENTER_MIN',
		'HOME_CENTER_PF',
		'HOME_CENTER_PTS',
		'HOME_CENTER_REB',
		'HOME_CENTER_STL',
		'HOME_CENTER_TO',
		'HOME_GUARD1_HOME',
		'HOME_GUARD1_AST',
		'HOME_GUARD1_BLK',
		'HOME_GUARD1_FG3A',
		'HOME_GUARD1_FG3M',
		'HOME_GUARD1_FGA',
		'HOME_GUARD1_FGM',
		'HOME_GUARD1_FTA',
		'HOME_GUARD1_FTM',
		'HOME_GUARD1_MIN',
		'HOME_GUARD1_PF',
		'HOME_GUARD1_PTS',
		'HOME_GUARD1_REB',
		'HOME_GUARD1_STL',
		'HOME_GUARD1_TO',
		'HOME_GUARD2_HOME',
		'HOME_GUARD2_AST',
		'HOME_GUARD2_BLK',
		'HOME_GUARD2_FG3A',
		'HOME_GUARD2_FG3M',
		'HOME_GUARD2_FGA',
		'HOME_GUARD2_FGM',
		'HOME_GUARD2_FTA',
		'HOME_GUARD2_FTM',
		'HOME_GUARD2_MIN',
		'HOME_GUARD2_PF',
		'HOME_GUARD2_PTS',
		'HOME_GUARD2_REB',
		'HOME_GUARD2_STL',
		'HOME_GUARD2_TO',
		'HOME_6MAN_HOME',
		'HOME_6MAN_AST',
		'HOME_6MAN_BLK',
		'HOME_6MAN_FG3A',
		'HOME_6MAN_FG3M',
		'HOME_6MAN_FGA',
		'HOME_6MAN_FGM',
		'HOME_6MAN_FTA',
		'HOME_6MAN_FTM',
		'HOME_6MAN_MIN',
		'HOME_6MAN_PF',
		'HOME_6MAN_PTS',
		'HOME_6MAN_REB',
		'HOME_6MAN_STL',
		'HOME_6MAN_TO',
		'AWAY_FOR1_HOME',
		'AWAY_FOR1_AST',
		'AWAY_FOR1_BLK',
		'AWAY_FOR1_FG3A',
		'AWAY_FOR1_FG3M',
		'AWAY_FOR1_FGA',
		'AWAY_FOR1_FGM',
		'AWAY_FOR1_FTA',
		'AWAY_FOR1_FTM',
		'AWAY_FOR1_MIN',
		'AWAY_FOR1_PF',
		'AWAY_FOR1_PTS',
		'AWAY_FOR1_REB',
		'AWAY_FOR1_STL',
		'AWAY_FOR1_TO',		
		'AWAY_FOR2_HOME',
		'AWAY_FOR2_AST',
		'AWAY_FOR2_BLK',
		'AWAY_FOR2_FG3A',
		'AWAY_FOR2_FG3M',
		'AWAY_FOR2_FGA',
		'AWAY_FOR2_FGM',
		'AWAY_FOR2_FTA',
		'AWAY_FOR2_FTM',
		'AWAY_FOR2_MIN',
		'AWAY_FOR2_PF',
		'AWAY_FOR2_PTS',
		'AWAY_FOR2_REB',
		'AWAY_FOR2_STL',
		'AWAY_FOR2_TO',
		'AWAY_CENTER_HOME',
		'AWAY_CENTER_AST',
		'AWAY_CENTER_BLK',
		'AWAY_CENTER_FG3A',
		'AWAY_CENTER_FG3M',
		'AWAY_CENTER_FGA',
		'AWAY_CENTER_FGM',
		'AWAY_CENTER_FTA',
		'AWAY_CENTER_FTM',
		'AWAY_CENTER_MIN',
		'AWAY_CENTER_PF',
		'AWAY_CENTER_PTS',
		'AWAY_CENTER_REB',
		'AWAY_CENTER_STL',
		'AWAY_CENTER_TO',
		'AWAY_GUARD1_HOME',
		'AWAY_GUARD1_AST',
		'AWAY_GUARD1_BLK',
		'AWAY_GUARD1_FG3A',
		'AWAY_GUARD1_FG3M',
		'AWAY_GUARD1_FGA',
		'AWAY_GUARD1_FGM',
		'AWAY_GUARD1_FTA',
		'AWAY_GUARD1_FTM',
		'AWAY_GUARD1_MIN',
		'AWAY_GUARD1_PF',
		'AWAY_GUARD1_PTS',
		'AWAY_GUARD1_REB',
		'AWAY_GUARD1_STL',
		'AWAY_GUARD1_TO',
		'AWAY_GUARD2_HOME',
		'AWAY_GUARD2_AST',
		'AWAY_GUARD2_BLK',
		'AWAY_GUARD2_FG3A',
		'AWAY_GUARD2_FG3M',
		'AWAY_GUARD2_FGA',
		'AWAY_GUARD2_FGM',
		'AWAY_GUARD2_FTA',
		'AWAY_GUARD2_FTM',
		'AWAY_GUARD2_MIN',
		'AWAY_GUARD2_PF',
		'AWAY_GUARD2_PTS',
		'AWAY_GUARD2_REB',
		'AWAY_GUARD2_STL',
		'AWAY_GUARD2_TO',
		'AWAY_6MAN_HOME',
		'AWAY_6MAN_AST',
		'AWAY_6MAN_BLK',
		'AWAY_6MAN_FG3A',
		'AWAY_6MAN_FG3M',
		'AWAY_6MAN_FGA',
		'AWAY_6MAN_FGM',
		'AWAY_6MAN_FTA',
		'AWAY_6MAN_FTM',
		'AWAY_6MAN_MIN',
		'AWAY_6MAN_PF',
		'AWAY_6MAN_PTS',
		'AWAY_6MAN_REB',
		'AWAY_6MAN_STL',
		'AWAY_6MAN_TO'
	]

	counter = 0
	curr_row = []
	home_and_away = []
	max_mins = (-1, None)
	for i in range(len(datasets)):
		all_data = []
		first = True
		home = datasets[i]['HOME'][0]
		reverse = not bool(home)
		outcome = datasets[i]['OUTCOME'][0]
		for j, data in datasets[i].iterrows():
			if np.isnan(data['OUTCOME']):
				counter = 0
				populate_row(max_mins[1], curr_row)
				if reverse == True:
					all_data.append([int(outcome)] + curr_row + home_and_away[0])
				else:
					all_data.append([int(outcome)] + home_and_away[0] + curr_row)
				first = True
				continue
			if data['HOME'] != home:
				counter = 0
				first = False
				home = data['HOME']
				populate_row(max_mins[1], curr_row)
				home_and_away.append(curr_row)
			if counter == 0:
				curr_row = []
				max_mins = (-1, None)
				if first == True:
					home = data['HOME']
					reverse = not bool(home)
					outcome = data['OUTCOME']
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
