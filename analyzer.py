import matplotlib.pyplot as plt
import datetime
import pandas as pd

date_config = '%m/%d/%y'
# separation character
start_line = "//-"
# if the lines contains any word on this list, they will be omitted
forbidden_keywords = ["added", "left", "changed", "created", "removed", "Creaste", "Añadiste", "Eliminaste",
                      "cambió el icono", "cambió de", "salió", "Los mensajes en este grupo",
                      "Messages to this group are now secured"]
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
operations = [lambda x: plot_day_count(x),
              lambda x: plot_week_day_count(x),
              lambda x: get_people_count(x),
              lambda x: get_word_count(x),
              lambda x: plot_mont_acc(x),
              lambda x: export_punchcard_matrix(x)]


def run():
	with open("wa_chat.txt") as file:
		file = file.readlines()
	matrix = lambda f: f(get_attributes(set_data(file)))

	res = list(map(matrix, operations))
	print(res[2])
	print("---------------------")
	print(res[3])
	print("Total word count: " + str(sum(res[3]['count'])))


def plot_week_day_count(matrix):
	data = matrix.groupby(matrix.date_time.dt.weekday)['message'].count()
	plt.bar(weekdays, data, align='center')
	plot_info("Day of week", "Message count")


def plot_day_count(matrix):
	matrix.groupby(matrix.date_time.dt.date)['date_time'].count().plot(rot=25, kind='line')
	plot_info("Day", "Message count")


def plot_mont_acc(matrix):
	# graphs message frequency on each month of the year
	month_count = get_month_count(matrix)
	plt.bar(month_count.index, month_count.values, align='center')
	plot_info("Month", "Message count")


def get_word_count(matrix):
	# counts occurrences of the words given in the data matrix
	word_bank = ["canción", "word2", "word3"]
	word_count = list(map(sum, map(matrix.message.str.contains, word_bank)))
	df = pd.DataFrame([word_bank, word_count]).T
	df.columns = ['word', 'count']
	return df


# detects the start of every message (with the dates logic).
# Appends all lines into a single place which is
# finally split with the start_line character.
def set_data(file):
	date_val = datetime.datetime.strptime(file[0].split(',', 1)[0], date_config)
	mfile = ""

	for line in file:
		for date in from_date(date_val):
			date_str = date.strftime(date_config).replace("/0", "/")
			if date_str[0] == '0':
				date_str = date_str[1:]
			if date_str in line:
				line = start_line + line
				date_val = date
				break
		mfile += line
	return mfile.split(start_line)[1:]


# creates the feature matrix, splitting each message line into its components
# includes datetime, sender name and message
def get_attributes(data):
	dt = pd.DataFrame(
		list(map(line_split,
		         filter(lambda temp_line: not any(
			         map(lambda word: word in temp_line, forbidden_keywords)), data))),
		columns=['date_time', 'sender', 'message'])
	dt.date_time = pd.to_datetime(dt.date_time, format=date_config + ", %I:%M %p")
	return dt


def line_split(line):
	split = line.split(" - ", 1)
	split2 = split[1].split(": ", 1)
	return [split[0], split2[0], split2[1]]


def get_people_count(matrix):
	return matrix.groupby(by='sender')['message'].count()


def get_month_count(matrix):
	return matrix.groupby(matrix.date_time.dt.strftime('%B'))['message'].count()


# takes in the date_array, creates the matrix input for the punchcard graph and exports it to csv file
def export_punchcard_matrix(matrix):
	punch_matrix = pd.DataFrame([[0 for _ in range(24)] for _ in range(7)])
	punch_matrix.index = weekdays

	for wd_num, wd_name in zip(range(7), weekdays):
		for hour in range(24):
			punch_matrix[hour][wd_name] = matrix[(matrix.date_time.dt.hour == hour) &
			                                     (matrix.date_time.dt.weekday == wd_num)].shape[0]
	punch_matrix.to_csv("result.csv", index=True)


def load_src(fpath, name="helper"):
	import os, imp
	return imp.load_source(name, os.path.join(os.path.dirname(__file__), fpath))


def plot_info(x_label, y_label):
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.show()


def from_date(date):
	for _ in range(100):
		yield date
		date = date + datetime.timedelta(1)


if __name__ == '__main__':
	run()
