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