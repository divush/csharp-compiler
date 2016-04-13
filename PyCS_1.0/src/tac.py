def print_tac(pclass):
	print("1, call, Main")
	print("2, exit")
	c = 3
	for member in pclass:
		for line in member['code']:
			if line != "":
				print(str(c) + ", " + line)
				c = c + 1