
# ACTHUNG: no name/address sanitation in these tests

from Duplicated import *




#####
# 1 #
#####
def test1_0():
	d1 = {'name':"bar a treta", 'address':'r. da boavista n 50, porto, portugal'}
	d2 = {'name':"bar da treta", 'address':'av. da boavista n 50, porto, portugal'}
	
	if isDup_0(d1,d2,min_ratio=85):
		return True
	else:
		return False

def test1_1():
	d1 = {'name':"bar a treta", 'address':'r. da boavista n 50, porto, portugal'}
	d2 = {'name':"bar da treta", 'address':'av. sá da bandeira n 50, porto, portugal'}

	if not isDup_0(d1,d2,min_ratio=90) and isDup_0(d1,d2,min_ratio=50):
		return True
	else:
		return False

		

#####
# 2 #
#####
# default: max_radius = 50 meters
def test2_0():
	
	d1 = {'lon':8.0,'lat':40.0}
	d2 = {'lon':8.0,'lat':40.0}

	if isDup_1(d1,d2) == True:
		return True
	else:
		return False


def test2_1():
	
	d1 = {'name': 'john doe something', 'lon':8.0,'lat':40.0}
	d2 = {'name': 'joqw do something', 'lon':8.0,'lat':40.0}

	if isDup_1(d1,d2):
		return True
	else:
		return False

def test2_2():
	
	d1 = {'name': 'john doe something', 'lon':8.0,'lat':40.0}
	d2 = {'name': 'joqw do something', 'lon':8.0,'lat':40.0}

	if not isDup_1(d1,d2,checkname=True ):
		return True
	else:
		return False


def test2_3():
	
	d1 = {'name': 'john doe something', 'lon':8.0,'lat':40.0}
	d2 = {'name': 'john do something', 'lon':8.0,'lat':40.0}

	if isDup_1(d1,d2,checkname=True ):
		return True
	else:
		return False

#####
# 3 #
#####
def test3_0():
	
	d1 = {'name':"bar a treta", 'address':'r. da boavista n 50, porto, portugal'}
	d2 = {'name':"bar da treta", 'address':'av. da boavista n 50, porto, portugal'}

	if isDup_2(d1,d2,min_ratio=85) and not isDup_2(d1,d2,min_ratio=90):
		return True
	else:
		return False

def test3_1():
	
	d1 = {'name':"bar a treta", 'address':'r. da boavista n 50, porto, portugal'}
	d2 = {'name':"bar da treta", 'address':'av. sá da bandeira n 50, porto, portugal'}

	if not isDup_2(d1,d2,min_ratio=80) and isDup_2(d1,d2,min_ratio=40):
		return True
	else:
		return False





#####
# 4 #
#####
def test4_0():
	
	d1 = {'name':"bar treta", 'address':'da boavista n 50, porto, portugal'}
	d2 = {'name':"bar da treta", 'address':'av. da boavista n 50, porto, portugal'}

	if isDup_3(d1,d2,min_size=4):
		return True
	else:
		return False

def test4_1():
	
	d1 = {'name':"bar a treta", 'address':'praceta da boavista n 50, porto, portugal'}
	d2 = {'name':"bar da treta", 'address':'avenida da boavista n 50, porto, portugal'}

	if not isDup_3(d1,d2,min_size=4):
		return True
	else:
		return False



def runTests():
	if test1_0() and test1_1():
		print ("TEST 1 [OK]")
	else:
		print ("TEST 1 [NOT OK]")


	if test2_0() and test2_1() and test2_2() and test2_3():
		print ("TEST 2 [OK]")
	else:
		print ("TEST 2 [NOT OK]")

	if test3_0() and test3_1():
		print ("TEST 3 [OK]")
	else:
		print ("TEST 3 [NOT OK]")

	if test4_0() and test4_1():
		print ("TEST 4 [OK]")
	else:
		print ("TEST 4 [NOT OK]")



if __name__ == '__main__':
	runTests()
