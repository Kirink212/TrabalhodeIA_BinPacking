#Algoritmo First Fit: Recebe uma lista de itens em ordem decrescente,
#inserindo o item no primeiro bin que tiver espaço suficiente para guardá-lo
def first_fit_algorithm(bin_capacity, items_list):
	
	#Lista de bins na qual cada bin é representado por uma string de 0's e 1's, em que as posições
	#que possuem valor 1 representam qual item está presente neste bin de acordo com seu índice, referente a lista de itens.
	bins_list = []
	
	bin_index = 0 #Índice do bin
	item_index = 0 #Índice do item

	t0 = time() #Começa a marcar o tempo de execução do algoritmo.
		
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