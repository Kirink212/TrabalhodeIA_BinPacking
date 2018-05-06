########################################
############# LIBRARIES ################
########################################

from time import time #Library to calculate algorithm running time
from random import shuffle, randint
from re import finditer
from operator import itemgetter

########################################
######### FUNCTION DECLARATION #########
########################################


#Reading the InstanceArchive.txt

def readInstanceArchive(filePath):
	file = open(filePath, "r")
	items_list = [] #Instance Items List

	#Setting the parameters
	number_of_items = int(file.readline()) #Total number of items in the instance
	bin_capacity = int(file.readline()) #The bin weight limit

	#print("Número de itens:", number_of_items)
	#print("Capacidade do Bin:", bin_capacity)

	#Iterating each file line
	for line in file:
		#Removing special characters from line if any
		line = line.strip()
		
		#Inserting item in items_list
		items_list.append(int(line))

	#print("Lista de itens: ", items_list)

	file.close()

	return bin_capacity, items_list
#Returns bin total weight
#Returns a list that stores the items indexes that are in a bin
def item_size(box):

	#Bin starts empty
	bin_sum = 0 #Bin total weight
	list_indexes = [] #List that stores the Item indexes that are in the bin


	#Finditer retorna um objeto que representa as posições que possuem 1 na string bitmap box
	#Para cada índice retornado por finditer, acessamos o peso do item relacionado ao índice,
	# somamos ele com o que já tem no bin e então guardamos seu índice na lista de índices que estão na bin.
	for one in finditer('1', box):
		bin_sum += items_list[one.start()] #one.start() é o índice do item
		list_indexes.append(one.start())

	return bin_sum, list_indexes

	
#Retorna o item de menor peso dentro de um bin e seu valor em peso
def min_item(box):
	bin_items_weight_list = [] #Lista dos pesos dos itens dentro do bin

	#Finditer retorna um objeto que representa as posições que possuem 1 na string bitmap box
	#Neste for fazemos uma lista de pesos
	for one in finditer('1', box):
		bin_items_weight_list.append(items_list[one.start()]) #Insere na lista de itens da bin os pesos

	min_item = min(bin_items_weight_list) #Pega o item de menor peso
	min_index = items_list.index(min_item) #Pega o índice deste

	return min_item, min_index

def first_fit_algorithm(bin_capacity, items_list):
	
	#Lista de bins na qual cada bin é representado por uma string de 0's e 1's, em que as posições
	#que possuem valor 1 representam qual item está presente neste bin de acordo com seu índice, referente a lista de itens.
	bins_list = []
	
	bin_index = 0 #Índice do bin
	item_index = 0 #Índice do item

	t0 = time() #Começa a marcar o tempo de execução do algoritmo.
		
	#Repetição até o final da items_list
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

#Algoritmo First Fit: Recebe uma lista de itens em ordem decrescente,
#inserindo o item no primeiro bin que tiver espaço suficiente para guardá-lo
def first_fit_algorithm_modified(bin_capacity, items_list):

	#Lista de bins na qual cada bin é representado por uma string de 0's e 1's, em que as posições
	#que possuem valor 1 representam qual item está presente neste bin de acordo com seu índice, referente a lista de itens.
	bins_list = []
	bin_index = 0 #Índice do bin
	item_index = 0 #Índice do item
	string_bin_pattern = "0"*len(items_list) #Cria uma string de zeros de tamanho igual ao número de itens do problema.

	# t0 = time()

	#Repetição até o final da items_list
	while item_index < len(items_list): 
	
		#If the list is empty, create the first Bin filled with 0's.
		if bins_list == []:
			bins_list.append(string_bin_pattern)

		#Retorna dois valores. O primeiro é o peso total do bin e o segundo é ignorado.
		bin_sum, aux = item_size(bins_list[bin_index])
		
		#Variable that receives the item weight and sums with the bin weight 
		check_sum = items_list[item_index] + bin_sum
		
		#If the sum of item weight and bin weight surpass the bin capcity, we go to the next bin.
		if check_sum > bin_capacity:

			#If there is no other bins, we create one.
			if bin_index == len(bins_list) - 1:
				bins_list.append(string_bin_pattern)
				
			#Go to the next bin
			bin_index = bin_index + 1
			
		#But if we can put the item inside the bin
		else:
			
			#Como strings em python são imutáveis, convertemos a mesma para um lista
			aux_list = list(bins_list[bin_index])
			
			#Trocamos o valor 0 por 1, para indicar que o peso está no bin
			aux_list[item_index] = '1'
			
			#Converte a lista para uma string e substitui a antiga string do Bin pela nova
			bins_list[bin_index] = "".join(aux_list)

			#Andamos para o próximo item
			item_index = item_index + 1
			
			#Voltamos para o bin inicial
			bin_index = 0

	# t1 = time()

	# for u_bin in bins_list:
	#  	bin_sum = sum(u_bin)
	#  	print("Este bin tem ", bin_capacity - bin_sum, " de peso sobrando")

	# print("-------------------------------")
	# for i, u_bin in enumerate(bins_list):
	# 	print("Bin ", i, ": \t", u_bin)
	# print(items_list)
	# print("Total de bins: ", len(bins_list))
	# print("Tempo de execução: ", t1 - t0)
	# print("-------------------------------")
	return bins_list

#Verifies if the bin is empty or not
def empty_bin(bin, items_list):
	return (bin == "0"*len(items_list))


def hill_climbing_test(bin_capacity, items_list, restart_limit, total_iterations, total_no_better):
	t0 = time()
	restart_algorithm = False
	restart_counter = 0
	bins_list_solution = []
	min_num_of_bins_found = 100000
	
	while restart_counter < restart_limit:
		if restart_algorithm:
			shuffle(items_list)
			restart_algorithm = False

		bins_list = first_fit_algorithm_modified(bin_capacity, items_list)
		initial_best = len(bins_list)

		bin_index_1 = 0
		bin_index_2 = 0
		bin_size_list = []

		for i, u_bin in enumerate(bins_list):
			bin_sum, index_list = item_size(u_bin)
			bin_size_list.append( (bin_sum, i, index_list) )

		list_aux = sorted(bin_size_list, key=itemgetter(0))
		bins_list_solution = bins_list
		bin_less_weight_index = list_aux[0][1]
		current_less_weight, current_less_weight_index = min_item(bins_list[bin_less_weight_index])
		list_aux_index_1 = 1
		list_aux_index_2 = 2
		item_index_1 = 0
		item_index_2 = 0
		item_aux_index_1 = list_aux[list_aux_index_1][2][item_index_1]
		item_aux_index_2 = list_aux[list_aux_index_2][2][item_index_2]
		bin_index_1 = list_aux[list_aux_index_1][1]
		bin_index_2 = list_aux[list_aux_index_2][1]
		list_aux_size = len(list_aux) - 1

		counter = 0
		better_counter = 0
		while (counter < total_iterations):
			better_solution = False

			# Copying bins_list
			bins_list_aux = bins_list[::]

			# Get total of items
			total_items_1 = bins_list[bin_index_1].count('1')
			total_items_2 = bins_list[bin_index_2].count('1')

			# Get both items from bin 1 and bin 2
			item_1 = list(bins_list_aux[bin_index_1])
			item_2 = list(bins_list_aux[bin_index_2])

			# Swap items inside bin_list_aux
			aux = item_1[item_aux_index_1]
			item_1[item_aux_index_1] = item_2[item_aux_index_1]
			item_2[item_aux_index_1] = aux

			aux = item_1[item_aux_index_2]
			item_1[item_aux_index_2] = item_2[item_aux_index_2]
			item_2[item_aux_index_2] = aux

			bins_list_aux[bin_index_1] = "".join(item_1)
			bins_list_aux[bin_index_2] = "".join(item_2)

			# Getting the space left by changing the items
			size_1, aux_off = item_size(bins_list_aux[bin_index_1])
			size_2, aux_off = item_size(bins_list_aux[bin_index_2])
			rest_of_bin_1 = bin_capacity - size_1
			rest_of_bin_2 = bin_capacity - size_2

			# print("Bin 1:", bin_index_1)
			# print("Bin 2:", bin_index_2)
			# print("Item 1:", item_index_1)
			# print("Item 2:", item_index_2)

			# Verify if the change surpasses the capacity of one of the bins
			if rest_of_bin_1 > 0 and rest_of_bin_2 > 0:

				# If there is space left on one of the bins
				there_is_space_left1 = (current_less_weight <= rest_of_bin_1)
				there_is_space_left2 = (current_less_weight <= rest_of_bin_2)

				# See if this change creates a better solution
				if there_is_space_left1:
					# change the item with less weight
					# from its original bin to bin_1
					aux_list = list(bins_list_aux[bin_index_1])
					aux_list[current_less_weight_index] = '1'
					bins_list_aux[bin_index_1] = "".join(aux_list)

					aux_list = list(bins_list_aux[bin_less_weight_index])
					aux_list[current_less_weight_index] = '0'
					bins_list_aux[bin_less_weight_index] = "".join(aux_list)

					better_solution = True
				elif there_is_space_left2:
					# change the item with less weight
					# from its original bin to bin_2
					aux_list = list(bins_list_aux[bin_index_2])
					aux_list[current_less_weight_index] = '1'
					bins_list_aux[bin_index_2] = "".join(aux_list)

					aux_list = list(bins_list_aux[bin_less_weight_index])
					aux_list[current_less_weight_index] = '0'
					bins_list_aux[bin_less_weight_index] = "".join(aux_list)

					better_solution = True
				elif better_counter > total_no_better:
					restart_algorithm = True
					break

					# better_solution = True
					
					# aux_less_weight, aux_less_weight_index = min_item(bins_list_aux[bin_index_1])
					# rand_num = randint(1, 3)
					# if rand_num == 1:
					# 	# Remove item from bin 1
					# 	item_1 = list(bins_list_aux[bin_index_1])
					# 	item_1[aux_less_weight_index] = "0"
					# 	bins_list_aux[bin_index_1] = "".join(item_1)

					# 	# Create new bin to isert removed item
					# 	bins_list_aux.append("0"*len(items_list))
					# 	item = list(bins_list_aux[len(bins_list_aux) - 1])
					# 	item[aux_less_weight_index] = "1"
					# 	bins_list_aux[len(bins_list_aux) - 1] = "".join(item)
					# 	print("Dentro daqui: ", len(bins_list_aux))

					# 	# Get item with less weight from current bin
					# 	aux_less_weight, aux_less_weight_index = min_item(bins_list_aux[bin_index_2])

					# 	# Remove item from bin 2
					# 	item_2 = list(bins_list_aux[bin_index_2])
					# 	item_2[aux_less_weight_index] = "0"
					# 	bins_list_aux[bin_index_2] = "".join(item_2)

					# 	# Create new bin to isert removed item
					# 	item = list(bins_list_aux[len(bins_list_aux) - 1])
					# 	item[aux_less_weight_index] = "1"
					# 	bins_list_aux[len(bins_list_aux) - 1] = "".join(item)
					# 	print("Dentro daqui: ", len(bins_list_aux))

			better_counter = better_counter + 1

			# If a better solution was achieved
			if better_solution:
				better_counter = 0

				# Remove last bin if it's empty
				if empty_bin(bins_list_aux[bin_less_weight_index], items_list):
					bins_list_aux.pop(bin_less_weight_index)

				# Current bins_list changes
				bins_list = bins_list_aux

				# print(len(bins_list))

				if len(bins_list) < len(bins_list_solution):
					bins_list_solution = bins_list

				bin_size_list = []

				for i, u_bin in enumerate(bins_list):
					bin_sum, index_list = item_size(u_bin)
					bin_size_list.append( (bin_sum, i, index_list) )

				list_aux = sorted(bin_size_list, key=itemgetter(0))
				list_aux_size = len(list_aux) - 1
				bin_less_weight_index = list_aux[0][1]
				current_less_weight, current_less_weight_index = min_item(bins_list[bin_less_weight_index])
				list_aux_index_1 = 1
				list_aux_index_2 = 2
				item_index_1 = 0
				item_index_2 = 0
				item_aux_index_1 = list_aux[list_aux_index_1][2][item_index_1]
				item_aux_index_2 = list_aux[list_aux_index_2][2][item_index_2]
				bin_index_1 = list_aux[list_aux_index_1][1]
				bin_index_2 = list_aux[list_aux_index_2][1]
			else:

				item_index_2 = item_index_2 + 1

				if item_index_2 > (total_items_2 - 1):
					item_index_2 = 0
					list_aux_index_2 = list_aux_index_2 + 1

				if list_aux_index_2 > list_aux_size:
					item_index_1 = item_index_1 + 1
					item_index_2 = 0
					list_aux_index_2 = list_aux_index_1 + 1

				if item_index_1 > (total_items_1 - 1):
					item_index_1 = 0
					item_index_2 = 0
					list_aux_index_1 = list_aux_index_1 + 1
					list_aux_index_2 = list_aux_index_1 + 1

				if list_aux_index_1 >= list_aux_size:
					item_index_1 = 0
					item_index_2 = 0
					list_aux_index_2 = 0
					break

				bin_index_1 = list_aux[list_aux_index_1][1]
				bin_index_2 = list_aux[list_aux_index_2][1]
				item_aux_index_1 = list_aux[list_aux_index_1][2][item_index_1]
				item_aux_index_2 = list_aux[list_aux_index_2][2][item_index_2]
			counter = counter + 1

		if len(bins_list_solution) < min_num_of_bins_found:
			min_num_of_bins_found = len(bins_list_solution)

		restart_counter = restart_counter + 1
	t1 = time()

	print("-------------------------------")
	print("Total de bins: ", min_num_of_bins_found)
	print("Tempo de execução: ", t1 - t0)
	print("-------------------------------")

	return bins_list_solution

########################################
############ MAIN PROGRAM ##############
########################################

#Instância t60_00
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_t60_00.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 30, 100, 20)
#Instância t120_01
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_t120_01.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 30, 100, 20)
#Instância t120_02
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u120_02.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 30, 100, 20)
#Instância t250_04
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u250_04.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 30, 100, 20)
#Instância t500_05
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u500_05.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 30, 100, 20)
