import datetime
date_config = 0


# creates a list of consequent dates starting from the given input date
def from_date(day, month, year):
	for _ in range(100):
		yield date_to_str(day, month, year)
		day, month, year = next_date(day, month, year)


# returns date of the next day of a given input date using calendar logic
def next_date(day, month, year):
	final_date = datetime.date(year, month, day) + datetime.timedelta(1)
	return final_date.day, final_date.month, final_date.year


def date_to_str(day, month, year):
	date = [str(day), str(month), str(year)]
	return "/".join([date[1-date_config], date[date_config], date[2]])


# returns day, month and year of date string
def goto_date(objective):
	split = list(map(lambda it: int(it), objective.split("/")))
	return split[1 - date_config], split[date_config], split[2]


# returns number of days between two dates
def date_distance(day, month, year, objective):
	d1 = datetime.date(year, month, day)
	split = goto_date(objective)
	d2 = datetime.date(year=split[0], month=split[1], day=split[2])
	return (d2 - d1).days