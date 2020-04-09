
import duplicated as duplicated


print (duplicated.__version__)


# SANITIZED

d1 = {'name':"a loja 1 a treta", 'address':'r. da boavista n 50, porto, portugal'}
d2 = {'name':"a loja 1 da treta", 'address':'av. da boavista n 50, porto, portugal'}

print (duplicated.isDup(d1,d2))	# returns {'DUPLICATED': 1, 'ALGO': 3}

d1 = {'name':"a loja 1 a treta", 'address':'r. da cdsxczxcds n 50, porto, portugal', "lon":10,"lat":20}
d2 = {'name':"a loja 1 da treta", 'address':'av. da boavista n 50, porto, portugal', "lon":10.005,"lat":20}

print (duplicated.isDup(d1,d2))	# returns {'DUPLICATED': 0}


d1 = {'name':"a loja 1 a treta", 'address':'r. da cdsxczxcds n 50, porto, portugal',"lon":10,"lat":20}
d2 = {'name':"a loja 1 da treta", 'address':'av. da boavista n 50, porto, portugal', "lon":10.00005,"lat":20}

print (duplicated.isDup(d1,d2))	# returns {'DUPLICATED': 1, 'ALGO': 1}


d1 = {'name':"a loja 1 a treta", 'address':'r. da cdsxczxcds n 50, porto, portugal', "lon":10,"lat":20}
d2 = {'name':"a loja 1 da treta", 'address':'av. da boavista n 50, porto, portugal',  "lon":10.00005,"lat":20}

print (duplicated.isDup(d1,d2, ignore=[1]))	# returns {'DUPLICATED': 0}

d1 = {'name':"a loja 1 a treta", 'address':'avenida da boavista n 50, porto, portugal'}
d2 = {'name':"a loja 1 da treta", 'address':'av. da boavista n 50, porto, portugal'}

print (duplicated.isDup(d1,d2,min_ratio = 85))	# returns {'DUPLICATED': 1, 'ALGO': 0}

d1 = {'name':"a loja 1 a treta", 'address':'avenida da boavista n 50, porto, portugal'}
d2 = {'name':"a loja 1 da treta", 'address':'av. da boavista n 50, porto, portugal'}

print (duplicated.isDup(d1,d2,min_ratio = 85, order=[3,2,1,0]))	# returns {'DUPLICATED': 1, 'ALGO': 3}


d1 = {'name':"a loja 1 a treta", 'address':'r. da cdsxczxcds n 50, porto, portugal', "lon":10,"lat":20}
d2 = {'name':"a loja 1 da treta", 'address':'av. da boavista n 50, porto, portugal',  "lon":12.00005,"lat":20}

print (duplicated.isDup(d1,d2))	# returns {'DUPLICATED': 0}


d1 = {'name':"name1 name1", 'address':'r. da cdsxczxcds n 50, porto, portugal', "lon":10,"lat":20}
d2 = {'name':"name2 name2", 'address':'av. da boavista n 50, porto, portugal',  "lon":12.00005,"lat":20}

print (duplicated.isDup(d1,d2, max_radius=1000000 ))	# returns {'DUPLICATED': 1, 'ALGO': 1}



d1 = {'name':"name1 name1", 'address':'r. da cdsxczxcds n 50, porto, portugal',"lon":10,"lat":20}
d2 = {'name':"name1 name11", 'address':'av. da boavista n 50, porto, portugal', "lon":10.00005,"lat":20}

print (duplicated.isDup(d1,d2, checkname = True))	# returns {'DUPLICATED': 1, 'ALGO': 1}


d1 = {'name':"name1 name1", 'address':'r. da cdsxczxcds n 50, porto, portugal',"lon":10,"lat":20}
d2 = {'name':"name2 name2", 'address':'av. da boavista n 50, porto, portugal', "lon":10.00005,"lat":20}

print (duplicated.isDup(d1,d2, checkname = True))	# returns {'DUPLICATED': 0}
