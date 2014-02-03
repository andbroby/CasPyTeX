def splitstringbyindexes(str,indexes):
	"""
	Splits a string by the indexes
	"0123456" with indexes [3] becomes ["012","456"]
	"""
	returnarr=[]
	for index,val in enumerate(indexes):
		if index==0:
			returnarr.append(str[:val])
		else:
			returnarr.append(str[indexes[index-1]+1:val])

	returnarr.append(str[val+1:])
	#print("SPLIT LIKE DIS",returnarr)
	return returnarr
def stringtoparentespar(str):
	"""
	Returns and array of the bracket pair indexes (brackets on the same level)
	"""
	startlist=[]
	slutlist=[]
	for index,val in enumerate(list(str)):
		if val=="(":startlist.append(index)
		elif val==")":slutlist.append(index)
	return parentespar1(startlist,slutlist)
def isinsideparentes(str,index):
	"""
	Finds out if an index in the string is inside any brackets
	"""
	parentespar=stringtoparentespar(str)
	for n in parentespar:
		if index>n[0] and index<n[1]:return True
	return False
def parentespar1(startlist,slutlist):
	"""
	Inputs a list of startbracket indexes, and a list of endbracket indexes,
	and returns an array of matched bracket indexes
	"""
	if len(startlist)!=len(slutlist):
		raise EOFError("Mismatching brackets")
	parlist=[]
	startlist.reverse()
	while startlist!=[]:
		for n in slutlist[:]:
			breakitall=False
			for p in startlist[:]:
				if n>p:
					parlist.append([p,n])
					startlist.remove(p)
					slutlist.remove(n)
					breakitall=True
					break
			if breakitall:break
	return parlist
def findcharoutsideparentes(char,str):
	"""
	Returns an array of index that match the char in the string outside 
	any brackets
	"""
	returnindexes=[]
	for index in range(len(str)):
		if str[index]==char and not isinsideparentes(str,index):
			returnindexes.append(index)
	return returnindexes
def ydersteparentes(parentespar):
	"""
	Returns the indexes of the outer bracket
	"""
	parentespar.sort()
	if parentespar==[]:return None
	return(parentespar[0])

def sigfigroundfromstr(numberstr,sigfig):
	"""
	Inputs a numberstring and a int of the amount if significant figures,
	and returns the rounded numberstring 
	"""
	if sigfig==0:
		raise ValueError("You can't have 0 significant figures")
	def trimZero(numberstr):
		if numberstr.split(".")[-1] == "0":
			return numberstr.split(".")[0]
		return numberstr 

	floatS = float(numberstr)
	leadingZeroes = 0
	numberArray = [str(int(numberstr.split(".")[0])), str(int(numberstr.split(".")[-1]))]

	if len(numberArray) > 1:
		i = 0
		while (numberArray[-1][i] == "0"):
			leadingZeroes += 1
			i += 1

	if numberArray[0] == "0" and not leadingZeroes:
		return str(round(floatS, sigfig))
	elif leadingZeroes:
		decimals = len(numberArray[-1]) if floatS - int(floatS) > 0 else 0
		s2 = numberArray[-1][leadingZeroes:]
		sigfig = len(s2) - sigfig
		s2 = round(float(s2), -1*sigfig)
		s2 = s2 / 10**decimals
		return trimZero(str(s2))
	else:
		integerLen = len(numberArray[0])
		sigfig = -1*(integerLen - sigfig)
		roundedString = trimZero(str(round(floatS, sigfig)))
		return roundedString

	
