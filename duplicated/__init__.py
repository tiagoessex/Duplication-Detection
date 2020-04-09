"""

Input data:
	data1: {name, address, lat, lon}
	data2: {name, address, lat, lon}


Returns:

	If an algorithm determinate that data1 and data2 are the same, then	returns the struct 
		{"DUPLICATED":1,"ALGO":X}
	where X is the algorithm number.
	
	Else, returns:
		{"DUPLICATED":0}


Usage example:


	using the main function:
	
		d1 = {'name':"a loja 1 a treta", 'address':'r. da boavista n 50, porto, portugal'}
		d2 = {'name':"a loja 1 da treta", 'address':'av. da boavista n 50, porto, portugal'}

		print (t.isDup(d1,d2))	# returns {'DUPLICATED': 1, 'ALGO': 3}


	using a particular algorithm:
	
		d1 = {'name':"bar a treta", 'address':'r. da boavista n 50, porto, portugal'}
		d2 = {'name':"bar da treta", 'address':'av. da boavista n 50, porto, portugal'}
		
		if isDup_0(d1,d2,min_ratio=85):
			return True
		else:
			return False
	

requirements:
	Python 3.7.x
	fuzzywuzzy
	geopy
	phonetics

"""

from .Duplicated import *

__version__ = "2.0.0"




