####################################################################
#
#
#
#	install:
# 		pip install fuzzywuzzy
# 		pip install python-Levenshtein
# 		pip install geopy
# 		pip install phonetics
#
#
####################################################################

import unicodedata
import re
import sys

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import geopy.distance
import phonetics





abreviaturas = {
		"al":"alameda", "av":"avenida", "az":"azinhaga", "br":"bairro",
		"bc":"beco", "cc":"calcada", "ccnh":"calcadinha", "cam":"caminho",
		"csl":"casal", "esc":"escadas", "escnh":"escadinhas", "estr":"estrada",
		"est":"estrada", "en":"estrada nacional", "jrd":"jardim", "lg":"largo",
		"loteam":"loteamento", "pq":"parque", "pto":"patio", "pc":"praca",
		"pct":"praceta", "prolng":"prolongamento", "qta":"quinta", "rot":"rotunda",
		"r":"rua", "transv":"transversal", "tv":"travessa", "trav":"travessa",
		"urb":"urbanizacao", "vl":"vila", "zn":"zona", "cv":"cave", "dto":"direito",
		"esq":"esquerdo", "ft":"frente", "hab":"habitacao", "lj":"loja",
		"rc":"res do chao", "slj":"sobre loja", "scv ":"sub cave ", "bl ":"bloco ",
		"edf ":"edificio ", "lt ":"lote ", "tr ":"torre ", "vv ":"vivenda ",
		"alf":"alferes", "alm":"almirante", "arq":"arquiteto", "brig":"brigadeiro",
		"cap":"capitao", "cmdt":"comandante", "comend":"comendador", "cons":"conselheiro",
		"cor":"coronel", "d":"dom", "d":"dona", "dr":"doutor", "dr":"doutora",
		"dq":"duque", "bem":"embaixador", "eng":"engenheira", "eng":"engenheiro",
		"fr":"frei", "gen":"general", "inf":"infante", "mq":"marques",
		"presid":"presidente", "prof":"professor", "prof":"professora",
		"s":"sao", "sarg":"sargento", "ten":"tenente", "visc":"visconde",
		"ass":"associacao", "inst":"instituto", "lug":"lugar", "min":"ministerio",
		"proj":"projetada", "numero":"sem", "soc":"sociedade", "univ":"universidade",
		"b":"bloco", "e":"edificio", "l":"lote", "t":"torre", "n":"numero"
}



############################
#	SETUP AND CLEANING OPS #
############################

# replace all special chars for non special
# ex: áâãàç -> aaac
def replacePTChars(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


# if not number or letter then be replaced by by_what
def replaceAllNonAlfaNum(s, by_what=" "):
	return re.sub('[^A-Za-z0-9]+', by_what, s)
		
# including trailing spaces
def removeAllExtraSpaces(s):
	return " ".join(s.split())
	
# basically, it joins all words into one
def removeAllSpaces(s):		
	return s.replace(' ','')


# replaces all tokens that have a correspondence in the abreviaturas list
# ex: s = "EN 5 lt 10 porto" -> "ESTRADA NACIONAL 5 LOTE 10 PORTO"  
def replaceAbrevs(addr):
	tokens = addr.split(' ')
	for i in range(len(tokens)):
		if tokens[i] in abreviaturas:
			tokens[i] = abreviaturas[tokens[i]]
	return ' '.join(tokens)


# in some algorithms small words can be considered noise and as such
# irrelevant
def removeSmallWords(s):
	remove_list = ['o','a','e','de','do','da','dos','das']
	word_list = s.split()	
	ss = ' '.join([i for i in word_list if i not in remove_list])
	return ss


def keepOnlyWords(s):
	return [s1 for s1 in s if s1.isalpha()]

def keepIfMinSize(s,n):
	return [s1 for s1 in s if (len(s1) >= n or not s1.isalpha()) ]


# prepare/clean - remove/replace
def sanitizeStr(data, remove_all_spaces = False, replace_abrv = False):
	temp = data.lower()	
	temp = replacePTChars(temp)
	temp = replaceAllNonAlfaNum(temp)
	if replace_abrv:	
		temp = replaceAbrevs(temp)		# only for addresses
	temp = removeSmallWords(temp)
	if not remove_all_spaces:
		temp = removeAllExtraSpaces(temp)
	else:			
		temp = removeAllSpaces(temp)	# only for phonetics
	return temp

##############
# OPERATIONS #
##############
'''
def createData(name = None, address = None, is_parent = None, nif = None, ent_type = None):
	data = {}
	
	if name:
		data['name'] = name
	if address:
		data['address'] = address
	if is_parent:
		data['is_parent'] = is_parent
	if nif:
		data['nif'] = nif
	if ent_type:
		data['ent_type'] = ent_type
	
	return data
'''

def getRatioNome(str1, str2):
	return fuzz.ratio(str1,str2)
		
def getRatioMorada(str1, str2):
	return fuzz.ratio(str1,str2)

def getPhoneticsRatioNome(str1, str2):
	return fuzz.ratio(phonetics.metaphone(str1),phonetics.metaphone(str2))
		
def getPhoneticsRatioMorada(str1, str2):
	return fuzz.ratio(phonetics.metaphone(str1),phonetics.metaphone(str2))

# check if the first numbers of s1 and s2 match
def isSameNumber(s1, s2, keyword):
	match1 = re.search(keyword + '\s*(\d+)', s1)
	match2 = re.search(keyword + '\s*(\d+)', s2)
	if match1 and match2:
		if match1.group(1) == match2.group(1):
			return True
	return False


def isNameIn(s1, s2 ,n):
#	if sanitize:
#		s1 = removeAllExtraSpaces(s1)
#		s2 = removeAllExtraSpaces(s2)
	temp1 = keepIfMinSize(s1.split(" "),n)
	temp2 = keepIfMinSize(s2.split(" "),n)
	return set(temp1).issubset(temp2) or set(temp2).issubset(temp1)

def isAddressIn(s1, s2 ,n):
#	if sanitize:
#		s1 = removeAllExtraSpaces(s1)
#		s2 = removeAllExtraSpaces(s2)
	temp1 = keepIfMinSize(s1.split(" "),n)
	temp2 = keepIfMinSize(s2.split(" "),n)
	return set(temp1).issubset(temp2) or set(temp2).issubset(temp1)


##############
# ALGO IMPL  #
##############

# returns true if similar
# data: {name=not null}
# if check_addresses => check both name and address
def isDup_0(data1, data2, min_ratio = 90, check_addresses = True):
	if 'name' not in data1 or 'name' not in data2:
		raise RuntimeError('Error: missing name(s)!')
	if check_addresses:
		if 'address' not in data1 or 'address' not in data2:
			raise RuntimeError('Error: missing address(s)!')


	isBar = False
	isLoja = False
	
	if ' bar ' in data1['name']:
		isBar = True
	if ' loja ' in data1['name']:
		isLoja = True
	
	if check_addresses:
		comp_result = getRatioNome(data1['name'],data2['name']) > min_ratio and getRatioMorada( data1['address'], data2['address']) > min_ratio
	else:
		comp_result = getRatioNome(data1['name'],data2['name']) > min_ratio
	if comp_result:
		if isBar:
			if not isSameNumber(data1['name'],data2['name'],'bar'):
				return False
		if isLoja:
			if not isSameNumber(data1['name'],data2['name'],'loja'):
				return False	

		return True
	
	return False




# returns true if similar
# data: {lat=not null, lon=not null}
# if checkname then if (lat,lon)1 ~(lat,lon)2 then if getRatioNome(name1, name2) > 90 or isNameIn then true
def isDup_1(data1, data2, max_radius = 50, checkname = False):
	if 'lat' not in data1 or 'lat' not in data2:
		raise RuntimeError('Error: missing latitude(s)!')
	if 'lon' not in data1 or 'lon' not in data2:
		raise RuntimeError('Error: missing longitude(s)!')	
	
	
	coords_1 = (data1['lat'],data1['lon'])
	coords_2 = (data2['lat'],data2['lon'])
	if geopy.distance.distance(coords_1, coords_2).meters < max_radius:
		
		if checkname and data1['name'] and data2['name']:
			return (getRatioNome(data1['name'],data2['name']) > 90 or isNameIn(data1['name'],data2['name'],4))

				
		return True
		
	return False


# returns true if similar
# it only works until the first space => remove all spaces
# data: {name=not null}
def isDup_2(data1, data2, min_ratio = 90, check_addresses = True):
	if 'name' not in data1 or 'name' not in data2:
		raise RuntimeError('Error: missing name(s)!')
	if check_addresses:
		if 'address' not in data1 or 'address' not in data2:
			raise RuntimeError('Error: missing address(s)!')			
	
	
	isBar = False
	isLoja = False	

	if ' bar ' in data1['name']:
		isBar = True
	if ' loja ' in data1['name']:
		isLoja = True
	
	if check_addresses:
		comp_result = getPhoneticsRatioNome(data1['name'],data2['name']) > min_ratio and getPhoneticsRatioNome(data1['address'],data2['address']) > min_ratio
	else:
		comp_result = getPhoneticsRatioNome(data1['name'],data2['name']) > min_ratio
	
	if comp_result:
		if isBar:
			if not isSameNumber(data1['name'],data2['name'],'bar'):
				return False
		if isLoja:
			if not isSameNumber(data1['name'],data2['name'],'loja'):
				return False
		
		return True
		
	return False


# returns true if similar
# data: {name=not null}
def isDup_3(data1, data2, min_size = 4, check_addresses = True):
	if 'name' not in data1 or 'name' not in data2:
		raise RuntimeError('Error: missing name(s)!')
	if check_addresses:
		if 'address' not in data1 or 'address' not in data2:
			raise RuntimeError('Error: missing address(s)!')	
	
	if check_addresses:
		if isNameIn(data1['name'],data2['name'],4) and isAddressIn(data1['address'],data2['address'],4):	
			return True
	else:
		if isNameIn(data1['name'],data2['name'],4):	
			return True
	
	return False



##################
# MAIN DUP FUNC  #
##################


def isDup(	data1, 
			data2, 
			min_ratio = 90, 
			max_radius = 50, 
			min_size = 4, 
			ignore=[], 
			order = [0,1,2,3], 
			sanitize = True, 
			checkname = False,
			check_addresses = True):

	"""
		main function ...
		
		
		data1: entity's 1 data, in json
		data2: entity's 2 data, in json
		min_ratio: minimum ratio for the fuzz.ratio (algo 0 and 2)
		max_radius: maximum distance in meters, to consider both entities 
					to be at the same place (algo 1)
		min_size: descart all words of size lesser than 4 (algo 3)
		ignore: list of algorithms to ignore
		order: which order the algorithms will be applied
		sanitize: sanitize the entry data (names and addresses) - remove 
					extra spaces, special chars, ...
		checkname: should algorithm 1 check not only the distance but 
					also the name? (algo 1)
		check_addresses: check names and addresses or only the names? (algo 0,2,3)
	"""

	
	if sanitize:
		if 'name' in data1 and data1['name']:
			data1['name'] = sanitizeStr(data1['name'])		
		if 'name' in data2 and data2['name']:
			data2['name'] = sanitizeStr(data2['name'])
		if check_addresses:
			if 'address' in data1 and data1['address']:
				data1['address'] = sanitizeStr(data1['address'], replace_abrv = True)
			if 'address' in data2 and data2['address']:
				data2['address'] = sanitizeStr(data2['address'], replace_abrv = True)
	
	for algo in order:
		if algo == 0 and 0 not in ignore:
			try:
				if isDup_0(data1, data2, min_ratio, check_addresses = check_addresses):
					return {"DUPLICATED":1,"ALGO":0}
			except Exception as e:
				pass

		if algo == 1 and 1 not in ignore:
			try:
				if isDup_1(data1, data2, max_radius, checkname = checkname):
					return {"DUPLICATED":1,"ALGO":1}
			except Exception as e:
				pass
		
		if algo == 2 and 2 not in ignore:
			try:
				d1 = data1.copy()
				d2 = data2.copy()
				#if sanitize:
				if 'name' in data1 and data1['name']:
					d1['name'] = removeAllSpaces(data1['name'])		
				if 'name' in data2 and data2['name']:
					d2['name'] = removeAllSpaces(data2['name'])
				if check_addresses:
					if 'address' in data1 and data1['address']:
						d1['address'] = removeAllSpaces(data1['address'])
					if 'address' in data2 and data2['address']:
						d2['address'] = removeAllSpaces(data2['address'])

				if isDup_2(d1, d2, min_ratio, check_addresses = check_addresses):
					return {"DUPLICATED":1,"ALGO":2}
			except Exception as e:
				pass	


		if algo == 3 and 3 not in ignore:
			try:
				if isDup_3(data1, data2, min_size, check_addresses = check_addresses):
					return {"DUPLICATED":1,"ALGO":3}			
			except Exception as e:
				pass
	return {"DUPLICATED":0}





'''
d1 = {'name': 'john doe something', 'lon':8.0,'lat':40.0}
d2 = {'name': 'joqw do something', 'lon':8.0,'lat':40.0}
	
print(isDup_1(d1,d2,checkname=True ))
'''


'''
# create the data structures
d1 = {'name':'a loja 1 a treta', 'address': 'r. da boavista n 50, porto, portugal'}
d2 = {'name':'a loja 1 da treta', 'address': 'av. da boavista n 50, porto, portugal'}
	
# sanitize ... only if needed
# note that if isDup_2 => also set remove_all_spaces = True
d1['name'] = sanitizeStr(d1['name'])
d2['name'] = sanitizeStr(d2['name'])
d1['address'] = sanitizeStr(d1['address'], replace_abrv = True)
d2['address'] = sanitizeStr(d2['address'], replace_abrv = True)
	
print( isDup_0(d1,d2,min_ratio=85))
'''
'''
qwe1 = 'address 1 qwe dfsd'
qwe2 = 'address'
qwe3 = None
print (len(qwe1.split()))
print (len(qwe2.split()))
print (len(qwe3.split()))
'''
