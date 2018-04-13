from time import time
from random import shuffle

########################################
######### FUNCTION DECLARATION #########
########################################

def readInstanceArchive(filePath):
	file = open(filePath, "r")
	items_list = []

	number_of_items = int(file.readline())
	bin_capacity = int(file.readline())

	#print("Número de itens:", number_of_items)
	#print("Capacidade do Bin:", bin_capacity)

	for line in file:
		line = line.strip()
		items_list.append(int(line))

	#print("Lista de itens: ", items_list)

	file.close()

	return bin_capacity, items_list

def first_fit_algorithm(bin_capacity, items_list):
	bins_list = []
	bin_index = 0
	item_index = 0

	t0 = time()
	while item_index < len(items_list): 
		if bins_list == []:
			bins_list.append([])

		#print(bins_list[bin_index])
		bin_sum = sum(bins_list[bin_index])
		check_sum = items_list[item_index] + bin_sum

		if check_sum > bin_capacity:

			if bin_index == len(bins_list) - 1:
				#print("Criei um novo bin")
				bins_list.append([])
			bin_index = bin_index + 1
		else:
			bins_list[bin_index].append(items_list[item_index])
			item_index = item_index + 1
			bin_index = 0

	# for u_bin in bins_list:
	# 	bin_sum = sum(u_bin)
	# 	print("Este bin tem ", bin_sum, " de peso")

	print("Lista de bins: ", bins_list)
	# t1 = time()
	# print("-------------------------------")
	print("Total de bins: ", len(bins_list))
	# print("Tempo de execução: ", t1-t0)
	# print("-------------------------------")
	return bins_list

def hill_climbing_test(bin_capacity, items_list):
	bins_list = first_fit_algorithm(bin_capacity, items_list)
	initial_best = len(bins_list)

	index_bin_1 = 0
	index_bin_2 = 0
	index_item_1 = 0
	index_item_2 = 0

	while(index_bin_1 < len(bins_list)):

		bin_1 = len(bins_list[index_bin_1])
		bin_2 = len(bins_list[index_bin_2])

		curr_bin = bins_list[index_bin_1]
		other_bin = bins_list[index_bin_2]

		value_1 = curr_bin[index_item_1]
		value_2 = curr_bin[index_item_2]

		check_sum_1 = value_2 + sum(curr_bin) - value1
		check_sum_2 = value_1 + sum(curr_bin) - value2

		if check_sum_1 <= bin_capacity and check_sum_2 <= bin_capacity:
			aux = curr_bin[index_item_1]
			curr_bin[index_item_1] = other_bin[index_item_2]
			other_bin[index_item_2] = aux
			index_item_1 = index_item_1 + 1
		else:
			index_item_2 = index_item_2 + 1

		if(index_item_1 == bin_1 - 1):
			index_bin_1 = index_bin_1 + 1
			index_item_1 = 0

		if(index_item_2 == bin_2 - 1):
			index_bin_2 = index_bin_2 + 1
			index_item_2 = 0

		if(index_bin_2 == len(bins_list) - 1):
			index_bin_1 = index_bin_1 + 1
			index_item_1 = 0
			index_bin_2 = 0
			index_item_2 = 0

########################################
############ MAIN PROGRAM ##############
########################################


bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_t60_00.txt")
first_fit_algorithm(bin_capacity, items_list)

# bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_t120_01.txt")
# first_fit_algorithm(bin_capacity, items_list)
# bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u120_02.txt")
# first_fit_algorithm(bin_capacity, items_list)
# bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u250_04.txt")
# first_fit_algorithm(bin_capacity, items_list)
# bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u500_05.txt")
# first_fit_algorithm(bin_capacity, items_list)