"""
TextToCAS tager matematik og konverterer det til CAS'en


(a+b)-2*a^3

"""
#from __future__ import division
#from __future__ import print_function
from sys import exit
import Entityclass as Entities
from stringmanipulations import *
from debugger import *
def TextToCAS(instring,recursions=0):
	origin=instring
	instring=instring.replace("-","+-").replace("++","+").replace("--","+").replace("(+-","(-")
	#if instring[0]=="+":instring=instring[1:]
	if instring[0]=="+":
		instring=instring[1:]
	if instring[0]=="-":
		return Entities.product([Entities.number(["-1"]),TextToCAS(instring[1:])])
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
	if "+" in instring or "*" in instring or "/" in instring or "(" in instring or ")" in instring:
		#print("OIOI",instring,ydersteparentes(stringtoparentespar(instring))[0])
		if instring[0]=="-" and ydersteparentes(stringtoparentespar(instring))[0]==1 and ydersteparentes(stringtoparentespar(instring))[1]==len(instring)-1:
			return Entities.product([Entities.number(["-1"]),TextToCAS(instring[1:])])
		debug(1,"FEJL: TextToCAS vil lave number instance med regnetegn i udtrykket\nStopper programmet")
		exit()
	#til sidst laves number instance
	if origin[0]=="-":
		debug(3,recursions*"    "+origin+" bliver til PRODUKT ['-1',"+origin[1:]+"]")
		debug(3,(recursions+1)*"    "+"-1"+" er et \"noegent\" tal")
		return Entities.product([Entities.number(["-1"]),TextToCAS(origin[1:],recursions+1)])
	else:
		debug(3,recursions*"    "+origin+" er et \"noegent\" tal")
		return Entities.number([instring])
debug.lvl=0
if __name__=="__main__":
	a=TextToCAS("2*(3*x+3)")
	#print(a.tostring())
	b=a.tostring()

	a=a.expand()
	print("DONE WITH SIMPLIFY")
	print("INPUT:"+b+"\n"+"RESULT:"+a.tostring())#+"\nApprox: " +a.approx().tostring())
