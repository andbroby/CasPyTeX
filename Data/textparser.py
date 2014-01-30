"""
TextToCAS tager matematik og konverterer det til CAS'en


(a+b)-2*a^3

"""
from sys import exit


import Entityclass as Entities
from stringmanipulations import *
from debugger import *
import equationsolver as equations
def TextToCAS(instring,recursions=0):
	origin=instring
	instring=instring.replace("-","+-").replace("++","+").replace("--","+").replace("(+-","(-")
	newinstring=""
	for index,char in enumerate(instring):
		if char=="_":
			if index==0:
				pass
			elif instring[index-1] not in ["*","/","+","-","("]:
				if index>=2 and instring[index-2]=="-":
					pass
				elif index+1<len(instring) and instring[index+1]=="{":
					pass
				else:
					newinstring+="*"
		newinstring+=char
	instring=newinstring[:]

	#if instring[0]=="+":instring=instring[1:]
	if instring[0]=="+" or instring[0]=="*":
		instring=instring[1:]
	if instring[0]=="-":
		return Entities.product([Entities.number(["-1"]),TextToCAS(instring[1:])])
	if [0,len(instring)-1] in stringtoparentespar(instring):
		instring=instring[1:-1]
	if ydersteparentes(stringtoparentespar(instring))==[0,len(instring)-1]:instring=instring[1:-1]
	#debug(3,"new string: "+str(instring))
	#foerst addition
	plusses=findcharoutsideparentes("+",instring)
	if plusses!=[]:
		debug(3,recursions*"    "+origin+" bliver til ADDITION "+str(splitstringbyindexes(instring,plusses)) )
		return Entities.addition([TextToCAS(n,recursions+1) for n in splitstringbyindexes(instring,plusses)])
	#saa produkt
	gangetegn=findcharoutsideparentes("*",instring)
	if gangetegn!=[]:
		debug(3,recursions*"    "+origin+" bliver til PRODUKT "+str(splitstringbyindexes(instring,gangetegn)) )
		return Entities.product([TextToCAS(n,recursions+1) for n in splitstringbyindexes(instring,gangetegn)])
	#saa division
	broekstreger=findcharoutsideparentes("/",instring)
	if broekstreger!=[]:
		if len(broekstreger)>1:
			debug(1,"TVETYDIG BROEK, STOPPER PROGRAMMET")
			exit()
		debug(3,recursions*"    "+origin+" bliver til DIVISION "+str(splitstringbyindexes(instring,broekstreger) ))
		return Entities.division([TextToCAS(n,recursions+1) for n in splitstringbyindexes(instring,broekstreger)])
	#saa potenser
	eksponenttegn=findcharoutsideparentes("^",instring)
	if eksponenttegn!=[]:
		if len(eksponenttegn)>1:
			debug(1,"TVETYDIG POTENS, STOPPER PROGRAMMET")
			exit()
		debug(3,recursions*"    "+origin+" bliver til POTENS "+str(splitstringbyindexes(instring,eksponenttegn)) )
		return Entities.potens([TextToCAS(n,recursions+1) for n in splitstringbyindexes(instring,eksponenttegn)])
	#saa funktioner
	for index,char in enumerate(instring):
		allowedchars=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
		if char=="(" and instring[index-1] in allowedchars:
			startbracket=index
			#proceeds to find the string that defines the function, ie sin(2x)
			for indexk in range(index-1,-1,-1):
				if instring[indexk] not in allowedchars or indexk==0:
					functstart=indexk
					break
			bracketoffset=1
			for indexk in range(index+1,len(instring)):
				if instring[indexk]=="(":
					bracketoffset+=1
				elif instring[indexk]==")":
					bracketoffset-=1
					if bracketoffset==0:
						funcend=indexk
						break
			funcstring=instring[functstart:startbracket]
			insidebrackets=instring[startbracket+1:funcend]
			#print(funcstring,insidebrackets)
			if funcstring=="sin":
				debug(3,recursions*"    "+origin+" bliver til Sine: "+insidebrackets )

				return Entities.sine([TextToCAS(insidebrackets,recursions+1)])
			elif funcstring=="cos":
				debug(3,recursions*"    "+origin+" bliver til Cosine: "+insidebrackets )
				return Entities.cosine([TextToCAS(insidebrackets,recursions+1)])
			elif funcstring=="tan":
				debug(3,recursions*"    "+origin+" bliver til Tangent: "+insidebrackets )
				return Entities.tangent([TextToCAS(insidebrackets,recursions+1)])

			elif funcstring=="arcsin" or funcstring=="asin":
				debug(3,recursions*"    "+origin+" bliver til Arcsine: "+insidebrackets )
				return Entities.arcsine([TextToCAS(insidebrackets,recursions+1)])
			elif funcstring=="arccos" or funcstring=="acos":
				debug(3,recursions*"    "+origin+" bliver til Arccosine: "+insidebrackets )
				return Entities.arccosine([TextToCAS(insidebrackets,recursions+1)])
			elif funcstring=="arctan" or funcstring=="atan":
				debug(3,recursions*"    "+origin+" bliver til Arctangent: "+insidebrackets )
				return Entities.arctangent([TextToCAS(insidebrackets,recursions+1)])

			elif funcstring=="ln" or funcstring=="Ln":
				debug(3,recursions*"    "+origin+" bliver til Natlogarithm: "+insidebrackets )
				return Entities.natlogarithm([TextToCAS(insidebrackets,recursions+1)])
			elif funcstring=="log" or funcstring=="Log":
				debug(3,recursions*"    "+origin+" bliver til comlogarithm: "+insidebrackets )
				return Entities.comlogarithm([TextToCAS(insidebrackets,recursions+1)])

			elif funcstring=="sqrt":
				debug(3,recursions*"    "+origin+" bliver til squareroot: "+insidebrackets )
				return Entities.squareroot([TextToCAS(insidebrackets,recursions+1)])
			else:
				debug(3,recursions*"    "+origin+" bliver til unknownfunction: "+funcstring+"("+insidebrackets+")" )
				return Entities.unknownfunction(funcstring,TextToCAS(insidebrackets,recursions+1))


	if "+" in instring or "*" in instring or "/" in instring or "(" in instring or ")" in instring:
		#print("OIOI",instring,ydersteparentes(stringtoparentespar(instring))[0])
		if instring[0]=="-" and ydersteparentes(stringtoparentespar(instring))[0]==1 and ydersteparentes(stringtoparentespar(instring))[1]==len(instring)-1:
			return Entities.product([Entities.number(["-1"]),TextToCAS(instring[1:])])
		debug(1,"FEJL: TextToCAS vil lave number instance med regnetegn i udtrykket\nStopper programmet")
		exit()
	#til sidst laves number instance
	if instring[0]=="-":
		debug(3,recursions*"    "+origin+" bliver til PRODUKT ['-1',"+instring[1:]+"]")
		debug(3,(recursions+1)*"    "+"-1"+" er et \"noegent\" tal")
		return Entities.product([Entities.number(["-1"]),TextToCAS(instring[1:],recursions+1)])
	else:
		debug(3,recursions*"    "+origin+" er et \"noegent\" tal")
		return Entities.number([instring])
debug.lvl=0
if __name__=="__main__":
	leftside=TextToCAS("")
	rightside=TextToCAS("x*32_birkes")
	focus=TextToCAS("x")
	leftside.printtree()
	print("ASDAS")
	print(leftside.simplify(focus).approx().tostring())
	print(leftside.simplify(focus).approx().printtree())
	#x=TextToCAS("x")
	#print("Eq1",leftside.tostring()+" = "+rightside.tostring())
	#eq1=equations.equation(leftside,rightside)
	#[n.printtree() for n in eq1.solve(x)]
	#print([n.approx().tostring() for n in eq1.solve(x)])
	