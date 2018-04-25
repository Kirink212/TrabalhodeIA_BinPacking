from time import time
from random import shuffle
from re import finditer
from operator import itemgetter

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

def item_size(item):
	bin_sum = 0

	for one in finditer('1', item):
		bin_sum += items_list[one.start()]

	return bin_sum

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

	for u_bin in bins_list:
	 	bin_sum = sum(u_bin)
	 	print("Este bin tem ", bin_capacity - bin_sum, " de peso sobrando")

	print("Lista de bins: ", bins_list)
	t1 = time()
	print("-------------------------------")
	print("Total de bins: ", len(bins_list))
	print("Tempo de execução: ", t1-t0)
	print("-------------------------------")
	return bins_list

def first_fit_algorithm_modified(bin_capacity, items_list):
	bins_list = []
	bin_index = 0
	item_index = 0
	string_bin_pattern = "0"*len(items_list)

	t0 = time()

	while item_index < len(items_list): 
		if bins_list == []:
			bins_list.append(string_bin_pattern)

		bin_sum = item_size(bins_list[bin_index])
		# for one in finditer('1', bins_list[bin_index]):
		# 	bin_sum += items_list[one.start()]

		check_sum = items_list[item_index] + bin_sum

		if check_sum > bin_capacity:

			if bin_index == len(bins_list) - 1:
				bins_list.append(string_bin_pattern)
			bin_index = bin_index + 1
		else:
			aux_list = list(bins_list[bin_index])
			aux_list[item_index] = '1'
			bins_list[bin_index] = "".join(aux_list)

			item_index = item_index + 1
			bin_index = 0

	t1 = time()

	# for u_bin in bins_list:
	#  	bin_sum = sum(u_bin)
	#  	print("Este bin tem ", bin_capacity - bin_sum, " de peso sobrando")

	print("-------------------------------")
	for i, u_bin in enumerate(bins_list):
		print("Bin ", i, ": \t", u_bin)
	print(items_list)
	print("Total de bins: ", len(bins_list))
	print("Tempo de execução: ", t1 - t0)
	print("-------------------------------")
	return bins_list

def sort_by_sum(bin_sum):
	pass

def swap_function(item1, item2):
	aux = item1
	item1 = item2
	item2 = aux

	return item1, item2

# def valid_swap(item1, item2):
# 	if 

def hill_climbing_test(bin_capacity, items_list):
	bins_list = first_fit_algorithm_modified(bin_capacity, items_list)
	initial_best = len(bins_list)

	bin_index_1 = 0
	bin_index_2 = 0
	bin_size_list = []

	for i, u_bin in enumerate(bins_list):
		bin_sum = item_size(u_bin)
		bin_size_list.append( (bin_sum, i) )
		# print("Este bin tem ", bin_sum, " de peso")

	list_aux = sorted(bin_size_list, key=itemgetter(0))
	print(list_aux)

	bin_less_weight = list_aux[0][1]
	print(bin_less_weight)
	less_weight = list_aux[0][0]
	print(less_weight)
	bin_index_1 = list_aux[1][1]
	bin_index_2 = list_aux[2][1]
	print(list_aux[1][0])
	print(list_aux[2][0])

	while (bin_index_1 >= 0):
		total_itens_1 = bins_list[bin_index_1].count('1')
		total_itens_2 = bins_list[bin_index_2].count('1')
		# pega o item do bin1
		# pega o item do bin2
		# troca os dois
		# verifica se a troca abriu algum espaço
		# se sim, subtitui e anda
		# se não, anda para o próximo

		item_1 = bins_list[bin_index_1][item_index_1]
		item_2 = bins_list[bin_index_2][item_index_2]

		#item_1, item_2 = swap_function(item_1, item_2)
		if item_index_2 > total_itens_2:
			item_index_2 = 0


		if bin_index_2 < 0:
			item_index_1 = item_index_1 + 1
			bin_index_2 = bin_index_1 + 1



########################################
############ MAIN PROGRAM ##############
########################################

#Instância t60_00
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_t60_00.txt")
first_fit_algorithm_modified(bin_capacity, items_list)
hill_climbing_test(bin_capacity, items_list)
# #Instância t120_01
# bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_t120_01.txt")
# first_fit_algorithm_modified(bin_capacity, items_list)
# #Instância t120_02
# bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u120_02.txt")
# first_fit_algorithm_modified(bin_capacity, items_list)
# #Instância t250_04
# bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u250_04.txt")
# first_fit_algorithm_modified(bin_capacity, items_list)
# #Instância t500_05
# bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u500_05.txt")
# first_fit_algorithm_modified(bin_capacity, items_list)