# Copyright @ Renata Wong 2021

# Python version: 6.5. Operationg system: Windows 10.

# Instructions for executing this code: 
# Place the file in a folder. 
# Open the command prompt and switch to the folder containing this file. 
# Type in the command prompt: Python subprocess-doodle.py

import subprocess
import numpy as np
import textwrap

# Task: parallelize matrix multiplication

# How it is done in steps: 
# Step 1: Declare two matrices to be multiplied in parallel.
# Step 2: Create 3*3 files containing the Python code write_text. These files will later process information from the parent process and return data to the parent. 
# Step 3: Spawn 3*3 subprocesses using subprocess.Popen(). Each of the subprocesses receives data (a row of A and a column of B) from the parent to do multiplication on. The data is sent via subprocess.communicate(). The data is received by the child via sys.stdin.read(). 
# Step 4: The function subprocess.communicate() returns the return value of the function calculate_vector. This data transfer from the child to the parent happens through the child using sys.stdout.write().
# Step 5: Gather the return data from subprocesses and store them into a product_matrix. 



# Declare two matrices 3 by 3
matrix_A = np.array([[1,2,3],[4,5,6],[7,8,9]])
matrix_B = np.array([[0,1,2],[3,4,5],[6,7,8]])

# Print out the two matrices to the console
print('matrix A = \r\n', matrix_A, '\r\n')
print('matrix B = \r\n', matrix_B)


# Declare an empty array of subprocesses with 9 elements
subprocesses = np.empty(9, dtype=object)

# Name the subprocesses as subprocess_0, subprocess_1, etc., through subprocess_8
for i in range(9):
	subprocesses[i] = 'subprocess_'+str(i)



# Python code to be written into the 9 files = subprocesses
# The parent process is passing string r in the form '[a b c][d e f]' to a subprocess. Need to separate the string into arrays '[a b c]' and '[d e f]' to use in function calculate_vector. 
# sys.stdin.read() takes input from the parent process through stdin=PIPE.
# sys.stdout.write() sends data from the subprocess to the parent process via stdout=PIPE.
write_text = textwrap.dedent('''\
	import numpy as np
	import sys
	def calculate_vector(row, column):
		vector = np.dot(row, column)
		return vector
	input = sys.stdin.read()  
	row_array = np.fromstring(input[1:6], dtype=int, sep=' ')
	column_array = np.fromstring(input[8:13], dtype=int, sep=' ')
	vector = calculate_vector(row_array, column_array)
	sys.stdout.write(str(vector))     
		 ''')



# Declare an empty array holding the matrix product
matrix_product_1D = np.empty(9, dtype=object)

print('\n')




# Spawn multiple subprocesses for each combination of rows of A and columns of B using subprocess.Popen

# Note that the variable data_from_child contains the return information from a subprocess. We print it here to the console using the print() function. 

sub_i = 0
for row in matrix_A: 
	for column in matrix_B.T:
		file_name = subprocesses[sub_i]+'.py'     # create a Python filename for each of the 9 subprocesses
		with open(file_name, 'w') as f:
			f.write(write_text)
		r = str(row)
		r += str(column)
		subprocesses[sub_i] = subprocess.Popen(['python.exe', file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf8')
		print('Parent process sending ', r, ' to child ', file_name)
		data_from_child = subprocesses[sub_i].communicate(r)[0]
		matrix_product_1D[sub_i] = data_from_child
		print(file_name + ' has returned ', data_from_child, '\r\n')
		sub_i = sub_i + 1


# Declare a matrix to hold the product
matrix_product = np.empty((3, 3), dtype=int)

j = 0
for i in range(matrix_product.shape[0]):
	matrix_product[i] = matrix_product_1D[j:j+3]
	j = j + 3
	
print('\n')
print('Product matrix =\r\n', matrix_product)

