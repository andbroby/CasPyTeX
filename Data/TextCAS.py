from subprocess import call
from latexfileclass import LatexFile
from sys import argv
import sys
from os import getcwd
import textparser
import Entityclass as Entities
import time
import CasPyTexConfig as config
import equationsolver as equations
import stringmanipulations
from debugger import *
def maybecolored(str,colorname,checkval):
	if checkval:
		return "{"+r"\color{"+colorname+"}"+str+"}"
	return str
def picknicestsimplification(inputstr,posformoutput,substituted=None):#picks the nicest both args in expressions, not list
	#sort away the inputstr
	newposformoutput=[n for n in posformoutput if n!=inputstr]
	#sort by treedepth
	if newposformoutput==[]:
		return inputstr
	nicest=newposformoutput[0]
	nicestgetreturn=newposformoutput[0].getsimplifyscore()
	for n in newposformoutput:
		values=n.getsimplifyscore()
		if values[0]<nicestgetreturn[0]:
			nicest=n
			nicestgetreturn=values
			continue
		elif values[0]==nicestgetreturn[0]:
			if values[1]<nicestgetreturn[1]:
				nicest=n
				nicestgetreturn=values
				continue
			elif values[1]==nicestgetreturn[1]:
				if len(n.tostring())>len(nicest.tostring()):
					nicest=n
					nicestgetreturn=values

	return nicest
class logfile:
	def __init__(self,filename):
		self.lines=["Filename:  "+str(filename)+"\n"]
		self.filename=filename+".CASlog"
	def appendline(self,rawstr):
		self.lines.append(rawstr+"\n")
	def writetofile(self):
		f=open(self.filename,"w")
		[f.write(line) for line in self.lines]
	def logit(self,rawstr):
		self.appendline(rawstr)
		self.writetofile()

def displaymathcascall(matstr,approx):#return [bool,latexstr] with bool being to show it or not
	if matstr[:6] in ["solve(","Solve("]:
		#find endsolve bracket )
		bracketoffset=0
		checknow=False
		bracketend=False
		for index,char in enumerate(matstr):
			if char=="(":
				bracketoffset+=1
				checknow=True
			elif char==")":
				bracketoffset-=1
			if checknow and bracketoffset==0:
				bracketend=index
				break
		if bracketend==False:
			return [False,"bad solve syntax"]
		insidesolvefunction=matstr[6:bracketend]
		dropit=False
		equationandsolvenum=False
		for index in range(len(insidesolvefunction)-1,-1,-1):
			if dropit:
				if insidesolvefunction[index]=="{":
					dropit=False
				continue
			if insidesolvefunction[index]=="}":
				dropit=True
				continue
			if insidesolvefunction[index]==",":
				equationandsolvenum=stringmanipulations.splitstringbyindexes(insidesolvefunction,[index])
		if equationandsolvenum==False:
			return [False, "bad solve syntax"]
		#remove unnecessary spaces
		newequationsandsolvenum=[]
		for n in equationandsolvenum:
			newn=""
			dropit=False
			for char in n:
				if dropit:
					if char=="}":
						dropit=False
				if not dropit and char=="{":
					dropit=True
				if not dropit and char==" ":
					continue
				newn+=char
			newequationsandsolvenum.append(newn)
		equationstring=newequationsandsolvenum[0]
		solvenumstring=newequationsandsolvenum[1]
		leftandrightside=equationstring.split("=")
		if len(leftandrightside)!=2:
			return [False,"Too many \"=\" in solve function!"]
		leftside=textparser.TextToCAS(leftandrightside[0])
		rightside=textparser.TextToCAS(leftandrightside[1])
		solvenum=textparser.TextToCAS(solvenumstring)
		equationclass=equations.equation(leftside,rightside)
		solutions=equationclass.solve(solvenum)
		returnstring=equationclass.tolatex()
		if solutions==None:
			return [True,returnstring+r"{\quad\color{red}\textrm{Could not find any solutions!} "]
		if solutions!=None:
			returnstring+=r"\iff "
		if approx:solutions=[n.approx().simplify() for n in solutions]
		for solution in solutions:
			if config.Use_Coloredoutput:
				returnstring+=r"{\color{"+config.Color_of_output+"} "+solvenum.tolatex(True)+"="+solution.tolatex(True)+"} "+r"\quad "+config.Or_Symbol+r"\quad "
			else:
				returnstring+=solvenum.tolatex(True)+"="+solution.tolatex(True)+r"\quad "+config.Or_Symbol+r"\quad "

		returnstring=returnstring[:-len(config.Or_Symbol+r"\quad ")]
		return 	[True, r"\["+returnstring+"\]"]


	if ":=" in matstr:
		beforeafterdefinition=matstr.split(r":=")
		if len(beforeafterdefinition)!=2:
			logger.logit("Definition Error: more than one \":=\"")
			return [True,"Definition Error: more than one \":=\""]
		definenumstr=beforeafterdefinition[0]
		definevalstr=beforeafterdefinition[1]
		try:
			definenumber=textparser.TextToCAS(definenumstr)
			definevalue=textparser.TextToCAS(definevalstr)
			if definenumber.type()=="unknownfunction":
				definitionsucces=Entities.subdict.addfunc(definenumber.funcstr,definenumber.args,definevalue)
			else:
				definitionsucces=Entities.subdict.adddefinition(definenumber,definevalue)
			if definitionsucces:
				simplified=picknicestsimplification(definevalue,definevalue.posforms(0,approx))
				if simplified!=definevalue:
					return [True,r"\["+definenumber.tolatex(True)+" "+config.Definition_Symbol+" "+definevalue.tolatex(True)+r"\;=\;"+maybecolored(simplified.tolatex(True),config.Color_of_output,config.Use_Coloredoutput)+r"\]"]

				return [True,r"\["+definenumber.tolatex(True)+" "+config.Definition_Symbol+" "+definevalue.tolatex(True)+r"\]"]
			else:
				raise ValueError() #just to get to the except
		except:
			logger.logit("Definition Error adding key "+matstr+  " to dict (bad key?)")
			return [False,"Definition Error adding key "+matstr+  " to dict (bad key?)"]
	else:#can only simplify
		origexp=textparser.TextToCAS(matstr)
		nicest=picknicestsimplification(origexp.makepossiblesubstitutions(),origexp.posforms(0,approx))
		if approx:
			nicest=nicest.approx().simplify()
		returnline=r"\["+origexp.tolatex()+"="+config.Use_Coloredoutput*r"\color{"+config.Use_Coloredoutput*config.Color_of_output+config.Use_Coloredoutput*"}"+nicest.tolatex(True)+r"\]"
		return [True,returnline]
		#returnline=r"\["+origexp.tolatex()
		#simplified=origexp.posforms(0,approx)[0]
		#if simplified!=origexp:
		#	returnline+="="+r"\color{blue}"+simplified.tolatex()+"}"
		#returnline+=r"\]"
		#return [True,returnline]



def cpttolatex(lines,filename="unnamed.tex"): #lines skal være uden grimme "\n" bag på
	path=getcwd()
	Truefilename=filename
	if sys.platform!="win32" and "/" in filename:
		Truefilename=filename.split("/")[-1]
		path="".join([n+"/" for n in filename.split("/")[:-1]][:])
	elif sys.platform=="win32" and "\\" in filename:
		Truefilename=filename.split("\\")[-1]
		path="".join([n+"\\" for n in filename.split("\\")[:-1]][:])
		if path[-1]=="\\":
			path=path[:-1]
	print("FILPATH",Truefilename,path)
	texfile=LatexFile(Truefilename,path)
	starttime=time.time()
	maketitle=False
	forceappendline=False
	lastlinewasnormal=True
	for index,line in enumerate(lines):
		if forceappendline:
			if "endlatex" in line and line[:2]=="#?":
				forceappendline=False
			else:
				texfile.addline(line)
			continue
		#check for ===== or -----
		if line=="" or sum([not char==" " for char in line])==0:
			texfile.addline(r"\\")
			lastlinewasnormal=True
			continue
		if True:
			is_section=True
			is_subsection=True
			for char in line:
				if char==" ":
					pass
				elif char=="=":
					is_subsection=False
				elif char=="-":
					is_section=False
				else:
					is_section=is_subsection=False
					break
			if is_section and is_subsection:
				pass
			elif is_section:
				texfile.linepop()
				texfile.addline(r"\section*{"+lines[index-1]+r"}")
				lastlinewasnormal=False
				continue
			elif is_subsection:
				texfile.linepop()
				texfile.addline(r"\subsection*{"+lines[index-1]+r"}")
				lastlinewasnormal=False
				continue
		if line[0]==r"|":#Cas-calls
			if line[1]==r"|":
				retval=displaymathcascall(line[2:-2],True)#approx

			else:
				retval=displaymathcascall(line[1:-1],False)#no approx
			if retval[0]==False:
				texfile.addline(r"\begin{verbatim}"+retval[1]+r"\end{verbatim}")
			elif retval[0]==True:
				texfile.addline(retval[1])
			continue

		if line[:2]=="#?": #preambles
			#check if #?startlatex
			if "startlatex" in line:
				forceappendline=True
				continue
			#We cut away #? and spaces
			cuttedline=""
			aftertheequalsign=False #no spaces removed after text has begun
			for n in line[2:]:
				if n!=" " or aftertheequalsign:
					if n!=" ":
						aftertheequalsign=True

					cuttedline+=n
			while cuttedline[-1]==" ":
				cuttedline=cuttedline[:-1]
			#we split it into the variable and the value
			varandval=cuttedline.split("=")

			if len(varandval)!=2:
				if len(varandval)==1:
					command=varandval[0]
					if command=="forgetall":
						Entities.subdict.wipedict()
					elif len(command)>6 and command[:6]=="forget":
						forgetvar=command[6:]
						while forgetvar[0]==" ":
							forgetvar=forgetvar[1:]
						while forgetvar[-1]==" ":
							forgetvar=forgetvar[:-1]
						try:
							Entities.subdict.forgetdefinition(Entities.number([forgetvar]))
						except:
							pass
				logger.logit("skipped line"+str(index+1)+"because of bad #? statement")
				continue
			variable=varandval[0]
			value=varandval[1]
			if variable in ["Title","title"]:
				if not maketitle:
					texfile.addline(r"\maketitle\noindent")
					maketitle=True
				texfile.addtopreamble(r"\title{"+value+r"}")
			elif variable in ["Author","author"]:
				
				texfile.addtopreamble(r"\author{"+value+r"}")
			elif variable in ["Date","date"]:
				
				texfile.addtopreamble(r"\date{"+value+r"}")
			elif variable in ["Use_Radians"]:
				if value in ["True","true"]:
					config.Use_Radians=True
				elif value in ["False","false"]:
					config.Use_Radians=False
			elif variable in ["Decimal_Places"]:
				try:
					decplaces=int(variable)
					config.Decimal_Places=decplaces
				except:
					pass
			elif variable in ["Use_Coloredoutput"]:
				if value in ["True","true"]:
					config.Use_Coloredoutput=True
				elif value in ["False","false"]:
					config.Use_Coloredoutput=False
			elif variable in ["Color_of_output"]:
				if value in config.Colors:
					config.Color_of_output=value
#Use_Coloredoutput=True
#Color_of_output="red"


			lastlinewasnormal=False
		elif line[0]=="#":
			if line[1]=="#":
				texfile.addline(r"\section*{"+line[2:]+r"}")
			else:
				texfile.addline(r"\subsection*{"+line[1:]+r"}")
			lastlinewasnormal=False
		else:#normal text, need to change *asdfasdf* to cursive and **asdfasdf** to bold
			newline="" #where 
			if lastlinewasnormal:
				newline+=r"\\"
			skipnext=False
			insertendshereitalic=[]
			insertendsherebold=[]
			for index,char in enumerate(line):
				if index in insertendshereitalic:
					newline+="}"
					continue
				if index in insertendsherebold:
					newline+="}"
					skipnext=True
					continue
				if skipnext:
					skipnext=False
					continue
				if char=="*":
#					print("LINE",line)
					if line[index+1]=="*":
						skipnext=True
						newline+=r"\textbf{"
						for indexk in range(index+2,len(line)):
							if line[indexk]=="*":
								insertendsherebold.append(indexk)
								break
					else:
						newline+=r"\textit{"
						for indexk in range(index+1,len(line)):
							if line[indexk]=="*":
								insertendshereitalic.append(indexk)
								break
				else:
					newline+=char
			texfile.addline(newline)
			lastlinewasnormal=True
	print("CAS calls and typesetting took "+str(time.time()-starttime)+" seconds")
	logger.logit("CAS calls and typesetting took "+str(time.time()-starttime)+" seconds")
	compileresult=texfile.compiletolatex()
	if compileresult==True:
		print("Succesfully compiled to .pdf!")
		logger.logit("Succesfully compiled to .pdf!")
	else:
		print("compilation Error")
		logger.logit("Compilation error")
	print("Total running time: "+str(time.time()-starttime)+" seconds")
	logger.logit("Total running time: "+str(time.time()-starttime)+" seconds")
#filename="test.cpt"
#f=open("TextCAS/"+filename)
#cpttolatex([n.replace("\n","") for n in f.readlines()],"test.cpt")
if __name__=="__main__":
	debug.lvl=0
	if len(argv)!=2:
		print("Bad arg, exiting")
	filename=argv[1]
	if filename[-4:]!=".cpt":
		print("This is not a .cpt file, exiting")
		sys.exit()
	logger=logfile(filename)
	#sys.exit()
	try:
		cptfile=open(getcwd()+"/"+filename)
		isfullpath=False
	except:
		try:
			cptfile=open(filename)
			isfullpath=True
		except:
			print("No such file exists, exiting")
			sys.exit()
	lines=[n.replace("\n","") for n in cptfile.readlines()]
	cpttolatex(lines,filename)





"""
preamble
\documentclass{article}
"""