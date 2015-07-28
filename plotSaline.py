#!/usr/bin/env python

import sys

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

wells = [0] * 64
with open(sys.argv[1], 'r') as my_file: 
	#parse file 
	fileNumber = 0
	inRead = False
	for line in my_file:
		if len(line.split()) == 0:
			rowCount = 0 # set row count to zero whenever you see a blank line
			continue

		word = line.split()[0]
		if "Run" in word:
			run = word[3:]
			if fileNumber > 1:
				#close old file
				wfile.close()
		if "Card" in word:
			card = word[8:]
		if "TX" in word:
			TX = word[2:]
			sys.stdout.write('run' + run + 'TX' + TX + 'Card' + card + "\n")
			wfile = open('run' + run + 'TX' + TX + 'Card' + card + '.dat', 'w+')
			inRead = True
			col = 0
			continue


		if inRead:
			if not is_number(line.split()[0]):
				inRead = False
				#close old file
				wfile.close()
				word = line.split()[0]

			else:
				# here we parse the data
				for i in range(0,8):
					wells[col*8 + i] = line.split()[i]
				if col < 7:
					col += 1
				else:
					col = 0
					for j in range(0,64):
						wfile.write(str(wells[j]) + " " )
					wfile.write("\n")

	wfile.close()
