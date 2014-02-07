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
	"""
	Sorrounds a latex strings with color if it should be colored
	checkval is the config bool signaling if it should be colored
	"""
	if checkval:
		return "{"+r"\color{"+colorname+"}"+str+"}"
	return str






def picknicestsimplification(inputstr,posformoutput):#picks the nicest both args in expressions, not list
	"""
	Picks the nicest simplification of inputstr (not a str, but an expression) from
	a list of possible forms (expressions too)
	Returns the nicest expression
	"""

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
	"""
	Represents a .Caslog file
	the functions should be self-explanatory
	"""
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

def displaymathcascall(matstr,approx,args):
	"""
	Inputs a string in the "mathmode" of CasPyTeX (ex: |2*3| (matstr would be "2*3)
	and a bool specifying if the answer should be approximated
	It will return an array [bool,str], the bool signaling if there were errors 
	(False if there was errors)
	the str is what it prints to the .tex file
	"""
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
			if "s" not in args:
				return [True,returnstring+r"{\quad\color{red}\textrm{Could not find any solutions!} "]
			return None
		if solutions!=None:
			returnstring+=r"\iff "
		if approx:solutions=[n.approx().simplify() for n in solutions]
		for solution in solutions:
			if config.Use_Coloredoutput:
				returnstring+=r"{\color{"+config.Color_of_output+"} "+solvenum.tolatex(True)+"="+solution.tolatex(True)+"} "+r"\quad "+config.Or_Symbol+r"\quad "
			else:
				returnstring+=solvenum.tolatex(True)+"="+solution.tolatex(True)+r"\quad "+config.Or_Symbol+r"\quad "

		returnstring=returnstring[:-len(config.Or_Symbol+r"\quad ")]
		if "s" not in args:
			return 	[True, returnstring]
		return None


	if ":=" in matstr:
		beforeafterdefinition=matstr.split(r":=")
		if len(beforeafterdefinition)!=2:
			logger.logit("Definition Error: more than one \":=\"")
			print("Definition Error: more than one \":=\"")
			sys.exit()
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
					if "s" not in args:
						return [True,definenumber.tolatex(True)+" "+config.Definition_Symbol+" "+definevalue.tolatex(True)+(r"\;=\;"+maybecolored(simplified.tolatex(True),config.Color_of_output,config.Use_Coloredoutput))*(not "d" in args)]
					else:
						return None
				if "s" not in args:

					return [True,definenumber.tolatex(True)+" "+config.Definition_Symbol+" "+definevalue.tolatex(True)]
				else:
					return None
			else:
				raise ValueError() #just to get to the except
		except:
			logger.logit("Definition Error adding key "+matstr+  " to dict (bad key?)")
			print("FATAL:Definition Error adding key "+matstr+  " to dict (bad key?)")
			sys.exit()
	else:#can only simplify
		origexp=textparser.TextToCAS(matstr)
		nicest=picknicestsimplification(origexp.makepossiblesubstitutions(),origexp.posforms(0,approx))
		if approx:
			nicest=nicest.approx().simplify()
		returnline=origexp.tolatex()+("="+config.Use_Coloredoutput*r"\color{"+config.Use_Coloredoutput*config.Color_of_output+config.Use_Coloredoutput*"}"+nicest.tolatex(True))*(not "d" in args)
		if "s" not in args:
			return [True,returnline]
		else:
			return None
		#returnline=r"\["+origexp.tolatex()
		#simplified=origexp.posforms(0,approx)[0]
		#if simplified!=origexp:
		#	returnline+="="+r"\color{blue}"+simplified.tolatex()+"}"
		#returnline+=r"\]"
		#return [True,returnline]

def interpretnormalline(linestring):
	"""
	Interprets a single line that is not a command or a mathmode call
	outputs the corresponding latex string
	the priority of what it looks at:
		-mathboxes
		-bold text
		-italic text
	"""
	skipuntil=-1
	newlinestring=""
	for index,char in enumerate(linestring):
		if index<=skipuntil:
			continue
		start=False
		if char=="|":
			start=index
			startstopinfo=False
			findtwo=False
			if index+1<len(linestring) and linestring[index+1]=="|":
				#||asdfasdasdf||
				findtwo=True
			for newindex in range(start+findtwo+1,len(linestring)):
				if linestring[newindex]=="|":
					stop=False
					if findtwo:
						if newindex+1==len(linestring) or linestring[index+1]!="|":
							raise ValueError("BAD MATBOX")
						else:
							stop=newindex+1
							startstopinfo=[start,stop,True]
														
					else:
						stop=newindex
						startstopinfo=[start,stop,False]
					break
			if startstopinfo==False:
				raise ValueError("BAD MATBOX",startstopinfo)
			args=[""]
			totalend=stop
			if startstopinfo[1]+1<len(linestring) and linestring[startstopinfo[1]+1]=="?":
				bracketoffset=0
				totalend=False
				for charindex in range(startstopinfo[1]+2,len(linestring)):
					char2=linestring[charindex]
					if char2=="{":
						bracketoffset+=1
					elif char2=="}":
						bracketoffset-=1
					if bracketoffset>0:
						args[-1]+=char2
					else:
						if char2=="?":
							args.append("")
						elif char2==" " or charindex+1==len(linestring):
							if char2!=" ":
								args[-1]+=char2
							totalend=charindex
							break
						else:
							args[-1]+=char2
	
			matstr=linestring[startstopinfo[0]+startstopinfo[2]+1:startstopinfo[1]-startstopinfo[2]]
			mathcodecall=displaymathcascall(matstr,startstopinfo[2],args)
			if mathcodecall==None:
				skipuntil=totalend
				continue
			if mathcodecall[0]==False:
				print("BAD MATHMODE BOX, QUITTING")
				sys.exit()
			else:
				newlinestring+="$"+mathcodecall[1]+"$"
				skipuntil=totalend
				continue
		elif char=="*":
			start=index
			bold=False
			if index+1<len(linestring) and linestring[index+1]=="*":
				bold=True
			bracketoffset=0
			for indexchar in range(start+1+bold,len(linestring)):
				char2=linestring[indexchar]
				if char2=="{":
					bracketoffset+=1
				elif char2=="}":
					bracketoffset-=1
				if bracketoffset>0:
					continue
				else:
					if char2=="*":
						if bold and indexchar+1<len(linestring) and linestring[indexchar+1]=="*":
							stop=indexchar+1
						elif bold:
							print("Bad bold typing,quitting")
							sys.exit()
						else:
							stop=indexchar

						break

			inbetween=linestring[start+bold+1:stop-bold]
			if bold:
				newlinestring+=r"\textbf{"+inbetween+r"}"

			else:
				newlinestring+=r"\textit{"+inbetween+r"}"
			skipuntil=stop
			continue

		else:
			newlinestring+=char
	return newlinestring

def cpttolatex(lines,filename="unnamed.tex"): 
	"""
	Interprets the lines of a .cpt file (lines without any "\n" in it)
	saves a file called filename+".pdf"
	"""
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
	print("Interpreting file:","\""+Truefilename+"\"")
	texfile=LatexFile(Truefilename,path)
	starttime=time.time()
	maketitle=False
	forceappendline=False
	lastlinewasnormal=True
	#remove comments
	lineswithoutcomments=[]
	for line in lines:
		newline=""
		wascommented=False
		for index,char in enumerate(line):
			if char=="/" and (index+1<len(line) and line[index+1]=="/") and not (index-1>=0 and line[index-1]=="\""):
				wascommented=True
				break
			if char=="\\" and (index+2<len(line) and line[index+1]=="/" and line[index+2]=="/"):
				pass#dont add the escape char 
			else:
				newline+=char
		if newline=="" and wascommented:
			continue
		lineswithoutcomments.append(newline)
	#[print(n,"\n") for n in lineswithoutcomments]
	for index,line in enumerate(lineswithoutcomments):
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
			interpretedasnormal=interpretnormalline(line)
			if interpretnormalline=="":continue
			retval=r"\["+interpretedasnormal[1:-1]+r"\]"
			texfile.addline(retval)
			continue
			"""if line[1]==r"|":
				retval=displaymathcascall(line[2:-2],True,[])#approx

			else:
				retval=displaymathcascall(line[1:-1],False,[])#no approx
			if retval[0]==False:
				texfile.addline(r"\begin{verbatim}"+retval[1]+r"\end{verbatim}")
			elif retval[0]==True:
				texfile.addline(r"\["+retval[1]+r"\]")"""
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
			elif variable in ["Significant_Figures"]:
				try:
					decplaces=int(value)
					config.Significant_Figures=decplaces
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
			texfile.addline(r"\\"*lastlinewasnormal+interpretnormalline(line))
			lastlinewasnormal=True
			"""newline="" #where 
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
			lastlinewasnormal=True"""
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
#if False:
	"""
	Inputs the .cpt file into the cpttolatex() and it will compile and save the
	resulting .pdf
	"""
	debug.lvl=3
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
