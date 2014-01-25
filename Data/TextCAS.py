from subprocess import call
from latexfileclass import LatexFile
from sys import argv
import sys
from os import getcwd
import textparser
import Entityclass as Entities
import time
#Read from config, change any relevant values
"""
try:
	
	configfile=open("config.cfg")
except:
	try:
		configfile=open("Data/config.cfg")
	except:
		raise ValueError("NO CONFIG FOUND, BREAKING")
for line in [n.replace("\n","") for n in configfile.readlines()]:	
	if line[0]=="#":continue
	try:
		var=line.split("=")[0]
		val=line.split("=")[1]
		if var=="Use_Radians":
			if val=="True":
				Use_Radians=True
			elif val=="False":
				Use_Radians=False
		if var=="Decimal_Places":
			dec_places=int(val)
	except:
		continue
"""
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
			definitionsucces=Entities.subdict.adddefinition(definenumber,definevalue)
			if definitionsucces:
				return [True,r"\["+definenumber.tolatex()+":="+definevalue.tolatex()+r"\]"]
			else:
				raise ValueError() #just to get to the except
		except:
			logger.logit("Definition Error adding key "+matstr+  " to dict (bad key?)")
			return [False,"Definition Error adding key "+matstr+  " to dict (bad key?)"]
	else:#can only simplify
		print("interpreted matstr",matstr)

		origexp=textparser.TextToCAS(matstr)
		returnline=r"\["+origexp.tolatex()
		simplified=origexp.posforms(0,approx)[0]
		if simplified!=origexp:
			returnline+="="+r"\color{blue}"+simplified.tolatex()+"}"
		returnline+=r"\]"
		return [True,returnline]
		pass



def cpttolatex(lines,filename="unnamed.tex"): #lines skal være uden grimme "\n" bag på
	texfile=LatexFile(filename,getcwd())
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
			aftertheequalsign=False #no spaces removed after "="
			for n in line[2:]:
				if n!=" " or aftertheequalsign:
					if n=="=":
						aftertheequalsign=True

					cuttedline+=n
			#we split it into the variable and the value
			varandval=cuttedline.split("=")
			if len(varandval)!=2:
				logger.logit("skipped line"+str(index+1)+"because of bad #? statement")
				continue
			variable=varandval[0]
			value=varandval[1]
			if variable in ["Title","title"]:
				if not maketitle:
					texfile.addline(r"\maketitle")
					maketitle=True
				texfile.addtopreamble(r"\title{"+value+r"}")
			elif variable in ["Author","author"]:
				texfile.addtopreamble(r"\author{"+value+r"}")
			elif variable in ["Date","date"]:
				texfile.addtopreamble(r"\date{"+value+r"}")
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
	texfile.compiletolatex()

#filename="test.cpt"
#f=open("TextCAS/"+filename)
#cpttolatex([n.replace("\n","") for n in f.readlines()],"test.cpt")
if __name__=="__main__":
	if len(argv)!=2:
		print("Bad arg, exiting")
	filename=argv[1]
	logger=logfile(filename)
	try:
		print(getcwd()+"/"+filename)
		cptfile=open(getcwd()+"/"+filename)
	except:
		print("No such file exists, exiting")
		sys.exit()
	lines=[n.replace("\n","") for n in cptfile.readlines()]
	cpttolatex(lines,filename)





"""
preamble
\documentclass{article}
"""