from stringmanipulations import *
from debugger import *

from fractions import gcd
from copy import deepcopy
class product:
	def __init__(self,arr): 
		self.arr=arr
		self.factors=arr
	def type(self):
		
		return "product"
	def tostring(self):###
		returnstring=""
		minuscounter=0
		newfactors=[]
		for n in self.factors:
			if n.type()=="number" and n.num=="-1":
				minuscounter+=1
			else:
				newfactors.append(n)
		returnstring="-"*(minuscounter%2)
		for n in newfactors:
			if n.type()=="addition":
				returnstring+="("+n.tostring()+")*"
			else:
				returnstring+=n.tostring()+"*"
		if returnstring[-1]=="*":returnstring=returnstring[:-1]
		return returnstring
	def tolatex(self):
		returnstring=""
		minuscounter=0
		newfactors=[]
		for n in self.factors:
			if n.type()=="number" and n.num=="-1":
				minuscounter+=1
			else:
				newfactors.append(n)
		returnstring="-"*(minuscounter%2)
		for n in newfactors:
			if n.type()=="addition":
				returnstring+=r"\left("+n.tolatex()+r"\right)\cdot "
			else:
				returnstring+=n.tolatex()+r"\cdot "
		if returnstring[-6:]==r"\cdot ":returnstring=returnstring[:-6]
		return returnstring
	def simplify(self,focus=None,thrd=0):###

		return SimplifyAll(self,focus,thrd)
	def delfactor(self,index):
		copy=self.factors[:]
		copy.pop(index)
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
		if self.evaluable(approx):
			return newnumber([str(eval(self.tostring().replace("^","**")))])
		else:
			newentitylist=[]
			for n in range(len(self.factors)):
				newentitylist.append(self.factors[n].evalsimplify(approx))
			if len(newentitylist)==1:return newentitylist[0]
			return product(newentitylist).evalpart()
	def evalpart(self,approx=False):
		newarr=[]
		proddy=1
		for n in self.factors:
			if n.evaluable(approx):
				proddy*=float(n.tostring())
			else:
				newarr.append(n)
		if proddy%1==0:proddy=int(proddy)
		if proddy==1:
			retval=newarr
		else: 
			retval=[newnumber([str(proddy)])]+newarr
		#if len(retval)==len(self.factors):
		#	return False
		newretval=[]
		for n in retval:
			if n.type()=="product":
				newretval+=n.factors
			else:
				newretval.append(n)
		return maybeclass(newretval,product)
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
	def __eq__(self,other,firstrecursion=True):
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
	def sameroot(self,focus):
		worked=False
		breakall=False
		for in1,fac1 in enumerate(self.factors):
			for in2,fac2 in enumerate(self.factors):
				if in1==in2:continue
				if fac1.type()=="potens":
					if fac2.type()=="potens":
						if fac1.root==fac2.root:
							if focus==None or fac1.root.contains(focus.tostring()) or  (fac1.exponent.contains(focus.tostring())==False and fac2.exponent.contains(focus.tostring())==False):
								newexp=maybeclass([fac1.exponent,fac2.exponent],addition)
								newroot=fac1.root
								newfact=potens([newroot,newexp])
								skipids=[id(fac1),id(fac2)]
								worked=True
								breakall=True
								break
					elif fac2.type()!="potens":
						if fac1.root==fac2:
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
	def printtree(self,rec=0):
		print("   "*rec+"PRODUCT: "+self.tostring())
		for n in self.factors:
			n.printtree(rec+1)
class number:
	def __init__(self,arr):
		self.arr=arr
		self.num=arr[0]
	def type(self):
		
		return "number"
	def tostring(self):
		
		return self.num
	def tolatex(self):
		
		return self.num
	def simplify(self,focus=None):###
		"""if self.evaluable():
			if float(self.num)%1==0:
				return number([str(int(float(self.num)))])"""
		return self
	def maxleveloftree(self,level=0):
		
		return level+1
	def evaluable(self,approx=False):
		for n in self.num:
			if n not in ["0","1","2","3","4","5","6","7","8","9",".","-"]:
				return False
		return True
	def evalsimplify(self,approx=False):
		if self.evaluable():
			if float(self.num)%1==0:
				self.num=str(int(float(self.num)))
		return self
	def contains(self,varstring):
		if varstring==None:
			return self.evaluable()
		if varstring==self.num:return True
		return False
	def compareinfo(self):

		return [self.type(),self.num]
	def approx(self):
		
		return self.evalsimplify(True)
	def __eq__(self,other,recursionNOTUSED=None):
		if type(other)==type(str()):return False
		if other in [None,False,"ThisIsTheSafestValueIcanThinkOf"]:return False
		if self.type()!=other.type():
			return False
		return self.num==other.num
	def findvariables(self):
		if not self.evaluable(True):
			return self.num
		return []
	def expand(self):
		return self
	def printtree(self,rec=0):
		print("   "*rec+self.num)
class potens:
	def __init__(self,arr):
		self.arr=arr
		self.rootandexponents=arr
		if len(arr)!=2:
			debug(1,"FORKERT POTENS, STOPPER PROGRAMMET")
			exit()
		self.root=arr[0]
		self.exponent=arr[1]
	def type(self):
		
		return "potens"
	def tostring(self):
		returnstring=""
		for n in self.rootandexponents:
			if n.type()!="number":
				returnstring+="("+n.tostring()+")^"
			else:
				returnstring+=n.tostring()+"^"
		if returnstring[-1]=="^":
			returnstring=returnstring[:-1]
		return returnstring
	def tolatex(self):
		returnstring=""
		if self.root.type()!="number":
			returnstring+=r"\left("+self.root.tolatex()+r"\right)^"
		else:
			returnstring+=self.root.tolatex()+"^"
		returnstring+="{"+self.exponent.tolatex()+"}"
		if returnstring[-1]=="^":
			returnstring=returnstring[:-1]
		return returnstring
	def simplify(self,focus=None,thrd=0):#
		
		return SimplifyAll(self,focus,thrd)
	def maxleveloftree(self,level=0):
		
		return max([n.maxleveloftree(level+1) for n in self.rootandexponents])
	def evaluable(self,approx=False):
		if self.root.evaluable(approx) and self.exponent.evaluable(approx):
			testroot=float(self.root.evalsimplify(approx).tostring())
			testexpo=float(self.exponent.evalsimplify(approx).tostring())
			if not approx and testroot%1==0 and testexpo%1!=0:
				return False
			return True
		return False
	def evalsimplify(self,approx=False):
		if self.evaluable(approx):
			return newnumber([str(eval(self.tostring().replace("^","**")))])
		else:
			newentitylist=[]
			for n in range(len(self.rootandexponents)):
				newentitylist.append(self.rootandexponents[n].evalsimplify(approx))
			if len(newentitylist)==1:return newentitylist[0]
			return potens(newentitylist)
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
			if focus!=None and self.root.contains(focus.tostring()):
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
	def __eq__(self,other,firstrecursion=True):
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
	def printtree(self,rec=0):
		print("   "*rec+"POTENS: "+self.tostring())
		for n in [self.root,self.exponent]:
			n.printtree(rec+1)
class division:
	def __init__(self,arr):
		self.arr=arr
		self.numerator=arr[0]
		self.denominator=arr[1]
	def type(self):
		
		return "division"
	def tostring(self):#
		taeller=self.numerator.tostring()
		naevner=self.denominator.tostring()
		if "*" in taeller or "+" in taeller or "-" in taeller or "/" in taeller:
			taeller="("+taeller+")"
		if "*" in naevner or "+" in naevner or "-" in naevner or "/" in naevner:
			naevner="("+naevner+")"
		return taeller+"/"+naevner
	def tolatex(self):
		
		return r"\frac{"+self.numerator.tolatex()+"}{"+self.denominator.tolatex()+"}"
	def simplify(self,focus=None):#
		
		return SimplifyAll(self,focus)
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
		if self.evaluable(approx):
			evalnum=eval(self.tostring().replace("^","**"))
			if evalnum%1==0 or approx==True:
				return newnumber([str(eval(self.tostring().replace("^","**")))])
			else:
				if self.numerator.type()=="number" and self.denominator.type()=="number":
					if float(self.numerator.tostring())%1==0 and float(self.denominator.tostring())%1==0:
						
						lcf=gcd(float(self.numerator.num),float(self.denominator.num))

						newarr=[newnumber( [str(float(self.numerator.num)/lcf)] ),newnumber([str(float(self.denominator.tostring())/lcf)])]
						return division(newarr)
					else: 
						return newnumber([str(eval(self.tostring().replace("^","**")))])
		else:
			newentitylist=[self.numerator.evalsimplify(approx),self.denominator.evalsimplify(approx)]
			if len(newentitylist)==1:return newentitylist[0]
			return division(newentitylist)
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
	def __eq__(self,other,firstrecursion=True):
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
	def samerootofexponent(self,focus=None): #a^b/a^c=a^(b-c)
		debug(3,"samerootofexponent fik input: "+str(self.tostring()))
		if self.numerator.type()=="potens" and self.denominator.type()=="potens":
			if self.numerator.rootandexponents[0]==self.denominator.rootandexponents[0] and (focus==None or focus==self.denominator.rootandexponents[0] or addition([maybeclass(self.numerator.rootandexponents[1:],potens),product([number(["-1"]),maybeclass(self.denominator.rootandexponents[1:],potens)])]).contains(focus.tostring())==False):
				newroot=self.numerator.rootandexponents[0]
				sum1=self.numerator.rootandexponents[1:]
				sum2=self.denominator.rootandexponents[1:]
				newexponent=addition([maybeclass(sum1,potens),product([number(["-1"]),maybeclass(sum2,potens)])])
				debug(3,"samerootofexponent output: "+potens([newroot,newexponent]).tostring())
				return potens([newroot,newexponent])
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
	def printtree(self,rec=0):
		print("   "*rec+"DIVISION: "+self.tostring())
		for n in [self.numerator,self.denominator]:
			n.printtree(rec+1)
class addition:
	def __init__(self,arr):
		self.arr=arr
		self.addends=arr
	def type(self):
		
		return "addition"
	def tostring(self):
		mathstring=""
		for n in [n.tostring() for n in self.arr]:
			if mathstring!="" and n[0]!="-":mathstring+="+"
			mathstring+=n
		return mathstring
	def tolatex(self):
		mathstring=""
		for n in [n.tolatex() for n in self.arr]:
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
		if self.evaluable(approx):
			return newnumber([str(eval(self.tostring().replace("^","**")))])
		else:
			newentitylist=[]
			for n in range(len(self.addends)):
				newentitylist.append(self.addends[n].evalsimplify(approx))
			if len(newentitylist)==1:return newentitylist[0]
			return addition(newentitylist).evalpart()
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
	def __eq__(self,other,firstrecursion=True):
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
		print("OI")
		for index1,addend1 in enumerate(self.addends):
			for index2,addend2 in enumerate(self.addends):
				if index1==index2:continue
				if addend1.type()=="product":
					if addend2.type()=="product":
						for in1,factor1 in enumerate(addend1.factors):
							for in2,factor2 in enumerate(addend2.factors):
								print(factor1.tostring(),factor2.tostring())
								if factor1==factor2:
									print("OI")
									if not factor1.evaluable(True):
										resten1=addend1.delfactor(in1)
										resten2=addend2.delfactor(in2)
										print("OIOIOI",resten1.evaluable(True),resten2.evaluable(True))
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




"""
product
division
addition
number
potens
"""
def ExpandAll(instance): #Expands and simplifies (a little)
	print(instance.tostring())
	newinstance=treesimplify(instance)
	while True:
		if newinstance.type()=="addition":
			newinstance=maybeclass([ExpandAll(n) for n in newinstance.addends],addition)
			newinstance=treesimplify(newinstance)
			testy=newinstance.NonIntrusiveAntiDistributive(None)
			if testy!=False:
				newinstance=testy
				print("antidist")
				continue
		elif newinstance.type()=="product":
			newinstance=maybeclass([ExpandAll(n) for n in newinstance.factors],product)
			newinstance=treesimplify(newinstance)
			distributexp=newinstance.distributive("force")
			if distributexp!=False:
				newinstance=distributexp
				print("dist")
				continue
			ntime0exp=newinstance.ntimes0(None)
			if ntime0exp!=False:
				newinstance=ntime0exp
				print("times0")
				continue
			evalpartexp=newinstance.evalpart(None)
			if evalpartexp.tostring()!=newinstance.tostring():
				newinstance=evalpartexp
				print("evalpart")
				continue
		elif newinstance.type()=="potens":
			newinstance=maybeclass([ExpandAll(n) for n in [newinstance.root,newinstance.exponent]],potens)
			newinstance=treesimplify(newinstance)
			nomialexp=newinstance.nomials()
			if nomialexp!=False:
				newinstance=nomialexp
				print("nomial")
				continue
		elif newinstance.type()=="division":
			newinstance=maybeclass([ExpandAll(n) for n in [newinstance.numerator,newinstance.denominator]],division)
			newinstance=treesimplify(newinstance)
		elif newinstance.type()=="number":
			pass
		else:
			raise ValueError("869 - Expected instance")
		break
	print(instance.tostring(),"TO",treesimplify(newinstance).evalsimplify().tostring())
	return treesimplify(treesimplify(newinstance).evalsimplify())
def ExpandAll2(instance):
	if True:
		if instance.type()=="number":
			return instance
		elif instance.type()=="product":
			newfactors=[]
			for factor in instance.factors:
				newfactors.append(factor.expand())
			newinstance=maybeclass(newfactors,product)
		elif instance.type()=="addition":
			newaddends=[]
			for addend in instance.addends:
				newaddends.append(addend.expand())
			newinstance=maybeclass(newaddends,addition)
		elif instance.type()=="potens":
			newrootandexp=[]
			for n in [instance.root,instance.exponent]:
				newrootandexp.append(n.expand())
			newinstance=maybeclass(newrootandexp,potens)
		elif instance.type()=="division":
			newnumanddenom=[]
			for n in [instance.numerator,instance.denominator]:
				newnumanddenom.append(n.expand())
			newinstance=maybeclass(newnumanddenom,division) #expandallparts
	if instance.type()=="addition":
		
		pass	
	if instance.type()=="product":
		distributexp=newinstance.distributive("force")
		if distributexp!=False:
			return ExpandAll(distributexp)
	if instance.type()=="division":
		
		pass
	if instance.type()=="number":
		
		pass
	if instance.type()=="potens":
		nomialexp=newinstance.nomials()
		if nomialexp!=False:
			return ExpandAll(nomialexp)
	if newinstance.type()=="addition":
		if newinstance.associativeprop(None)!=False:
			newinstance=newinstance.associativeprop(None)
		while True:
			testy=newinstance.NonIntrusiveAntiDistributive(None)
			if testy!=False:
				newinstance=testy
				if newinstance.type()!="addition":
					break
			else:
				break
	if newinstance.type()=="product":
		if newinstance.ntimes0(None)!=False:

			newinstance=newinstance.ntimes0(None)
	if newinstance.type()=="product":
		if newinstance.associativeprop(None)!=False:
			newinstance=newinstance.associativeprop(None)
	if newinstance.type()=="product":
		if newinstance.ntimes0(None)!=False:
			newinstance=newinstance.ntimes0(None)
	return newinstance.evalsimplify()

def treesimplify(instance): #simplifies trees (via the 2 associativeprop() functions)
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
	return newinstance


#Simplificeringsmetoder
SimplifyClassdict=dict() #kommer til at indeholde som index typen af klassen (produkt fx) og saa en array af simplificeringsmetoder som strings
def SimplifyAll(instance,focus,specialsimp=0): #specialsimp=1 betyder simplify på strings, 2 er for latex
	#instance.printtree()
	instance=treesimplify(instance)
	#instance.printtree()
	if specialsimp in [1,2]:
		retvar=[]
		expanded=instance.expand()
		if not expanded.__eq__(instance,False):
			print("EXPAND ADDED",expanded.tostring())
			retvar.append(expanded)
		for focus1 in instance.findvariables()+[None]:
			testsimp=SimplifyAll(instance,number([focus1]))
			willbeadded=True
			for alreadyfound in retvar:
				if testsimp.__eq__(alreadyfound,False):
					willbeadded=False
					break
			if willbeadded and not testsimp.__eq__(instance,False):
				retvar.append(testsimp)
		if specialsimp==1:
			return [n.tostring() for n in retvar]
		elif specialsimp==2:
			return [n.tolatex() for n in retvar]

	debug(2,"SimplifyAll fik input: "+instance.tostring())
	newsimplify=instance.simplifyallparts(focus).evalsimplify()
	debug(2,"SIMPLIFYING DONE FROM "+instance.tostring()+" to "+newsimplify.tostring())

	try:
		
		Simplifyingmethods=SimplifyClassdict[newsimplify.type()]
	except KeyError:
		try:
			methodfile=open("Simplify Methods/"+newsimplify.type()+".simplifymethods")
		except:
			try:
				methodfile=open("Data/Simplify Methods/"+newsimplify.type()+".simplifymethods")
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
	else:
		return 1/0
def newnumber(arr):
	num=arr[0]
	if num=="-1":
		return number(["-1"])
	if num[0]=="-":
		return product([number(["-1"]),number([num[1:]])])
	return number([num])
class otherfunction: #GLEMMES INDTIL VIDERE
	def __init__(self,arr):
		self.arr=arr
		self.factors=arr
	def type(self):
		
		return "otherfunction"
	def tostring(self):
		pass
	def simplify(self):
		return self
