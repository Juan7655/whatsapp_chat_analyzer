import seaborn
import matplotlib.pyplot as plt
import datetime
import date_manager
import pandas

# separation character
start_line = "//-"
initial_day = 13
initial_month = 10
initial_year = 18
# date_config = 0 -> mm/dd/yy
# date_config = 1 -> dd/mm/yy
date_config = 0

# if the lines contains any word on this list, it will be omitted
forbidden_keywords = ["added", "left", "changed", "created", "removed", "Creaste", "Añadiste", "Eliminaste",
					  "cambió el icono", "cambió de", "salió", "Los mensajes en este grupo",
					  "Messages to this group are now secured"]


def run():
	with open("wa_chat.txt") as file:
		file = file.readlines()

	now = datetime.datetime.now()
	data = set_data(file)
	data.pop(0)
	matrix = get_attributes(data)
	date_array = get_date_array(matrix)
	date_dist = date_manager.date_distance(matrix[0][0], matrix[0][1], matrix[0][2],
										   date_manager.date_to_str(now.day, now.month, now.year - 2000))

	# graphs frequency of messages in every day of the week
	weekday_arr = [(i + date_dist - 1) % 7 for i in date_array["date_dist"]]
	date_array.insert(0, "weekday", weekday_arr)
	week_days = [i for i in range(7)]
	week_day_count = [weekday_arr.count(i) for i in range(7)]
	plt.bar(week_days, week_day_count, align='center')
	plt.xlabel("Día de la semana")
	plt.ylabel("Número de mensajes")
	plt.show()

	# graphs frequency of messages on every day
	# seaborn.distplot(date_array["date_dist"], kde=False, bins=date_dist)
	# plt.xlabel("Día")
	# plt.ylabel("Número de mensajes")
	# plt.show()

	# counts messages for every person in the group
	ppl_count, month_count = get_people_count(matrix)
	for i in range(len(ppl_count[0])):
		print(str(ppl_count[0][i]) + ": " + str(ppl_count[1][i]))
	print("---------------------")

	# counts occurrences of the words given in the data matrix
	word_bank = ["canción", "word2", "word3"]
	cnt = 0
	for i in word_bank:
		temp_count = sum(map(lambda line: i in line[5], matrix))
		print(i + " count: " + str(temp_count))
		cnt += temp_count
	print("Total word count: " + str(cnt))

	# graphs message frequency on each month of the year
	plt.bar([i for i in range(1, 13)], month_count, align='center')
	plt.xlabel("Mes")
	plt.ylabel("Número de mensajes")
	plt.show()

	punchcard_matrix(date_array[["weekday", "hour"]])


# detects the start of every message (with the dates logic). Appends all lines into a single place which is
# finally splitted with the start_line character.
def set_data(file):
	day = initial_day
	month = initial_month
	year = initial_year
	mfile = ""

	for line in file:
		for date in date_manager.from_date(day, month, year):
			if date in line:
				line = line.replace(date, start_line + date, 1)
				line = line.replace("1" + start_line + date, start_line + "1" + date, 1)
				day, month, year = date_manager.goto_date(date)
				break
		mfile += line
	return mfile.split(start_line)


# creates the feature matrix, splitting each message line into its components
# structures data into the returned matrix
# includes date(day, month, year), time, sender name and message
def get_attributes(data):
	# determines which lines are not taken into account
	return list(
		map(lambda line: line_split(line),
		    filter(lambda temp_line: not any(
			    map(lambda word: word in temp_line, forbidden_keywords)), data)))


def line_split(line):
	split = line.split(", ", 2)

	date = split[0]
	m_date = [0, 0, 0]
	m_date[1 - date_config] = int(date.split("/")[0])
	date = date.replace(str(m_date[1 - date_config]) + "/", "", 1)
	m_date[date_config] = int(date.split("/")[0])
	date = date.replace(str(m_date[date_config]) + "/", "", 1)
	m_date[2] = int(date)

	line = line.replace(date_manager.date_to_str(m_date[0], m_date[1], m_date[2]) + ", ", "", 1)
	time = line.split(" - ", 2)[0]
	line = line.replace(time + " - ", "", 1)
	split = line.split(": ", 2)
	sender = split[0]
	message = split[1]
	return [m_date[0], m_date[1], m_date[2], time, sender, message]


# transforms each day int a relative number with respect to the initial date.
# includes the hour column for the punchcard graph
def get_date_array(matrix):
	dates = pandas.DataFrame(columns=["date_dist", "hour"])
	current_index = 1
	day = matrix[0][0]
	month = matrix[0][1]
	year = matrix[0][2]

	for i in matrix:
		# calculates relative date distance with respect to the last entered date and sums it to the count
		# saves process by not calculating the distance with respect to the initial date, but with each one's previous
		current_index += date_manager.date_distance(day, month, year, date_manager.date_to_str(i[0], i[1], i[2]))
		df = pandas.DataFrame([[current_index, i[3].split(":")[0]]], columns=["date_dist", "hour"])
		dates = dates.append(df)
		day = i[0]
		month = i[1]
		year = i[2]
	return dates


# counts the number of messages for every person in the chat
def get_people_count(matrix):
	array = [matrix[0][4]]
	month_count = [0 for _ in range(1, 13)]
	count = [0]

	for i in matrix:
		if i[4] in array:
			index = array.index(i[4])
			count[index] += 1
		else:
			array.append(i[4])
			count.append(1)
		month_count[i[1] - 1] += 1
	mt = [array, count]
	return mt, month_count


# takes in the date_array, creates the matrix input for the punchcard graph and exports it to csv file
def punchcard_matrix(matrix):
	punch_matrix = pandas.DataFrame([[0 for _ in range(24)] for _ in range(7)])
	for index, row in matrix.iterrows():
		punch_matrix[int(row["hour"])][int(row["weekday"])] += 1
	weekdays = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
	punch_matrix.insert(0, "weekday", weekdays)
	punch_matrix.set_index("weekday")
	punch_matrix.to_csv("result.csv", index=False)


def load_src(fpath, name="helper"):
	import os, imp
	return imp.load_source(name, os.path.join(os.path.dirname(__file__), fpath))


if __name__ == '__main__':
	run()
