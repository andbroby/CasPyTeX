from stringmanipulations import *
from debugger import *
import sys
from fractions import gcd
from copy import deepcopy
import math
import CasPyTexConfig as config
Use_Radians=config.Use_Radians
dec_places=config.Decimal_Places
const_pi=math.pi
const_e =math.e

class definitiondict:
	def __init__(self):
		self.funcdict=dict()	
		self.subdict=dict()
	def adddefinition(self,definenumber,defineval):
		if type(definenumber)!=type(number(["2"])): #Checking for bad definitions
			print("Bad definition (definenumber), quitting from definition")
			return False
		try:
			
			defineval.type()
		except:
			print("Bad definition, quitting from definition")
			return False
		self.subdict[definenumber.num]=defineval
		return True
	def wipedict(self):
		self.subdict=dict()
		return True
	def forgetdefinition(self,definenumber):
		try:
			numstr=definenumber.num
			self.subdict.pop(numstr, None)
			return True
		except:
			return False
	def findsubstitute(self,definenumber):
		try:
			numkey=definenumber.num
		except:
			print("bad definenumber")
			return False
		try:
			return self.subdict[numkey]
		except:
			return False
	def addfunc(self,forskriftstr,inputnum,defineexp):
		if type(inputnum)!=type(number(["2"])):
			print("Bad func definition",inputnum.tostring())
			return False
		try:
			defineexp.type()
		except:
			print("Bad func defineexp")
			return False
		self.funcdict[forskriftstr]=[inputnum,defineexp]
		return True
	def forgetfuncdef(self,forskriftstr):
		try:
			self.funcdict(forskriftstr,None)
			return True
		except:
			return False
	def wipefuncdict(self):
		self.funcdict=dict()
		return True
	def findfuncsub(self,forskriftstr,inputexp):
		try:
			defineexpwithoutsub=self.funcdict[forskriftstr]
		except:
			return False
		definexpsubbed=defineexpwithoutsub[1].substitute(defineexpwithoutsub[0],inputexp)
		return definexpsubbed



cancallisunit=["number","potens","division","product"]
class product:
	def __init__(self,arr): 
		self.arr=arr
		self.factors=arr
		self.isunit=True
		for factor in self.factors:
			if not (factor.type() in cancallisunit and factor.isunit):
				self.isunit=False
				break
	def type(self):
		
		return "product"
	def tostring(self,substitute=False):###
		returnstring=""
		minuscounter=0
		newfactors=[]
		for n in self.factors:
			if n.type()=="number" and n.num=="-1":
				minuscounter+=1
			else:
				newfactors.append(n)
		if newfactors==[]:
			return "-"*(minuscounter%2)+"1"
		returnstring="-"*(minuscounter%2)
		for n in newfactors:
			if n.type()=="addition":
				returnstring+="("+n.tostring()+")*"
			elif n.type()=="number" and n.isunit and (len(returnstring)==0 or returnstring[-1]=="*"):
				returnstring=returnstring[:-1]+n.tostring()+"*"
			else:
				returnstring+=n.tostring()+"*"
		if returnstring[-1]=="*":returnstring=returnstring[:-1]
		return returnstring
	def tolatex(self,roundit=False):
		returnstring=""
		minuscounter=0
		newfactors=[]
		for n in self.factors:
			if n.type()=="number" and n.num=="-1":
				minuscounter+=1
			else:
				newfactors.append(n)
		returnstring="-"*(minuscounter%2)
		for index,n in enumerate(newfactors):
			if n.type()=="addition":
				returnstring+=r"\left("+n.tolatex(roundit)+r"\right)\cdot "
			elif n.type() in cancallisunit and n.isunit and len(returnstring)>=6 and returnstring[-6:]==r"\cdot " and not (index>0 and newfactors[index-1].type() in cancallisunit and newfactors[index-1].isunit):
				returnstring=returnstring[:-6]+r"\;"+n.tolatex(roundit)+r"\cdot "
			elif n.type() in cancallisunit  and n.isunit:
				returnstring+=r"\;"*(index>0 and not(newfactors[index-1].type() in cancallisunit[index-1]))+n.tolatex(roundit)+r"\cdot "
			else:
				returnstring+=n.tolatex(roundit)+r"\cdot "
		if returnstring[-6:]==r"\cdot ":returnstring=returnstring[:-6]
		return returnstring
	def simplify(self,focus=None,thrd=0):###

		return SimplifyAll(self,focus,thrd)
	def delfactor(self,index):
		copy=self.factors[:]
		copy.pop(index)
		if copy==[]:
			return number(["1"])
		if len(copy)==1:return copy[0]

		return product(copy)
	def maxleveloftree(self,level=0):
		
		return max([n.maxleveloftree(level+1) for n in self.factors])
	def evaluable(self,approx=False):
		for k in self.factors:
			if not k.evaluable(approx):
				return False
		return True
	def evalsimplify(self,approx=False):
		newfactors=[n.evalsimplify(approx) for n in self.factors]
		#small associative property
		newnewfactors=[]
		for factor in newfactors:
			if factor.type()=="product":
				newnewfactors+=factor.factors
			else:
				newnewfactors.append(factor)

		nonevaluableparts=[]
		evalparts=[]
		for n in newnewfactors:
			if n.evaluable(approx):
				evalparts.append(n)
			else:
				nonevaluableparts.append(n)
		evalfactor=1
		for n in evalparts:
			evalfactor*=eval(n.tostring().replace("^","**"))
		if evalfactor%1==0:
			evalfactor=int(evalfactor)
		if nonevaluableparts==[]:
			return newevaluednum(evalfactor)
		if evalfactor==1:
			return maybeclass(nonevaluableparts,product)
		else:
			return maybeclass([newevaluednum(evalfactor)]+nonevaluableparts,product)
	
	def evalpart(self,approx=False):
		return self.evalsimplify(approx)
		#newarr=[]
		#proddy=1
		#for n in self.factors:
		#	if n.evaluable(approx):
		#		proddy*=float(n.tostring())
		#	else:
		#		newarr.append(n)
		#if proddy%1==0:proddy=int(proddy)
		#if proddy==1:
		#	retval=newarr
		#else: 
		#	retval=[newnumber([str(proddy)])]+newarr
		#newretval=[]
		#for n in retval:
		#	if n.type()=="product":
		#		newretval+=n.factors
		#	else:
		#		newretval.append(n)
		#retval=maybeclass(newretval,product)
		#if retval.type=="product" and retval.moveconstantsinfront()!=False:
		#	retval=retval.moveconstantsinfront()
		#return maybeclass(newretval,product)
	def moveconstantsinfront(self,focus=None):
		toputback=[]
		toputinfront=[]
		factorwindex=[[self.factors[k],k] for k in range(len(self.factors))]
		for factor in factorwindex:
			if factor[0].evaluable(True):
				toputinfront.append(factor)
			else:
				toputback.append(factor)
		newfactors=toputinfront+toputback
		if [n[1] for n in newfactors]!=[n[1] for n in factorwindex]:
			return product([n[0] for n in newfactors])
		return False
	def simplifyallparts(self,focus):
		newparts=[]
		for n in self.factors:
			newparts.append(n.simplify(focus))
		if len(newparts)==1:return newparts[0]
		return product(newparts)
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()		
		for n in self.factors:
			if n.contains(varstring):
				return True
		return False
	def approx(self):
		
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:
			return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		useditems=[]
		for n in info1[1]:
			foundmatch=False
			for index,k in enumerate(info2[1]):
				if n.__eq__(k,False) and index not in useditems:
					useditems.append(index)
					foundmatch=True
					break
			if foundmatch==False:
				return False
		return True
	def compareinfo(self):
		return [self.type(),self.factors]
	def findvariables(self):
		variables=[]
		for n in self.factors:
			for k in n.findvariables():
				if k not in variables:
					variables.append(k)
		return variables
	def ntimes0(self,focus):
		zeroed=False
		for n in self.factors:
			if n==number(["0"]):
				zeroed=True
		if zeroed:
			return number(["0"])
		return False
	def associativeprop(self,focus=None):
		newfactors=[]
		retfalse=True
		for n in self.factors:
			if n.type()=="product" and not (len(n.factors)==2 and n.factors[0]==number(["-1"]) and n.factors[0].type()!="product"):
				retfalse=False
				newfactors+=n.factors
			else:
				newfactors.append(n)
		if retfalse:
			return False
		return maybeclass(newfactors,product)
	def sameroot(self,focus,nonintrusive=False):
		worked=False
		breakall=False
		for in1,fac1 in enumerate(self.factors):
			for in2,fac2 in enumerate(self.factors):
				if in1==in2:continue
				if fac1.type()=="potens":
					if fac2.type()=="potens":
						if fac1.root==fac2.root:
							if nonintrusive:
								if fac1.exponent.evaluable(True) and fac2.exponent.evaluable(True):
									#copypaste
									newexp=maybeclass([fac1.exponent,fac2.exponent],addition)
									newroot=fac1.root
									newfact=potens([newroot,newexp])
									skipids=[id(fac1),id(fac2)]
									worked=True
									breakall=True
									break								
							elif focus==None or fac1.root.contains(focus.tostring()) or  (fac1.exponent.contains(focus.tostring())==False and fac2.exponent.contains(focus.tostring())==False):
								newexp=maybeclass([fac1.exponent,fac2.exponent],addition)
								newroot=fac1.root
								newfact=potens([newroot,newexp])
								skipids=[id(fac1),id(fac2)]
								worked=True
								breakall=True
								break
					elif fac2.type()!="potens":
						if fac1.root==fac2:
							if nonintrusive:
								if fac1.exponent.evaluable(True):
									newexp=maybeclass([fac1.exponent,number(["1"])],addition)
									newroot=fac1.root
									newfact=potens([newroot,newexp])
									skipids=[id(fac1),id(fac2)]
									worked=True
									breakall=True
									break									
							if focus==None or fac2.contains(focus.tostring()) or fac1.exponent.contains(focus.tostring())==False:
								newexp=maybeclass([fac1.exponent,number(["1"])],addition)
								newroot=fac1.root
								newfact=potens([newroot,newexp])
								skipids=[id(fac1),id(fac2)]
								worked=True
								breakall=True
								break
				if fac1.type()!="potens":
					if fac2.type()=="potens":
						if fac2.root==fac1:
							if nonintrusive:
								if fac2.exponent.evaluable(True):
									newexp=maybeclass([fac2.exponent,number(["1"])],addition)
									newroot=fac2.root
									newfact=potens([newroot,newexp])
									skipids=[id(fac1),id(fac2)]
									worked=True
									breakall=True
									break
							if focus==None or fac1.contains(focus.tostring()) or fac2.exponent.contains(focus.tostring())==False:
								newexp=maybeclass([fac2.exponent,number(["1"])],addition)
								newroot=fac2.root
								newfact=potens([newroot,newexp])
								skipids=[id(fac1),id(fac2)]
								worked=True
								breakall=True
								break
					if fac2.type()!="potens":
						if fac1==fac2:
							newfact=potens([fac1,number(["2"])])	
							skipids=[id(fac1),id(fac2)]
							worked=True
							breakall=True
							break		
			if breakall==True:
				break
		if worked==True:
			newfactors=[newfact]
			for n in self.factors:
				if id(n) not in skipids:
					newfactors.append(n)
			return maybeclass(newfactors,product)
		return False
	def sameexponent(self,focus):#b^a*c^a=(b*c)^a
		worked=False
		breakall=False
		for in1,fac1 in enumerate(self.factors):
			for in2,fac2 in enumerate(self.factors):
				if in1==in2:continue
				if fac1.type()=="potens" and fac2.type()=="potens":
					if fac1.exponent==fac2.exponent:
						if (focus!=None and fac1.exponent.contains(focus.tostring())) or self.evaluable(True):
							return potens([product([fac1.root,fac2.root]),fac1.exponent])
		return False
	def distributive(self,focus):
		for factor in self.factors:
			if factor.type()=="addition":
				if focus=="force" or (focus!=None and factor.contains(focus.tostring())):
					factorsthatarenotfactor=[n for n in self.factors if id(n)!=id(factor)]
					newsum=[]
					for addend in factor.addends:
						newsum.append(product(factorsthatarenotfactor+[addend]))
					return addition(newsum)

		return False
	def expand(self):
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"PRODUCT: "+self.tostring())
		for n in self.factors:
			n.printtree(rec+1)
	def fractionasfactor(self,focus=None): #ganger hele tal op til nævner, eller brøker med brøker
		for in1,factor1 in enumerate(self.factors):
			for in2,factor2 in enumerate(self.factors):
				if in1==in2:continue
				rununialg=False
				if factor1.type()=="division" and factor2.type()=="division":
					newnumerator=product([factor1.numerator,factor2.numerator])
					newdenom=product([factor1.denominator,factor2.denominator])
					unified=division([newnumerator,newdenom])
					newfactors=[n for n in self.factors if id(n) not in [id(factor1),id(factor2)]]+[unified]
					return maybeclass(newfactors,product)
				elif factor1.type()=="division":
					rununialg=True
					frac=factor1
					side=factor2
				elif factor2.type()=="division":
					rununialg=False
					frac=factor2
					side=factor1
				if rununialg:
					newnumerator=product([side,frac.numerator])
					newdenom=frac.denominator
					unified=treesimplify(division([newnumerator,newdenom]))
					newfactors=[n for n in self.factors if id(n) not in [id(factor1),id(factor2)]]+[unified]
					retval=treesimplify(maybeclass(newfactors,product))
					if side in cancallisunit and side.isunit and frac in cancallisunit and frac.isunit:
						return retval
					if unified.evaluable(True) or frac.numerator.type()=="product" and frac.numerator.factors[0].evaluable(True):
						return retval
					if unified.samerootofexponent()!=False or unified.antisameexponentfrac()!=False or unified.samerootofexponentfactors()!=False or unified.shortfract()!=False or unified.cancelfactors()!=False:
						return maybeclass(newfactors,product)					#if side.evaluable():

					#	newnumerator=product([side,frac.numerator])
					#	newdenom=frac.denominator
					#	unified=division([newnumerator,newdenom])
					#	newfactors=[n for n in self.factors if id(n) not in [id(factor1),id(factor2)]]+[unified]
					#	return maybeclass(newfactors,product)
		return False
	def makepossiblesubstitutions(self):
		newfactors=[]
		for n in self.factors:
			newfactors.append(n.makepossiblesubstitutions())
		if maybeclass(newfactors,product)!=self:
			return maybeclass(newfactors,product).makepossiblesubstitutions()
		else:
			return self
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")		
		newfactors=[]
		for n in self.factors:
			newfactors.append(n.substitute(subthisexp,tothisexp))
		if maybeclass(newfactors,product)!=self:
			return maybeclass(newfactors,product).substitute(subthisexp,tothisexp)
		else:
			return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),len(self.factors)]
class number:
	def __init__(self,arr,isfunction=False):
		self.arr=arr
		if len(arr)!=1:
			raise ValueError("WRONG NUMBER")
		self.num=arr[0]
		self.isunit=False
		self.isfunction=isfunction
		if self.num[0]=="_":
			self.isunit=True
	def type(self):
		
		return "number"
	def tostring(self,substitute=False):
		if self.num=="_pi":
			return "pi"
		elif self.num=="_e":
			return "e"
		return self.num
	def tolatex(self,roundit=False):
		if self.num=="_pi":
			return r"\pi"
		elif self.num=="_e":
			return "e"
		elif self.num[0]=="_":
			return r"\textrm{"+self.num[1:]+"}"
		if roundit==True and self.evaluable():
			rounded=sigfigroundfromstr(self.num,config.Significant_Figures)
			return rounded
		return self.num
	def simplify(self,focus=None,thrd=0):###
		"""if self.evaluable():
			if float(self.num)%1==0:
				return number([str(int(float(self.num)))])"""
		return self.makepossiblesubstitutions()
	def maxleveloftree(self,level=0):
		
		return level+1
	def evaluable(self,approx=False):
		if self.num in ["_pi","_e"] and approx:
			return True
		for n in self.num:
			if n not in ["0","1","2","3","4","5","6","7","8","9",".","-"]:
				return False
		return True
	def evalsimplify(self,approx=False):
		if approx and self.num in ["_pi","_e"]:
			if self.num=="_pi":
				return newevaluednum(math.pi)
			elif self.num=="_e":
				return newevaluednum(math.e)
		if self.evaluable(approx):
			if float(self.num)%1==0:

				return number([str(int(float(self.num)))])
		return self
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if varstring==self.num:return True
		return False
	def simplifyallparts(self,approx=False):		
		return self
	def compareinfo(self):

		return [self.type(),self.num]
	def approx(self):
		
		return self.evalsimplify(True)
	def __eq__(self,other,recursionNOTUSED=False):
		if type(other)==type(str()):return False
		if other in [None,False,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if self.type()!=other.type():
			return False
		return self.num==other.num
	def findvariables(self):
		if not self.evaluable(True):
			return [self.num]
		return []
	def expand(self):
		
		return self
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		
		print("   "*rec+self.num)
	def makepossiblesubstitutions(self):
		testifsubavailable=subdict.findsubstitute(self)
		if testifsubavailable!=False:
			return testifsubavailable.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [1,1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		if subthisexp.num==self.num:
			return tothisexp
		return self
class potens:
	def __init__(self,arr):
		self.arr=arr
		self.rootandexponents=arr
		if len(arr)!=2:
			print_stack
			print([n.tostring() for n in arr])
			debug(1,"FORKERT POTENS, STOPPER PROGRAMMET")
			exit()
		self.root=arr[0]
		self.exponent=arr[1]
		self.isunit=False
		if self.root.type()=="number" and self.root.isunit:
			self.isunit=True
	def type(self):
		
		return "potens"
	def tostring(self,substitute=False):
		returnstring=""
		for n in self.rootandexponents:
			if n.type()!="number":
				returnstring+="("+n.tostring()+")^"
			else:
				returnstring+=n.tostring()+"^"
		if returnstring[-1]=="^":
			returnstring=returnstring[:-1]
		return returnstring
	def tolatex(self,roundit=False):
		returnstring=""
		if self.root.type()!="number":
			returnstring+=r"\left("+self.root.tolatex(roundit)+r"\right)^"
		else:
			returnstring+=self.root.tolatex(roundit)+"^"
		returnstring+="{"+self.exponent.tolatex(roundit)+"}"
		if returnstring[-1]=="^":
			returnstring=returnstring[:-1]
		return returnstring
	def simplify(self,focus=None,thrd=0):#
		
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		
		return max([n.maxleveloftree(level+1) for n in self.rootandexponents])
	def evaluable(self,approx=False):
		if self.root.evaluable(approx) and self.exponent.evaluable(approx):
			return True
		else:
			if self.root.evaluable(True) and self.exponent.evaluable(True):
				if float(self.root.evalsimplify(True).num)**float(self.exponent.evalsimplify(True).num)%1==0:
					return True
			return False
	def evalsimplify(self,approx=False):
		newroot=self.root.evalsimplify(approx)
		newexponent=self.exponent.evalsimplify(approx)
		if newroot.evaluable(approx) and newexponent.evaluable(approx):
			evaluated=eval(newroot.tostring().replace("^","**"))**eval(newexponent.tostring().replace("^","**"))
			if evaluated%1==0:
				evaluated=int(evaluated)
			if approx==False and evaluated%1!=0:
				return potens([newroot,newexponent])
			return newevaluednum(evaluated)
		return potens([newroot,newexponent])
	def simplifyallparts(self,focus):
		newparts=[]
		for n in self.rootandexponents:
			newparts.append(n.simplify(focus))
	
		if len(newparts)==1:return newparts[0]
		return potens(newparts)
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		for n in self.rootandexponents:
			if n.contains(varstring):
				return True
		return False
	def approx(self):
		
		return self.evalsimplify(True)
	def ntothe1(self,focus):
		if self.exponent==number(["1"]):
			return self.root
		return False
	def sameexponentfrac(self,focus): #(focus/b)^c=focus^c/b^c
		if self.root.type()=="division":
			if  (focus!=None and self.root.contains(focus.tostring())) or (focus==None or (  self.root.contains(focus.tostring())==False and self.exponent.contains(focus.tostring())==False)):
				newnumb=potens([self.root.numerator,self.exponent])
				newdenom=potens([self.root.denominator,self.exponent])
				return division([newnumb,newdenom])
		return False
	def antisameroot(self,focus):
		if self.exponent.type()=="addition":
			if focus!=None and self.exponent.contains(focus.tostring()):
				expadds=self.exponent.addends
				inputarr=[]
				for n in expadds:
					inputarr.append(potens([self.root,n]))
				return maybeclass(inputarr,product)
		return False
	def antisameexponent(self,focus): #(b*c)^a=b^a*c^a
		if self.root.type()=="product":
			if focus==None or focus!=None and self.root.contains(focus.tostring()):
				newprod=[]
				for n in self.root.factors:
					newprod.append(potens([n,self.exponent]))
				return product(newprod)
		return False
	def compareinfo(self):
		
		return [self.type(),[self.root,self.exponent]]
	def potenspotens(self,focus):
		if self.root.type()=="potens":
			if focus==None or self.root.root.contains(focus.tostring()):
				return potens([self.root.root,product([self.root.exponent,self.exponent])])
		return False	
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def findvariables(self):
		variables=[]
		for n in [self.root,self.exponent]:
			for k in n.findvariables():
				if k not in variables:
					variables.append(k)
		return variables
	def nomials(self): #(a+b+..)^n | n i N
		if self.root.type()=="addition":
			newself=self.evalsimplify()
			if newself.root.type()=="addition" and newself.exponent.type()=="number":
				if newself.exponent.evaluable() and float(newself.exponent.num)%1==0 and float(newself.exponent.num)>0:
					exponentint=int(newself.exponent.num)
					proddyfactors=[]
					for n in range(exponentint):
						proddyfactors.append(deepcopy(self.root))
					proddy=product(proddyfactors).distributive("force")
					while True:
						newaddends=[]
						for addend in proddy.addends:
							if addend.type()=="product":
								testdist=addend.distributive("force")
								if addend.type()=="product" and testdist!=False:
									newaddends+=testdist.addends
								else:
									newaddends.append(addend)
							else:
								newaddends.append(addend)
						newproddy=addition(newaddends)
						if newproddy.__eq__(proddy,False):
							return newproddy.simplify()
						else:
							proddy=newproddy
		return False
	def expand(self):
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"POTENS: "+self.tostring())
		for n in [self.root,self.exponent]:
			n.printtree(rec+1)
	def makepossiblesubstitutions(self):
		newarr=[]
		for n in [self.root,self.exponent]:
			newarr.append(n.makepossiblesubstitutions())
		if maybeclass(newarr,potens)!=self:
			return maybeclass(newarr,potens).makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),2]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		newarr=[]
		for n in [self.root,self.exponent]:
			newarr.append(n.substitute(subthisexp,tothisexp))
		if maybeclass(newarr,potens)!=self:
			return maybeclass(newarr,potens).substitute(subthisexp,tothisexp)
		return self
class division:
	def __init__(self,arr):
		self.arr=arr
		self.numerator=arr[0]
		self.denominator=arr[1]
		self.isunit=False
		self.onelineprint=False
		if self.numerator.type() in cancallisunit and self.numerator.isunit:
			if self.denominator.type() in cancallisunit and self.denominator.isunit:
				self.isunit=True
		if self.numerator.type() in ["number","potens"] and self.numerator.isunit:
			if self.denominator.type() in ["number","potens"] and self.denominator.isunit:
				self.onelineprint=True
	def type(self):
		
		return "division"
	def tostring(self,substitute=False):#
		taeller=self.numerator.tostring()
		naevner=self.denominator.tostring()
		if "*" in taeller or "+" in taeller or "-" in taeller or "/" in taeller:
			taeller="("+taeller+")"
		if "*" in naevner or "+" in naevner or "-" in naevner or "/" in naevner:
			naevner="("+naevner+")"
		return taeller+"/"+naevner
	def tolatex(self,roundit=False):
		if self.onelineprint:
			return self.numerator.tolatex(roundit)+"/"+self.denominator.tolatex(roundit)
		else:
			return r"\frac{"+self.numerator.tolatex(roundit)+"}{"+self.denominator.tolatex(roundit)+"}"
	def simplify(self,focus=None,thrd=0):#
		
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		
		return max([n.maxleveloftree(level+1) for n in [self.numerator,self.denominator]])
	def evaluable(self,approx=False):
		for k in [self.numerator,self.denominator]:
			if not k.evaluable(approx):
				return False
		if approx==False and self.numerator.type()=="number" and self.denominator.type()=="number":
			if float(self.numerator.tostring())%1==0 and float(self.denominator.tostring())%1==0:
				lcf=gcd(float(self.numerator.num),float(self.denominator.num))
				self.numerator=newnumber( [str(int(float(self.numerator.num)/lcf))] )
				self.denominator=newnumber([str(int(float(self.denominator.tostring())/lcf))])
				return False
		return True
	def evalsimplify(self,approx=False):
		newnum=self.numerator.evalsimplify(approx)
		newdenom=self.denominator.evalsimplify(approx)
		if approx:
			if newnum.evaluable(approx) and newdenom.evaluable(approx):
				evaluated=eval(newnum.tostring().replace("^","**"))/eval(newdenom.tostring().replace("^","**"))
				if evaluated%1==0:
					evaluated=int(evaluated)
				return newevaluednum(evaluated)
			elif newnum.evaluable(approx):
				if newdenom.type()=="product" and newdenom.factors[0].evaluable(True):
					returnnum=division([newnum,newdenom.factors[0]]).evalsimplify(approx)
					returndenom=newdenom.delfactor(0)
					return division([returnnum,returndenom])
			elif newdenom.evaluable(approx):
				if newnum.type()=="product" and newnum.factors[0].evaluable(True):
					joined=division([newnum.factors[0],newdenom]).evalsimplify(True)
					returnrest=newnum.delfactor(0)
					return product([joined,returnrest])
			elif newnum.type()=="product" and newnum.factors[0].evaluable(True) and newdenom.type()=="product" and newdenom.factors[0].evaluable(True):
				joined=division([newnum.factors[0],newdenom.factors[0]]).evalsimplify(True)
				retval=division([product([joined,newnum.delfactor(0)]),newdenom.delfactor(0)])
				return retval
			return self
		elif approx==False:
			if newnum.evaluable(approx) and newdenom.evaluable(approx):
				approxeval=eval(newnum.tostring().replace("^","**"))/eval(newdenom.tostring().replace("^","**"))
				if approxeval%1==0:
					approxeval=int(approxeval)
					return newevaluednum(approxeval)
				elif eval(newnum.tostring().replace("^","**"))%1==0 and eval(newdenom.tostring().replace("^","**"))%1==0:
					nummy=int(newnum.tostring())
					denommy=int(newdenom.tostring())
					lcf=gcd(nummy,denommy)
					return division([newnumber([str(nummy//lcf)]),newnumber([str(denommy//lcf)])])
				else:
					return division([newnum,newdenom])
			else:
				return division([newnum,newdenom])
		else:
			raise ValueError
	def simplifyallparts(self,focus):
		newparts=[]
		for n in [self.numerator,self.denominator]:
			newparts.append(n.simplify(focus))

		if len(newparts)==1:return newparts[0]
		return division(newparts)
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		for n in [self.numerator,self.denominator]:
			if n.contains(varstring):
				return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.numerator,self.denominator]]
	def approx(self):
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def ndiv1(self,focus):
		if self.denominator==newnumber(["1"]):
			return self.numerator
		elif self.denominator==number(["-1"]):
			return product([number(["-1"]),self.numerator])
		else:
			return False
	def samerootofexponentfactors(self,focus=None): #same thing as samerootofexponent, just with factors
		if self.numerator.type()=="product" and self.denominator.type()=="product":
			appendtofactors=[]
			skiptheseids=[]
			breakall=False
			for numfact in self.numerator.factors:
				for denomfact in self.denominator.factors:
					#create newfraction
					createfract=division([numfact,denomfact])
					if createfract.samerootofexponent(focus)!=False:
						skiptheseids+=[id(numfact),id(denomfact)]
						appendtofactors.append(createfract.samerootofexponent(focus))
						breakall=True
						break
				if breakall:
					break
			if breakall:#simplifications happened
				newnum=maybeclass(appendtofactors+[n for n in self.numerator.factors if id(n) not in skiptheseids],product)
				newdenom=maybeclass([n for n in self.denominator.factors if id(n) not in skiptheseids],product)
				return maybeclass([newnum,newdenom],division)
		elif self.numerator.type()=="product":
			skipthisindex=False
			for index,numfact in enumerate(self.numerator.factors):
				createfract=division([numfact,self.denominator]).samerootofexponent(focus)
				if createfract!=False:
					appendtofactors=createfract
					skipthisindex=index
					break
			if skipthisindex!=False:
				newfactors=[createfract]
				for n in range(len(self.numerator.factors)):
					if n!=skipthisindex:
						newfactors.append(self.numerator.factors[n])
				return maybeclass(newfactors,product)
		elif self.denominator.type()=="product":
			skipthisindex=False
			for index,denomfact in enumerate(self.denominator.factors):
				createfract=division([self.numerator,denomfact]).samerootofexponent(focus)
				if createfract!=False:
					appendtonum=createfract
					skipthisindex=index
					break
			if skipthisindex!=False:
				newdenoms=[]
				for n in range(len(self.denominator.factors)):
					if n!=skipthisindex:
						newdenoms.append(self.denominator.factors[n])
				newnum=maybeclass([appendtonum,self.numerator],product)
				newdenom=maybeclass(newdenoms,product)
				return maybeclass([newnum,newdenom],division)
		return False
	def samerootofexponent(self,focus=None): #a^b/a^c=a^(b-c)
		debug(3,"samerootofexponent fik input: "+str(self.tostring()))
		if self.numerator.type()=="potens" and self.denominator.type()=="potens":
			#OLDif self.numerator.rootandexponents[0]==self.denominator.rootandexponents[0] and (focus==None or focus==self.denominator.rootandexponents[0] or addition([maybeclass(self.numerator.rootandexponents[1:],potens),product([number(["-1"]),maybeclass(self.denominator.rootandexponents[1:],potens)])]).contains(focus.tostring())==False):
			if self.numerator.root==self.denominator.root:
				if (focus!=None and self.numerator.root.contains(focus.tostring())) or (self.numerator.exponent.evaluable(True) and self.denominator.exponent.evaluable(True)):
					newroot=self.numerator.rootandexponents[0]
					sum1=self.numerator.rootandexponents[1:]
					sum2=self.denominator.rootandexponents[1:]
					newexponent=addition([maybeclass(sum1,potens),product([number(["-1"]),maybeclass(sum2,potens)])])
					debug(3,"samerootofexponent output: "+potens([newroot,newexponent]).tostring())
					return potens([newroot,newexponent])
		elif self.numerator.type()=="potens":
			if self.numerator.root==self.denominator:
				if (focus!=None and self.numerator.root.contains(focus.tostring())) or (self.numerator.exponent.evaluable(True)):
					newroot=self.denominator
					return potens([newroot,addition([self.numerator.exponent,number(["1"])])])
		elif self.denominator.type()=="potens":
			if self.denominator.root==self.numerator:
				if (focus!=None and self.numerator.contains(focus.tostring())) or (self.denominator.root.evaluable(True)):
					newroot=self.numerator
					return potens([newroot,addition([self.denominator.exponent,number(["1"])])])
		return False
	def antisameexponentfrac(self,focus=None): #b^a/c^a=(b/c)^a
		if self.numerator.type()=="potens" and self.denominator.type()=="potens":
			num=self.numerator
			denom=self.denominator
			if num.exponent==denom.exponent:
				if (focus!=None and num.exponent.contains(focus.tostring())):
					return potens([division([num.root,denom.root]),num.exponent])

		return False
	def findvariables(self):
		variables=[]
		for n in [self.numerator,self.denominator]:
			for k in n.findvariables():
				if k not in variables:
					variables.append(k)
		return variables
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"DIVISION: "+self.tostring())
		for n in [self.numerator,self.denominator]:
			n.printtree(rec+1)
	def shortfract(self,focus=None): #forkorter brøker hvis de kan
		if self.numerator.type()=="product":
			if self.denominator.type()=="product":
				newnumerator=self.numerator.evalpart()
				newdenom=self.denominator.evalpart()
			else:
				newnumerator=self.numerator.evalpart()
				newdenom=self.denominator
			if newnumerator.type()=="product":
				if newdenom.type()=="product":
					shortnum=newnumerator.factors[0]
					shortdenom=newdenom.factors[0]
					if shortnum.evaluable() and shortdenom.evaluable():
						evaluablefract=division([shortnum,shortdenom]).evalsimplify()
						if evaluablefract.type()=="number":
							evaluablefract=division([evaluablefract,number(["1"])])
						if evaluablefract.numerator!=number(["1"]):
							newnumerator.factors[0]=evaluablefract.numerator
						else:
							newnumerator=newnumerator.delfactor(0)
						if evaluablefract.denominator!=number(["1"]):
							newdenom.factors[0]=evaluablefract.denominator
						else:
							newdenom=newdenom.delfactor(0)
						retval=division([newnumerator,newdenom])
						if not retval.__eq__(self,False):
							return division([newnumerator,newdenom])
				else:
					pass
		return False
	def cancelfactors(self,focus=None): #b*a/b => b etc etc
		if self.numerator.type()=="product":
			if self.denominator.type()=="product":
				for in1,fact1 in enumerate(self.numerator.factors):
					for in2,fact2 in enumerate(self.denominator.factors):
						if fact1==fact2:
							numerfactors=self.numerator.delfactor(in1)
							denomfactors=self.denominator.delfactor(in2)
							if type(numerfactors)!=type(list()):
								numerfactors=[numerfactors]
							if type(denomfactors)!=type(list()):
								denomfactors=[denomfactors]
							return division([maybeclass(numerfactors,product),maybeclass(denomfactors,product)])
			else:
				fact2=self.denominator
				for in1,fact1 in enumerate(self.numerator.factors):
					if fact1==fact2:
						newfacts=self.numerator.delfactor(in1)
						if type(newfacts)!=type(list()):
							return newfacts
						return maybeclass(newfacts,product)
		else:
			if self.denominator.type()=="product":
				fact2=self.numerator
				for in1,fact1 in enumerate(self.denominator.factors):
					if fact1==fact2:
						newfacts=self.denominator.delfactor(in1)
						if type(newfacts)!=type(list()):
							return division([number(["1"]),newfacts])
						return division([number(["1"]),maybeclass(newfacts,product)])
			else:
				if self.numerator==self.denominator:
					return number(["1"])
		return False
	def makepossiblesubstitutions(self):
		newarr=[]
		for n in [self.numerator,self.denominator]:
			newarr.append(n.makepossiblesubstitutions())
		if maybeclass(newarr,division)!=self:
			return maybeclass(newarr,division).makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),2]
	def movefactordownifalone(self,focus=None):#(2_m)/_s => 2*(_m/_s)
		if self.numerator.type()=="product":
			newnum=self.numerator.moveconstantsinfront()
			if newnum==False:
				newnum=self.numerator

			if newnum.factors[0].type()=="number":
				canmovedown=True
				for elsefactor in newnum.factors[1:]:
					if elsefactor.type() in cancallisunit and elsefactor.isunit:

						continue
					canmovedown=False
					break
				if canmovedown:
					newdenom=self.denominator.evalsimplify(True)
					if newdenom.type()=="product" and newdenom.factors[0].evaluable(True):
						return False
					elif newdenom.evaluable(True):
						return False
					multiplier=newnum.factors[0]
					return product([multiplier,division([maybeclass(newnum.factors[1:],product),self.denominator])])
		return False
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		newarr=[]
		for n in [self.numerator,self.denominator]:
			newarr.append(n.substitute(subthisexp,tothisexp))
		if maybeclass(newarr,division)!=self:
			return maybeclass(newarr,division).substitute(subthisexp,tothisexp)
		return self
class addition:
	def __init__(self,arr):
		self.arr=arr
		self.addends=arr
	def type(self):
		
		return "addition"
	def tostring(self,substitute=False):
		mathstring=""
		for n in [n.tostring() for n in self.arr]:
			if mathstring!="" and n[0]!="-":mathstring+="+"
			mathstring+=n
		return mathstring
	def tolatex(self,roundit=False):
		mathstring=""
		for n in [n.tolatex(roundit) for n in self.arr]:
			if mathstring!="" and n[0]!="-":mathstring+="+"
			mathstring+=n
		return mathstring
	def simplify(self,focus=None,thrd=0):
		
		return SimplifyAll(self,focus,thrd)
	def simplifyallparts(self,focus):
		newparts=[]
		for n in self.addends:
			newparts.append(n.simplify(focus))
		if len(newparts)==1:return newentitylist[0]
		return addition(newparts)		
	def antidistributive(self,focus=None): #k*a+n*a=(k+n)*a
		debug(3,"antidistributive fik input: "+str(self.tostring())+" og self.addends:")
		[debug(3,"             "+str(n.tostring())) for n in self.addends]
		Runagain=False
		breakall=False
		for index1,add1 in enumerate(self.addends):
			if add1.type()=="product":
				for index2,add2 in enumerate(self.addends):
					if add2.type()=="product" and index1!=index2: 
							factors1=add1.factors
							factors2=add2.factors
							for in1,factor1 in enumerate(factors1):
								for in2,factor2 in enumerate(factors2):
									if factor1==factor2 and (focus==None or focus==factor2 or not addition([add1.delfactor(in1),add2.delfactor(in2)]).contains(focus.tostring())  ):
										if factor1.evaluable():continue
										if focus!=None and addition([add1.delfactor(in1),add2.delfactor(in2)]).contains(focus.tostring()):continue
										Runagain=True

										unified=product([addition([add1.delfactor(in1),add2.delfactor(in2)]),factor1])		
										skiptheseids=[id(add1),id(add2)]
										breakall=True
										break
								if breakall:break
					elif add2.type()!="product" and index1!=index2:
						for in1,factor1 in enumerate(add1.factors):
							if factor1==add2 and (focus==None or focus==factor1 or not addition([number(["1"]),add1.delfactor(in1)]).contains(focus.tostring())):
								if factor1.evaluable() or (focus!=None and addition([number(["1"]),add1.delfactor(in1)]).contains(focus.tostring())):continue
								Runagain=True
								unified=product([addition([number(["1"]),add1.delfactor(in1)]),add2])
								skiptheseids=[id(add1),id(add2)]
								breakall=True
								break
					if breakall:break
			elif add1.type()!="product":
				for index2,add2 in enumerate(self.addends):
					if add2.type()=="product" and index1!=index2:
							factors2=add2.factors
							for in2,factor2 in enumerate(factors2):
								if add1==factor2 and (focus==None or focus==factor2 or not addition([number(["1"]),add2.delfactor(in2)]).contains(focus.tostring()) ):
									if factor2.evaluable() or focus!=None and addition([number(["1"]),add2.delfactor(in2)]).contains(focus.tostring()):continue
									Runagain=True
									unified=product([addition([number(["1"]),add2.delfactor(in2)]),add1])		
									skiptheseids=[id(add1),id(add2)]
									breakall=True
									break
							if breakall:break
					elif add2.type()!="product" and index1!=index2:
						if add1==add2:
							Runagain=True
							unified=product([number(["2"]),add2])
							skiptheseids=[id(add1),id(add2)]
							breakall=True
							break
						elif add1.tostring()=="-"+add2.tostring() or "-"+add1.tostring()==add2.tostring():
							Runagain=True
							unified=number(["0"])
							breakall=True
							skiptheseids=[id(add1),id(add2)]
							break
					if breakall:break
			if breakall:
				break
		if Runagain==True:
			newaddends=[unified]
			for n in self.addends:
				if id(n) not in skiptheseids:
					newaddends.append(n)
			if len(newaddends)==1:
				debug(3,"antidistributive output (1): "+str(newaddends[0].tostring()))
				return newaddends[0]
			else:
				simplifiedsum=addition(newaddends)
				"""if simplifiedsum.antidistributive(focus)!=False:
					return simplifiedsum.antidistributive(focus)"""
				debug(3,"antidistributive output (2): "+simplifiedsum.tostring())
				return simplifiedsum
		return False
	def maxleveloftree(self,level=0):
		
		return max([n.maxleveloftree(level+1) for n in self.addends])
	def evaluable(self,approx=False):
		for k in self.addends:
			if not k.evaluable(approx):
				return False
		return True
	def evalsimplify(self,approx=False):
		newaddends=[n.evalsimplify(approx) for n in self.addends]
		evaluedsum=0
		newnewaddends=[]
		for n in newaddends:
			if n.evaluable(approx):
				evaluedsum+=eval(n.tostring().replace("^","**"))
			else:
				newnewaddends.append(n)
		if evaluedsum%1==0:
			evaluedsum=int(evaluedsum)
		if newnewaddends==[]:
			return newevaluednum(evaluedsum)
		if evaluedsum==0:
			return maybeclass(newnewaddends,addition)
		else:
			summedup=[newevaluednum(evaluedsum)]+newnewaddends
			return maybeclass(summedup,addition)
	def evalpart(self,approx=False):
		newarr=[]
		summy=0
		for n in self.addends:
			if n.evaluable(approx):
				summy+=float(n.tostring())
			else:
				newarr.append(n)
		if summy%1==0:summy=int(summy)
		if summy==0:
			retval=newarr
		else: 
			retval=[newnumber([str(summy)])]+newarr
		return maybeclass(retval,addition)
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		for n in self.addends:
			if n.contains(varstring):
				return True
		return False
	def compareinfo(self):

		return [self.type(),self.addends]
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		useditems=[]
		for n in info1[1]:
			foundmatch=False
			for index,k in enumerate(info2[1]):
				if n.__eq__(k,False) and index not in useditems:
					useditems.append(index)
					foundmatch=True
					break
			if foundmatch==False:
				return False
		return True
	def associativeprop(self,focus):
		newaddends=[]
		retfalse=True
		for n in self.addends:
			if n.type()=="addition":
				retfalse=False
				newaddends+=n.addends
			else:
				newaddends.append(n)
		if retfalse:
			return False
		return maybeclass(newaddends,addition)
	def approx(self):
		
		return self.evalsimplify(True)
	def findvariables(self):
		variables=[]
		for n in self.addends:
			for k in n.findvariables():
				if k not in variables:
					variables.append(k)
		return variables
	def expand(self):

		return ExpandAll(self)
	def NonIntrusiveAntiDistributive(self,focus=None):
		breakitall=False
		for index1,addend1 in enumerate(self.addends):
			for index2,addend2 in enumerate(self.addends):
				if index1==index2:continue
				if addend1.type()=="product":
					if addend2.type()=="product":
						for in1,factor1 in enumerate(addend1.factors):
							for in2,factor2 in enumerate(addend2.factors):
								if factor1==factor2:
									if not factor1.evaluable(True):
										resten1=addend1.delfactor(in1)
										resten2=addend2.delfactor(in2)

										if resten1.evaluable(True) and resten2.evaluable(True):
											newfront=addition([resten1,resten2])
											unified=product([newfront,factor1])
											breakitall=True
											skiptheseids=[id(addend1),id(addend2)]
											break
					else:
						for in1,factor1 in enumerate(addend1.factors):
							if factor1==addend2:
								if not factor1.evaluable(True):
									resten1=addend1.delfactor(in1)
									if resten1.evaluable(True):
										unified=product([addition([number(["1"]),resten1]),factor1])
										breakitall=True
										skiptheseids=[id(addend1),id(addend2)]
										break
				else:
					if addend2.type()=="product":
						for in2,factor2 in enumerate(addend2.factors):
							if addend1==factor2:
								if not factor2.evaluable(True):
									resten2=addend2.delfactor(in2)
									if resten2.evaluable(True):
										unified=product([addition([number(["1"]),resten2]),factor2])
										breakitall=True
										skiptheseids=[id(addend1),id(addend2)]
										break
					else:
						if addend1==addend2 and not addend1.evaluable(True):
							unified=product([number(["2"]),addend1])
							breakitall=True
							skiptheseids=[id(addend1),id(addend2)]
							break
				if breakitall:break
			if breakitall:break
		if breakitall:
			if unified.associativeprop()!=False:
				unified=unified.associativeprop()
			newaddends=[unified]
			for n in self.addends:
				if id(n) not in skiptheseids:
					newaddends.append(n)
			return maybeclass(newaddends,addition)

		return False						
	def printtree(self,rec=0):
		print("   "*rec+"ADDITION: "+self.tostring())
		for n in self.addends:
			n.printtree(rec+1)
	def posforms(self,stringortex,approx=False):
		return posformsimplify(self,stringortex,approx)
	def makepossiblesubstitutions(self):
		newarr=[]
		for n in self.addends:
			newarr.append(n.makepossiblesubstitutions())
		if maybeclass(newarr,addition)!=self:
			return maybeclass(newarr,addition).makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),len(self.addends)]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		newarr=[]
		for n in self.addends:
			newarr.append(n.substitute(subthisexp,tothisexp))
		if maybeclass(newarr,addition)!=self:
			return maybeclass(newarr,addition).substitute(subthisexp,tothisexp)
		return self
"""
product
division
addition
number
potens
"""
def ExpandAll(instance): #Expands and simplifies (a little)
	newinstance=treesimplify(deepcopy(instance))
	while True:
		if newinstance.type()=="addition":
			newinstance=maybeclass([ExpandAll(n) for n in newinstance.addends],addition)
			newinstance=treesimplify(newinstance)
			testy=newinstance.NonIntrusiveAntiDistributive(None)
			if testy!=False:
				newinstance=testy
				continue
		elif newinstance.type()=="product":
			newinstance=maybeclass([ExpandAll(n) for n in newinstance.factors],product)
			newinstance=treesimplify(newinstance)
			distributexp=newinstance.distributive("force")
			if distributexp!=False:
				newinstance=distributexp
				continue
			ntime0exp=newinstance.ntimes0(None)
			if ntime0exp!=False:
				newinstance=ntime0exp
				continue
			evalpartexp=newinstance.evalpart()
			if evalpartexp.tostring()!=newinstance.tostring():
				newinstance=evalpartexp
				continue
			fractionexp=newinstance.fractionasfactor()
			if fractionexp!=False:
				newinstance=fractionexp
				continue
			moveinexp=newinstance.moveconstantsinfront()
			if moveinexp!=False:
				newinstance=moveinexp
				continue
			samerootnonintrusiveexp=newinstance.sameroot(True)
			if samerootnonintrusiveexp!=False:
				newinstance=samerootnonintrusiveexp
				continue
		elif newinstance.type()=="potens":
			newinstance=maybeclass([ExpandAll(n) for n in [newinstance.root,newinstance.exponent]],potens)
			newinstance=treesimplify(newinstance)
			nomialexp=newinstance.nomials()
			if nomialexp!=False:
				newinstance=nomialexp
				continue
		elif newinstance.type()=="division":
			newinstance=maybeclass([ExpandAll(n) for n in [newinstance.numerator,newinstance.denominator]],division)
			newinstance=treesimplify(newinstance)
			fract2exp=newinstance.cancelfactors()
			if fract2exp!=False:
				newinstance=fract2exp
				continue
		elif newinstance.type()=="number":
			pass
		elif newinstance.type()=="sine":
			newinstance=sine([ExpandAll(newinstance.arg)])
		elif newinstance.type()=="cosine":
			newinstance=cosine([ExpandAll(newinstance.arg)])
		elif newinstance.type()=="tangent":
			newinstance=tangent([ExpandAll(newinstance.arg)])
		elif newinstance.type()=="arcsine":
			newinstance=arcsine([ExpandAll(newinstance.arg)])
		elif newinstance.type()=="arccosine":
			newinstance=arccosine([ExpandAll(newinstance.arg)])
		elif newinstance.type()=="arctangent":
			newinstance=arctangent([ExpandAll(newinstance.arg)])
		elif newinstance.type()=="natlogarithm":
			newinstance=natlogarithm([ExpandAll(newinstance.arg)])
		elif newinstance.type()=="comlogarithm":
			newinstance=comlogarithm([ExpandAll(newinstance.arg)])
		elif newinstance.type()=="squareroot":
			newinstance=squareroot([ExpandAll(newinstance.arg)])
		elif newinstance.type()=="unknownfunction":
			newinstance=unknownfunction(newinstance.funcstr,ExpandAll(newinstance.inputexp))
		else:
			raise ValueError("869 - Expected instance")
		break
	return treesimplify(treesimplify(newinstance).evalsimplify())

def treesimplify(instance): #simplifies trees (via the 2 associativeprop() functions)
	newinstance=instance
	if True: #simplifyparts
		if instance.type()=="addition":
			newinstance=maybeclass([treesimplify(n) for n in instance.addends],addition)
		elif instance.type()=="product":
			newinstance=maybeclass([treesimplify(n) for n in instance.factors],product)
		elif instance.type()=="potens":
			newinstance=maybeclass([treesimplify(n) for n in [instance.root,instance.exponent]],potens)
		elif instance.type()=="division":
			newinstance=maybeclass([treesimplify(n) for n in [instance.numerator,instance.denominator]],division)
		elif instance.type()=="number":
			newinstance=instance
	if newinstance.type()=="addition" or newinstance.type()=="product":
		if newinstance.associativeprop(None)!=False:
			newinstance=newinstance.associativeprop(None)
	if newinstance.type()=="product":
		if newinstance.moveconstantsinfront()!=False:
			newinstance=newinstance.moveconstantsinfront()
	return newinstance


#Simplificeringsmetoder
SimplifyClassdict=dict() #kommer til at indeholde som index typen af klassen (produkt fx) og saa en array af simplificeringsmetoder som strings
subdict=definitiondict()
def posformsimplify(instance,stringortex,approx=False): #1 for strings, 2 for tex 0 for instance
	instancecopy=deepcopy(instance)
	instancecopy=instancecopy.makepossiblesubstitutions()
	instancecopy=treesimplify(instancecopy)
	if instancecopy.type()=="number":
		if stringortex==1:
			return [instancecopy.tostring()]
		elif stringortex==2:
			return [instancecopy.tolatex()]
		elif stringortex==0:
			return [instancecopy]
	retvar=[]
	expanded=instancecopy.expand()
	if not expanded.__eq__(instancecopy,False):
		retvar.append(expanded)
	for focus1 in instancecopy.findvariables()+[None]:
		if None==focus1:
			focus2=None
		else:
			focus2=number([focus1])
		testsimp=SimplifyAll(instancecopy,focus2)
		willbeadded=True
		for alreadyfound in retvar:
			if testsimp.__eq__(alreadyfound,False):
				willbeadded=False
				break
		if willbeadded and not testsimp.__eq__(instancecopy,False):
			retvar.append(testsimp)
	if retvar==[]:
		retvar.append(instancecopy)
	if approx:
		retvar=[n.approx() for n in retvar]
	if stringortex==0:
		return retvar
	elif stringortex==1:
		return [n.tostring() for n in retvar]
	elif stringortex==2:
		return [n.tolatex() for n in retvar]
def SimplifyAll(instance,focus,specialsimp=0): #specialsimp=1 betyder simplify på strings, 2 er for latex
	instancecopy=deepcopy(instance)
	instancecopy=instancecopy.makepossiblesubstitutions()
	instancecopy=treesimplify(instancecopy)
	if instancecopy.type()=="number" and specialsimp==0:
		return instancecopy
	if specialsimp in [1,2]:
		retvar=[]
		expanded=instancecopy.expand()
		if not expanded.__eq__(instancecopy,False):
			retvar.append(expanded)
		for focus1 in instancecopy.findvariables()+[None]:
			if None==focus1:
				focus2=None
			else:
				focus2=number([focus1])
			testsimp=SimplifyAll(instancecopy,focus2)
			willbeadded=True
			for alreadyfound in retvar:
				if testsimp.__eq__(alreadyfound,False):
					willbeadded=False
					break
			if willbeadded and not testsimp.__eq__(instancecopy,False):
				retvar.append(testsimp)
		if specialsimp==1:
			return [n.tostring() for n in retvar]
		elif specialsimp==2:
			return [n.tolatex() for n in retvar]

	debug(2,"SimplifyAll fik input: "+instance.tostring())
	newsimplify=instancecopy.simplifyallparts(focus).evalsimplify()
	debug(2,"SIMPLIFYING DONE FROM "+instance.tostring()+" to "+newsimplify.tostring())
	try:
		
		Simplifyingmethods=SimplifyClassdict[newsimplify.type()]
	except KeyError:
		try:
			methodfile=open("Simplify Methods/"+newsimplify.type()+".simplifymethods")
		except:
			try:
				methodfile=open(sys.argv[0].replace("TextCAS.py","")+"Simplify Methods/"+newsimplify.type()+".simplifymethods")
			except:
				raise ValueError("Could not find the .simplifymethod files")

		rawmethods=methodfile.readlines()
		#debug(3,"METHODS FOUND FOR CLASS:"+newsimplify.type()+"\n"+str(rawmethods))
		methods=[line.replace("\n","") for line in rawmethods]
		#debug(1,"METHODS FOUND FOR CLASS:"+newsimplify.type()+"\n"+str(methods))
		SimplifyClassdict[newsimplify.type()]=methods
		Simplifyingmethods=methods
		methodfile.close()
	for method in Simplifyingmethods:
		testingifmethodworked=eval("newsimplify."+method+"(focus)")
		if testingifmethodworked!=False:
			debug(2,"SIMPLIFYING FROM "+newsimplify.tostring()+" TO "+testingifmethodworked.tostring()+" VIA "+method)
			return testingifmethodworked.simplify(focus)
	debug(2,"(HELT FAERDIG) SimplifyAll  output fra: "+newsimplify.tostring()+" til "+newsimplify.evalsimplify().tostring())
	return newsimplify.evalsimplify()

def maybeclass(arr,classfunc):
	if len(arr)==1:
		return arr[0]
	elif len(arr)>1:
		return classfunc(arr)
def newnumber(arr):
	num=arr[0]
	if num=="-1":
		return number(["-1"])
	if num[0]=="-":
		return product([number(["-1"]),number([num[1:]])])
	return number([num])
def newevaluednum(inputfloat):
	if inputfloat>10**9 or inputfloat<-10**9:
		exponent=int(math.log10(inputfloat))
		multiplier=str(inputfloat)[0]+"."+str(inputfloat).replace(".","")[1:]
		return potens([newnumber([multiplier]),newnumber([str(exponent)])])
	elif inputfloat<0.001 and inputfloat>-0.001:
		if inputfloat==0:
			return number(["0"])
		if "e" not in str(inputfloat):
			raise ValueError("Bad translation of float")
		else:
			rets=str(inputfloat).split("e")
			return potens([newnumber([rets[0]]),newnumber([rets[1]])])
	else:
		return newnumber([str(inputfloat)])
class sine:
	def __init__(self,arr):
		if len(arr)!=1:
			raise ValueError("more than one argument in sine class")
		self.arg=arr[0]
	def type(self):
		return "sine"
	def tostring(self,substitute=False):
		return "sin("+self.arg.tostring()+")"
	def tolatex(self,roundit=False):
		return r"\sin\left("+self.arg.tolatex(roundit)+r"\right)"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.arg.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		if not self.arg.evaluable():
			return False
		if approx:
			return True
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			newarg=self.arg.evalsimplify(approx)
			if Use_Radians:
				realnum=math.sin(eval(newarg.tostring().replace("^","**")))
			else:
				realnum=math.sin(const_pi/180*eval(newarg.tostring().replace("^","**")))
			return newevaluednum(realnum)
		else:
			return self	
	def simplifyallparts(self,focus):
		
		return sine([self.arg.simplify(focus)])
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.arg.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.arg]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]: #if not the same types
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"sine: "+self.tostring())
		self.arg.printtree(rec+1)
	def findvariables(self):
		return self.arg.findvariables()
	def makepossiblesubstitutions(self):
		retval=sine([self.arg.makepossiblesubstitutions()])
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=sine([self.arg.substitute(subthisexp,tothisexp)])
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self

class cosine:
	def __init__(self,arr):
		if len(arr)!=1:
			raise ValueError("more than one argument in cosine class")
		self.arg=arr[0]
	def type(self):
		return "cosine"
	def tostring(self,substitute=False):
		return "cos("+self.arg.tostring()+")"
	def tolatex(self,roundit=False):
		return r"\cos\left("+self.arg.tolatex(roundit)+r"\right)"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.arg.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		if not self.arg.evaluable():
			return False
		if approx:
			return True
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			newarg=self.arg.evalsimplify(approx)
			if Use_Radians:
				realnum=math.cos(eval(newarg.tostring().replace("^","**")))
			else:
				realnum=math.cos(const_pi/180*eval(newarg.tostring().replace("^","**")))
			return newevaluednum(realnum)
		else:
			return self	
	def simplifyallparts(self,focus):
		
		return cosine([self.arg.simplify()])
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.arg.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.arg]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"cosine: "+self.tostring())
		self.arg.printtree(rec+1)
	def findvariables(self):
		return self.arg.findvariables()
	def makepossiblesubstitutions(self):
		retval= cosine([self.arg.makepossiblesubstitutions()])
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=cosine([self.arg.substitute(subthisexp,tothisexp)])
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self


class tangent:
	def __init__(self,arr):
		if len(arr)!=1:
			raise ValueError("more than one argument in tangent class")
		self.arg=arr[0]
	def type(self):
		return "tangent"
	def tostring(self,substitute=False):
		return "tan("+self.arg.tostring()+")"
	def tolatex(self,roundit=False):
		return r"\tan\left("+self.arg.tolatex(roundit)+r"\right)"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.arg.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		if not self.arg.evaluable():
			return False
		if approx:
			return True
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			newarg=self.arg.evalsimplify(approx)
			if Use_Radians:
				realnum=math.tan(eval(newarg.tostring().replace("^","**")))
			else:
				realnum=math.tan(const_pi/180*eval(newarg.tostring().replace("^","**")))
			return newevaluednum(realnum)
		else:
			return self	
	def simplifyallparts(self,focus):
		
		return tangent([self.arg.simplify()])
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.arg.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.arg]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"tangent: "+self.tostring())
		self.arg.printtree(rec+1)
	def findvariables(self):
		return self.arg.findvariables()
	def makepossiblesubstitutions(self):
		retval= tangent([self.arg.makepossiblesubstitutions()])
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=tangent([self.arg.substitute(subthisexp,tothisexp)])
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self

class arcsine:
	def __init__(self,arr):
		if len(arr)!=1:
			raise ValueError("more than one argument in arcsine class")
		self.arg=arr[0]
	def type(self):
		return "arcsine"
	def tostring(self,substitute=False):
		return "arcsin("+self.arg.tostring()+")"
	def tolatex(self,roundit=False):
		return r"\arcsin\left("+self.arg.tolatex(roundit)+r"\right)"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.arg.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		if not self.arg.evaluable():
			return False
		if approx:
			return True
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			newarg=self.arg.evalsimplify(approx)
			if eval(newarg.tostring().replace("^","**"))>1 or eval(newarg.tostring().replace("^","**"))<-1:return self
			if Use_Radians:
				realnum=math.asin(eval(newarg.tostring().replace("^","**")))
			else:
				realnum=180/const_pi*math.asin(eval(newarg.tostring().replace("^","**")))
			return newevaluednum(realnum)
		else:
			return self	
	def simplifyallparts(self,focus):
		
		return arcsine([self.arg.simplify()])
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.arg.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.arg]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"arcsine: "+self.tostring())
		self.arg.printtree(rec+1)
	def findvariables(self):
		return self.arg.findvariables()
	def makepossiblesubstitutions(self):
		retval=arcsine([self.arg.makepossiblesubstitutions()])
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=arcsine([self.arg.substitute(subthisexp,tothisexp)])
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self
class arccosine:
	def __init__(self,arr):
		if len(arr)!=1:
			raise ValueError("more than one argument in arccosine class")
		self.arg=arr[0]
	def type(self):
		return "arccosine"
	def tostring(self,substitute=False):
		return "arccos("+self.arg.tostring()+")"
	def tolatex(self,roundit=False):
		return r"\arccos\left("+self.arg.tolatex(roundit)+r"\right)"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.arg.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		if not self.arg.evaluable():
			return False
		if approx:
			return True
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			newarg=self.arg.evalsimplify(approx)
			if eval(newarg.tostring().replace("^","**"))>1 or eval(newarg.tostring().replace("^","**"))<-1:return self
			if Use_Radians:
				realnum=math.acos(eval(newarg.tostring().replace("^","**")))
			else:
				realnum=180/const_pi*math.acos(eval(newarg.tostring().replace("^","**")))
			return newevaluednum(realnum)
		else:
			return self	
	def simplifyallparts(self,focus):
		
		return arccosine([self.arg.simplify()])
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.arg.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.arg]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"arccosine: "+self.tostring())
		self.arg.printtree(rec+1)
	def findvariables(self):
		return self.arg.findvariables()
	def makepossiblesubstitutions(self):
		retval= arccosine([self.arg.makepossiblesubstitutions()])
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=arccosine([self.arg.substitute(subthisexp,tothisexp)])
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self
class arctangent:
	def __init__(self,arr):
		if len(arr)!=1:
			raise ValueError("more than one argument in arctangent class")
		self.arg=arr[0]
	def type(self):
		return "arctangent"
	def tostring(self,substitute=False):
		return "arctan("+self.arg.tostring()+")"
	def tolatex(self,roundit=False):
		return r"\arctan\left("+self.arg.tolatex(roundit)+r"\right)"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.arg.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		if not self.arg.evaluable():
			return False
		if approx:
			return True
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			newarg=self.arg.evalsimplify(approx)
			if Use_Radians:
				realnum=math.atan(eval(newarg.tostring().replace("^","**")))
			else:
				realnum=180/const_pi*math.atan(eval(newarg.tostring().replace("^","**")))
			return newevaluednum(realnum)
		else:
			return self	
	def simplifyallparts(self,focus):
		
		return arctangent([self.arg.simplify()])
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.arg.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.arg]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"arctangent: "+self.tostring())
		self.arg.printtree(rec+1)
	def findvariables(self):
		return self.arg.findvariables()
	def makepossiblesubstitutions(self):
		retval= arctangent([self.arg.makepossiblesubstitutions()])
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=arctangent([self.arg.substitute(subthisexp,tothisexp)])
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self


class natlogarithm:
	def __init__(self,arr):
		if len(arr)!=1:
			raise ValueError("more than one argument in natlogarithm class")
		self.arg=arr[0]
	def type(self):
		return "natlogarithm"
	def tostring(self,substitute=False):
		return "ln("+self.arg.tostring()+")"
	def tolatex(self,roundit=False):
		return r"\ln\left("+self.arg.tolatex(roundit)+r"\right)"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.arg.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		if not self.arg.evaluable():
			return False
		if approx:
			return True
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			newarg=self.arg.evalsimplify(approx)
			if eval(newarg.tostring().replace("^","**"))<=0:return self
			realnum=math.log(eval(newarg.tostring().replace("^","**")))
			return newevaluednum(realnum)
		else:
			return self	
	def simplifyallparts(self,focus):
		
		return natlogarithm([self.arg.simplify()])
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.arg.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.arg]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"natlogarithm: "+self.tostring())
		self.arg.printtree(rec+1)
	def findvariables(self):
		return self.arg.findvariables()
	def makepossiblesubstitutions(self):
		retval= natlogarithm([self.arg.makepossiblesubstitutions()])
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=natlogarithm([self.arg.substitute(subthisexp,tothisexp)])
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self
class comlogarithm: #log_10
	def __init__(self,arr):
		if len(arr)!=1:
			raise ValueError("more than one argument in comlogarithm class")
		self.arg=arr[0]
	def type(self):
		return "comlogarithm"
	def tostring(self,substitute=False):
		return "log("+self.arg.tostring()+")"
	def tolatex(self,roundit=False):
		return r"\log\left("+self.arg.tolatex(roundit)+r"\right)"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.arg.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		if not self.arg.evaluable():
			return False
		if approx:
			return True
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			newarg=self.arg.evalsimplify(approx)
			if eval(newarg.tostring().replace("^","**"))<=0:return self
			realnum=math.log10(eval(newarg.tostring().replace("^","**")))
			return newevaluednum(realnum)
		else:
			return self	
	def simplifyallparts(self,focus):
		
		return comlogarithm([self.arg.simplify()])
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.arg.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.arg]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"comlogarithm: "+self.tostring())
		self.arg.printtree(rec+1)
	def findvariables(self):
		return self.arg.findvariables()
	def makepossiblesubstitutions(self):
		retval= comlogarithm([self.arg.makepossiblesubstitutions()])
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=comlogarithm([self.arg.substitute(subthisexp,tothisexp)])
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self
class squareroot:
	def __init__(self,arr):
		if len(arr)!=1:
			raise ValueError("more than one argument in squareroot class")
		self.arg=arr[0]
	def type(self):
		return "squareroot"
	def tostring(self,substitute=False):
		return "sqrt("+self.arg.tostring()+")"
	def tolatex(self,roundit=False):
		return r"\sqrt{"+self.arg.tolatex(roundit)+r"}"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.arg.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		if not self.arg.evaluable():
			return False
		if approx:
			return True
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			newarg=self.arg.evalsimplify(approx)
			newnum=eval(newarg.tostring().replace("^","**"))
			if newnum<0:return self

			realnum=math.sqrt(newnum)
			return newevaluednum(realnum)
		else:
			return self	
	def simplifyallparts(self,focus):
		
		return squareroot([self.arg.simplify()])
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.arg.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.arg]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"squareroot: "+self.tostring())
		self.arg.printtree(rec+1)
	def findvariables(self):
		
		return self.arg.findvariables()
	def makepossiblesubstitutions(self):
		retval= squareroot([self.arg.makepossiblesubstitutions()])
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=squareroot([self.arg.substitute(subthisexp,tothisexp)])
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self
class unknownfunction:
	def __init__(self,funcstr,inputexp):
		self.funcstr=funcstr
		self.inputexp=inputexp
	def type(self):
		return "unknownfunction"
	def tostring(self,substitute=False):
		return self.funcstr+"("+self.inputexp.tostring()+")"
	def tolatex(self,roundit=False):
		return self.funcstr+r"\left("+self.inputexp.tolatex()+r"\right)"
	def simplify(self,focus=None,thrd=0):###
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		return self.inputexp.maxleveloftree(level+1)
	def evaluable(self,approx=False):
		return False
	def evalsimplify(self,approx=False):
		return self
	def simplifyallparts(self,focus):
		
		return unknownfunction(self.funcstr,self.inputexp.simplify())
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if self.inputexp.contains(varstring):
			return True
		return False
	def compareinfo(self):
		
		return [self.type(),[self.funcstr,self.inputexp]]
	def approx(self):
	
		return self.evalsimplify(True)
	def __eq__(self,other,firstrecursion=False):
		if other in [False,None,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if type(other)==type(str()):return False
		if firstrecursion:
			newself=self.simplify(None)
			newother=other.simplify(None)
			return newself.__eq__(newother,False)
		info1=self.compareinfo()
		info2=other.compareinfo()
		if info1[0]!=info2[0]:
			return False
		return info1[1]==info2[1]
	def expand(self):
		
		return ExpandAll(self)
	def posforms(self,stringortex,approx=False):
		
		return posformsimplify(self,stringortex,approx)
	def printtree(self,rec=0):
		print("   "*rec+"unknownfunction:"+self.tostring())
		self.inputexp.printtree(rec+1)
	def findvariables(self):
		
		return self.inputexp.findvariables()
	def makepossiblesubstitutions(self):
		retval=subdict.findfuncsub(self.funcstr,self.inputexp)
		if retval!=False:
			return retval.makepossiblesubstitutions()
		retval= unknownfunction(self.funcstr,self.inputexp.makepossiblesubstitutions())
		if retval!=self:
			return retval.makepossiblesubstitutions()
		return self
	def getsimplifyscore(self):
		return [self.maxleveloftree(),1]
	def substitute(self,subthisexp,tothisexp):
		if subthisexp.type()!="number":
			raise ValueError("bad substitution number")
		retval=unknownfunction(self.funcstr,self.inputexp.substitute(subthisexp,tothisexp))
		if retval!=self:
			return retval.substitute(subthisexp,tothisexp)
		return self