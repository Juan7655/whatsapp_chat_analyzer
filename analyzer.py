import seaborn
import matplotlib.pyplot as plt
import datetime
import date_manager

start_line = "//-"
initial_day = 15
initial_month = 12
initial_year = 15
date_config = 1

forbidden_keywords = ["added", "left", "changed", "created", "removed", "Creaste", "Añadiste", "Eliminaste",
                      "cambió el icono", "cambió de", "salió", "Los mensajes en este grupo"]


def run():
	with open("wa_chat(1).txt") as file:
		file = file.readlines()

	now = datetime.datetime.now()
	data = set_data(file)
	data.pop(0)
	matrix = get_attributes(data)
	date_array = get_date_array(matrix)
	print(date_array)
	date_dist = date_manager.date_distance(matrix[0][0], matrix[0][1], matrix[0][2],
	                                       date_manager.date_to_str(now.day, now.month, now.year - 2000))
	seaborn.distplot(date_array, kde=False, bins=date_dist)

	ppl_count = get_people_count(matrix)
	for i in range(len(ppl_count[0])):
		print(str(ppl_count[0][i]) + ": " + str(ppl_count[1][i]))

	print("---------------------")

	word_bank = ["word1", "word2", "word3"]
	cnt = 0
	for i in word_bank:
		temp_count = get_word_count(matrix, i)
		print(i + " count: " + str(temp_count))
		cnt += temp_count
	print("Total word count: " + str(cnt))
	plt.show()


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
				day, month, year = date_manager.goto_date(day, month, year, date)
				break
		mfile += line
	return mfile.split(start_line)


def get_attributes(data):
	matrix = []
	count = 0

	for line in data:
		accept_line = True
		for word in forbidden_keywords:
			if word in line:
				accept_line = False
				break

		if accept_line:
			split = line.split(", ", 2)

			date = split[0]
			m_date = [0, 0, 0]
			m_date[1 - date_config] = int(date.split("/")[0])
			date = date.replace(str(m_date[0]) + "/", "", 1)
			m_date[date_config] = int(date.split("/")[0])
			date = date.replace(str(m_date[1]) + "/", "", 1)
			m_date[2] = int(date)

			line = line.replace(date_manager.date_to_str(m_date[0], m_date[1], m_date[2]) + ", ", "", 1)
			time = line.split(" - ", 2)[0]
			line = line.replace(time + " - ", "", 1)
			split = line.split(": ", 2)
			sender = split[0]
			try:
				message = split[1]
			except IndexError:
				print("")

			matrix.append([m_date[0], m_date[1], m_date[2], time, sender, message])
			count += 1
	return matrix


def get_date_array(matrix):
	dates = []
	current_index = 1
	day = matrix[0][0]
	month = matrix[0][1]
	year = matrix[0][2]

	for i in matrix:
		current_index += date_manager.date_distance(day, month, year, date_manager.date_to_str(i[0], i[1], i[2]))
		dates.append(current_index)
		day = i[0]
		month = i[1]
		year = i[2]
	return dates


# counts the number of messages for every person in the chat
def get_people_count(matrix):
	array = [matrix[0][4]]
	count = [0]

	for i in matrix:
		if i[4] in array:
			index = array.index(i[4])
			count[index] += 1
		else:
			array.append(i[4])
			count.append(1)
	mt = [array, count]
	return mt


# counts occurrences of the given words in the chat
def get_word_count(matrix, word):
	count = 0

	for i in matrix:
		if word in i[5]:
			count += 1
	return count


if __name__ == '__main__':
	run()
