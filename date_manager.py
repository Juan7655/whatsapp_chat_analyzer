date_config = 1


# creates a list of consequent dates starting from the given input date
def from_date(day, month, year):
	date_list = []

	for _ in range(100):
		date_list.append(date_to_str(day, month, year))
		day, month, year = next_date(day, month, year)

	return date_list


# returns date of the next day of a given input date using calendar logic
def next_date(day, month, year):
	months_30 = [4, 6, 9, 11]

	day += 1

	if day == 32 or \
			(day == 31 and month in months_30) or \
			(day == 29 and month == 2 and year % 4 != 0) or \
			(day == 30 and month == 2 and year % 4 == 0):
		day = 1
		month += 1

	if month == 13:
		month = 1
		year += 1

	return day, month, year


def date_to_str(day, month, year):
	if date_config == 0:
		return str(month) + "/" + str(day) + "/" + str(year)
	else:
		return str(day) + "/" + (str(month) if month > 9 else ("0" + str(month))) + "/" + str(year)


# returns day, month and year of date string
def goto_date(day, month, year, objective):
	while True:
		if date_to_str(day, month, year) == objective:
			return day, month, year
		day, month, year = next_date(day, month, year)


# returns number of days between two dates
def date_distance(day, month, year, objective):
	count = 0
	while True:
		if date_to_str(day, month, year) == objective:
			return count
		count += 1
		day, month, year = next_date(day, month, year)
