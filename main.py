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

	# Bin starts empty
	# Bin total weight
	bin_sum = 0 
	#List that stores the Item indexes that are in the bin
	list_indexes = []

	# Finditer returns an object that represents the positions 
	# that are 1 in the box bitmap string
	# For each index returned, we access the item 
	# weight related to that index
	# and sum it with the bin weight. Then we store its index
	# in the bin list of indexes 
	for one in finditer('1', box):
		# one.start() its the item index
		bin_sum += items_list[one.start()]
		list_indexes.append(one.start())

	return bin_sum, list_indexes

# Retuns the item with less weight inside a bin and its index 	
def min_item(box):
	# List of weights inside a bin
	bin_items_weight_list = []
	
	# Finditer returns an object that represents
	# the positions that are 1 in the box bitmap string
	# In this for we create a weight list
	for one in finditer('1', box):
		# Insere na lista de itens da bin os pesos
		bin_items_weight_list.append(items_list[one.start()])

	# Get the item with less weight
	min_item = min(bin_items_weight_list)
	# Get its index
	min_index = items_list.index(min_item)

	return min_item, min_index

	
# First Fit Algorithm: Receives a list of items in descending order,
# inserting the item on the first bin with enough space to store it
def first_fit_algorithm_modified(bin_capacity, items_list, show_log):
	# Bin list where each bin is represented 
	# as a string of 0's and 1's, 
	# where each position that have number 1 
	# represents which item is on the bin 
	bins_list = []
	bin_index = 0
	item_index = 0
	# Creates a string with size equals the number of items 
	# in the problem, filled with zeroes
	string_bin_pattern = "0"*len(items_list)

	# Start counting algorithm runtime
	t0 = time()
	
	# Repeats until items_list is over
	while item_index < len(items_list): 
	
		# If the list is empty, create the first Bin filled with 0's.
		if bins_list == []:
			bins_list.append(string_bin_pattern)

		# Returns two values. The first if the total weight
		# of the bin and the second is ignored.
		bin_sum, aux = item_size(bins_list[bin_index])
		
		# Variable that receives the item weight
		# and sums with the bin weight 
		check_sum = items_list[item_index] + bin_sum
		
		# If the sum of item weight and bin weight
		# surpass the bin capcity, we go to the next bin.
		if check_sum > bin_capacity:

			# If there is no other bins, we create one.
			if bin_index == len(bins_list) - 1:
				bins_list.append(string_bin_pattern)
				
			# Go to the next bin
			bin_index = bin_index + 1
			
		# But if we can put the item inside the bin
		else:
			
			# As strings in python are immutable, 
			# we convert it to a list
			aux_list = list(bins_list[bin_index])
			
			# We change the 0 value to 1, 
			# indicating that the item is in the bin
			aux_list[item_index] = '1'
			
			# Converts the list to a string and replaces 
			# the old string with the new one.
			bins_list[bin_index] = "".join(aux_list)

			# Go to the next item
			item_index = item_index + 1
			
			# Go back to the initial bin
			bin_index = 0

	# Finished to count algorithm runtime
	t1 = time()

	# Show log just if show_log is True
	if show_log:
		print("-------------------------------")
		print("Total de bins: ", len(bins_list))
		# for index, one_bin in enumerate(bins_list):
		# 	print("Bin ", index+1, ":")
		# 	count = 0
		# 	for i, string in enumerate(one_bin):
		# 		if string == '1':
		# 			count = count + 1
		# 			print("\tItem ", count, ":", items_list[i])
		print("Tempo de execução: ", t1 - t0)
		print("-------------------------------")

	return bins_list

# Verifies if the bin is empty or not
def empty_bin(bin, items_list):
	return (bin == "0"*len(items_list))

# Initially uses the first fit method to create an initial state and from it,
# make swaps and reallocates to arrive at better solutions.
# If from the initial state the algorithm can't find a better state, 
# it randomizes the items list and starts again. But only do it a fixed 
# amount of times.
def hill_climbing_test(bin_capacity, items_list, restart_limit, total_iterations, total_no_better):
	# Starts to count the execution time
	t0 = time()

	# Verifies if you did a restart
	restart_algorithm = False
	# Count the number of restarts
	restart_counter = 0
	# List of solutions found
	bins_list_solution = []
	# Auxiliar list of solutions found
	aux_bins_list_solution = []
	# Upper limit of number of bins
	min_num_of_bins_found = 100000
	
	# While that determines the number times the first fit
	# algorithm will be called again (Random Restart Loop)
	while restart_counter < restart_limit:
		# Condition used to shuffle in all iterations,
		# except for the first one
		if restart_algorithm:
			shuffle(items_list)
			restart_algorithm = False

		# Calling first fit algorithm and registering
		# the initial solution in bins_list variable
		bins_list = first_fit_algorithm_modified(bin_capacity, items_list, False)

		# This list stores, for each bin, its total weight,
		# the bin index in bins_list and the list of
		# indexes of each item inside it
		bin_size_list = []

		# For each bin in bins_list, add a tuple inside
		# bins_size_list with the informations told above
		for i, u_bin in enumerate(bins_list):
			bin_sum, index_list = item_size(u_bin)
			bin_size_list.append( (bin_sum, i, index_list) )

		# Sort list by bins total size
		# (bin_sum variable in iteration above)
		list_aux = sorted(bin_size_list, key=itemgetter(0))
		# Auxiliar list receives bins list (first solution)
		aux_bins_list_solution = bins_list
		# Variable that receives the index of the
		# bin with less total weight
		bin_less_weight_index = list_aux[0][1]
		# Variables that receives the index of the
		# item with less total weight and its own weight
		current_less_weight, current_less_weight_index = min_item(bins_list[bin_less_weight_index])

		# Auxiliar variables
		list_aux_index_1 = 1
		list_aux_index_2 = 2
		# Variable to index which two items are been compared
		item_index_1 = 0
		item_index_2 = 0
		# Variable to index which two items are been compared 
		# However, this index is related to items_list
		item_aux_index_1 = list_aux[list_aux_index_1][2][item_index_1]
		item_aux_index_2 = list_aux[list_aux_index_2][2][item_index_2]
		# Variables to index which two bins are been compared
		bin_index_1 = list_aux[list_aux_index_1][1]
		bin_index_2 = list_aux[list_aux_index_2][1]
		list_aux_size = len(list_aux) - 1

		counter = 0
		better_counter = 0
		# While counter doesn't reach the total iterations
		# passed as a parameter, the algorithm will
		# be executed (Hill Climbing Loop)
		while (counter < total_iterations):
			# Set better_solution boolean to false
			better_solution = False

			# Copying bins_list to bins_list_aux
			bins_list_aux = bins_list[::]

			# Get total of items of each bin
			total_items_1 = bins_list[bin_index_1].count('1')
			total_items_2 = bins_list[bin_index_2].count('1')

			# Get both items from bin 1 and bin 2
			# We need to convert from string to list
			# because strings are immutable
			item_1 = list(bins_list_aux[bin_index_1])
			item_2 = list(bins_list_aux[bin_index_2])

			# Swap items inside bin_list_aux
			# We need to change the '0' from bin_1 by
			# the '1' in the same position of the bin_2
			aux = item_1[item_aux_index_1]
			item_1[item_aux_index_1] = item_2[item_aux_index_1]
			item_2[item_aux_index_1] = aux

			aux = item_1[item_aux_index_2]
			item_1[item_aux_index_2] = item_2[item_aux_index_2]
			item_2[item_aux_index_2] = aux

			# Transform back from list to string
			bins_list_aux[bin_index_1] = "".join(item_1)
			bins_list_aux[bin_index_2] = "".join(item_2)

			# Getting the space left after swapping the items
			# between bins
			size_1, aux_off = item_size(bins_list_aux[bin_index_1])
			size_2, aux_off = item_size(bins_list_aux[bin_index_2])
			rest_of_bin_1 = bin_capacity - size_1
			rest_of_bin_2 = bin_capacity - size_2

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
				# If the algorithm is more than "total_no_better"
				# iterations without finding a better solution,
				# the looping is interrupted and the algorithm
				# and the algorithm restarts with other inital
				# solution
				elif better_counter > total_no_better:
					restart_algorithm = True
					break

			better_counter = better_counter + 1

			# If a better solution was achieved
			if better_solution:
				better_counter = 0

				# Remove last bin if it's empty
				if empty_bin(bins_list_aux[bin_less_weight_index], items_list):
					bins_list_aux.pop(bin_less_weight_index)

				# Current bins_list changes
				bins_list = bins_list_aux

				if len(bins_list) < len(aux_bins_list_solution):
					aux_bins_list_solution = bins_list

				# The lines bellow does the same thing
				# that they do in the beginning of the
				# algorithm, 
				bin_size_list = []

				# The lines bellow does the same thing 
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

		if len(aux_bins_list_solution) < min_num_of_bins_found:
			min_num_of_bins_found = len(aux_bins_list_solution)
			bins_list_solution = aux_bins_list_solution

		restart_counter = restart_counter + 1
	t1 = time()

	print("-------------------------------")
	print("Total de bins: ", min_num_of_bins_found)
	# for index, one_bin in enumerate(bins_list_solution):
	# 	print("Bin ", index+1, ":")
	# 	count = 0
	# 	for i, string in enumerate(one_bin):
	# 		if string == '1':
	# 			count = count + 1
	# 			print("\tItem ", count, ":", items_list[i])

	print("Tempo de execução: ", t1 - t0)
	print("-------------------------------")

	return bins_list_solution

# Function to generate output archive
# Receives last bins' list found as solution
# and the path to the file in which the results
# will be written
def outputFile(bins_list_solution, filePath):
	# Open file in write mode
	file = open(filePath, "w")

	# Get the number of bins
	num_bins = str(len(bins_list_solution))

	# Write the number of bins in file
	file.write(num_bins + "\n")

	# For each bin in bins_list, write each item size
	# in the same file line
	for index, one_bin in enumerate(bins_list_solution):
		aux = ""
		for i, string in enumerate(one_bin):
			# Just concatenate when there's one in string
			if string == '1':
				# Find the items size in items_list, depending on i (index)
				aux += str(items_list[i]) + " "
		# Write the items sizes in file
		file.write(aux + "\n")

	# Close file
	file.close()

########################################
############ MAIN PROGRAM ##############
########################################


#########################################################################
# Execution order for each instance:									#
#	1 - Read instance file;												#
#	2 - Call first fit algorithm;										#
#	3 - Write result in output file (just First Fit results folder);	#
#	4 - Call hill climbing algorithm;									#
#	5 - Write result in output file (just Hill Climbing results folder).#
#########################################################################

#Instância t60_00
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_t60_00.txt")
bins_list = first_fit_algorithm_modified(bin_capacity, items_list, True)
outputFile(bins_list, "Instances-SubSet-Falkenauer-FirstFit-Solution/Falkenauer_t60_00.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 10, 100, 20)
outputFile(bins_list, "Instances-SubSet-Falkenauer-HillClimbing-Solution/Falkenauer_t60_00.txt")

#Instância t120_01
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_t120_01.txt")
bins_list = first_fit_algorithm_modified(bin_capacity, items_list, True)
outputFile(bins_list, "Instances-SubSet-Falkenauer-FirstFit-Solution/Falkenauer_t120_01.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 10, 100, 20)
outputFile(bins_list, "Instances-SubSet-Falkenauer-HillClimbing-Solution/Falkenauer_t120_01.txt")

#Instância t120_02
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u120_02.txt")
bins_list = first_fit_algorithm_modified(bin_capacity, items_list, True)
outputFile(bins_list, "Instances-SubSet-Falkenauer-FirstFit-Solution/Falkenauer_u120_02.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 30, 100, 20)
outputFile(bins_list, "Instances-SubSet-Falkenauer-HillClimbing-Solution/Falkenauer_u120_02.txt")

#Instância t250_04
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u250_04.txt")
bins_list = first_fit_algorithm_modified(bin_capacity, items_list, True)
outputFile(bins_list, "Instances-SubSet-Falkenauer-FirstFit-Solution/Falkenauer_u250_04.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 10, 100, 20)
outputFile(bins_list, "Instances-SubSet-Falkenauer-HillClimbing-Solution/Falkenauer_u250_04.txt")

#Instância t500_05
bin_capacity, items_list = readInstanceArchive("Instances-SubSet-Falkenauer 2/Falkenauer_u500_05.txt")
bins_list = first_fit_algorithm_modified(bin_capacity, items_list, True)
outputFile(bins_list, "Instances-SubSet-Falkenauer-FirstFit-Solution/Falkenauer_u500_05.txt")
bins_list = hill_climbing_test(bin_capacity, items_list, 1, 100, 20)
outputFile(bins_list, "Instances-SubSet-Falkenauer-HillClimbing-Solution/Falkenauer_u500_05.txt")
