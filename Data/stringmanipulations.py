def splitstringbyindexes(str,indexes):
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
	startlist=[]
	slutlist=[]
	for index,val in enumerate(list(str)):
		if val=="(":startlist.append(index)
		elif val==")":slutlist.append(index)
	return parentespar1(startlist,slutlist)
def isinsideparentes(str,index):
	parentespar=stringtoparentespar(str)
	for n in parentespar:
		if index>n[0] and index<n[1]:return True
	return False
def parentespar1(startlist,slutlist):
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
	returnindexes=[]
	for index in range(len(str)):
		if str[index]==char and not isinsideparentes(str,index):
			returnindexes.append(index)
	return returnindexes
def ydersteparentes(parentespar):
	parentespar.sort()
	if parentespar==[]:return None
	return(parentespar[0])
