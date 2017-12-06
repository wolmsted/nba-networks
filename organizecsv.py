import pandas as pd
import json


def main():
	selected_columns = [
		'OUTCOME',
		'NAME',
		'TEAM_CITY',
		'HOME',
		'DATE',
		'AST',
		'BLK',
		'DREB',
		'FG3A',
		'FG3M',
		'FG3_PCT',
		'FGA',
		'FGM',
		'FG_PCT',
		'FTA',
		'FTM',
		'FT_PCT',
		'MIN',
		'OREB',
		'PF',
		'PTS',
		'REB',
		'START_POSITION',
		'STL',
		'TO'
	]

	train = read_file(selected_columns, 'rotowire/train.json')
	train.to_csv('csv_files/train.csv', columns=selected_columns, index=False)

	test = read_file(selected_columns, 'rotowire/test.json')
	test.to_csv('csv_files/test.csv', columns=selected_columns, index=False)

	validate = read_file(selected_columns, 'rotowire/valid.json')
	validate.to_csv('csv_files/validate.csv', columns=selected_columns, index=False)


def read_file(selected_columns, filename):
	data = []
	seen = set()
	with open(filename, 'r') as f:
		file = json.load(f)
		for row in file:
			winner = ''
			if row['home_line']['TEAM-PTS'] > row['vis_line']['TEAM-PTS']:
				winner = 1
			else:
				winner = 0
			box_score = row['box_score']
			date = row['day']
			check_dup = (row['home_line']['TEAM-CITY'], row['vis_line']['TEAM-CITY'], date)
			if check_dup in seen:
				continue
			else:
				seen.add(check_dup)

			for i in range(26):
				str_i = str(i)
				if str_i not in box_score['TEAM_CITY']:
					break
				new_row = []
				new_row.append(str(winner))
				new_row.append(box_score['PLAYER_NAME'][str_i])
				new_row.append(box_score['TEAM_CITY'][str_i])
				home = '1' if row['home_line']['TEAM-CITY'] == box_score['TEAM_CITY'][str_i] else '0'
				new_row.append(home)
				new_row.append(date)
				new_row.append(box_score['AST'][str_i])
				new_row.append(box_score['BLK'][str_i])
				new_row.append(box_score['DREB'][str_i])
				new_row.append(box_score['FG3A'][str_i])
				new_row.append(box_score['FG3M'][str_i])
				new_row.append(box_score['FG3_PCT'][str_i])
				new_row.append(box_score['FGA'][str_i])
				new_row.append(box_score['FGM'][str_i])
				new_row.append(box_score['FG_PCT'][str_i])
				new_row.append(box_score['FTA'][str_i])
				new_row.append(box_score['FTM'][str_i])
				new_row.append(box_score['FT_PCT'][str_i])
				new_row.append(box_score['MIN'][str_i])
				new_row.append(box_score['OREB'][str_i])
				new_row.append(box_score['PF'][str_i])
				new_row.append(box_score['PTS'][str_i])
				new_row.append(box_score['REB'][str_i])
				new_row.append(box_score['START_POSITION'][str_i])
				new_row.append(box_score['STL'][str_i])
				new_row.append(box_score['TO'][str_i])
				data.append(new_row)
			# empty line for new box score
			data.append([None] * 25)

	return pd.DataFrame(data, columns=selected_columns)


if __name__ == '__main__':
    main()
