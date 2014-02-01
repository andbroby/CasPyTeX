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
	zeroessofar=True
	figurecounter=0
	addzeroes=False
	rounddown=False
	aftercomma=False
	newstrarray=[]
	for index,figure in enumerate(numberstr):
		if figure==".":
			aftercomma=True
		if addzeroes:
			if aftercomma:
				break
			newstrarray.append(0)
			continue
		if zeroessofar and figure not in ["0","."]:
			zeroessofar=False
			figurecounter=1
		if not zeroessofar:

			if figurecounter!=sigfig+1 and figure!=".":
				figurecounter+=1
			elif figurecounter==sigfig+1:
				if figure==".":
					if int(numberstr[index+1])>=5:
						newstrarray[index-1]+=1
						addzeroes=True
						if not aftercomma:
							newstrarray.append(0)
						continue
					elif int(numberstr[index+1])<5:
						rounddown=True
						addzeroes=True
						if not aftercomma:
							newstrarray.append(0)
						continue
				if int(numberstr[index])>=5:
					newstrarray[index-1]+=1
					addzeroes=True
					if not aftercomma:
						newstrarray.append(0)
					continue
				elif int(numberstr[index])<5:
					rounddown=True
					addzeroes=True
					if not aftercomma:
						newstrarray.append(0)
					continue
		if figure!=".":
			newstrarray.append(int(figure))
		else:
			newstrarray.append(".")
	if rounddown==True:
		return "".join([str(n) for n in newstrarray])
	else:
		newarr=newstrarray[:]
		while True:
			oldarr=newarr[:]
			newarr=[]
			for index,figure in enumerate(oldarr):
				if figure==10:
					if newarr[index-1]==".":
						newarr[index-2]+=1
						newarr.append(0)
					else:
						if index==0:
							newarr.insert(1)
							newarr.append(0)
						else:
							newarr[index-1]+=1
							newarr.append(0)
				else:
					newarr.append(figure)
			if 10 not in newarr:
				return "".join([str(n) for n in newarr])
