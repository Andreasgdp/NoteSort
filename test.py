test = [1, 2, 3, 4]

for index, element in enumerate(test):
	if element == 2:
		element = 0

print(test)
# [1, 2, 3, 4]

for index, element in enumerate(test):
	if element == 2:
		test[index] = 0

print(test)
# [1, 0, 3, 4]