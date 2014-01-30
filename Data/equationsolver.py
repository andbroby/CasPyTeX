import Entityclass as ent
class equation:
	def __init__(self,leftexp,rightexp): #leftexp=rightexp
		self.leftexp=leftexp
		self.rightexp=rightexp
	def movesolvenumstoleftside(self,solvesideinput,constantsideinput,solvenum,firstrun=True):
		solvenumstring=solvenum.num
		if solvesideinput.contains(solvenumstring) and not constantsideinput.contains(solvenumstring):
			return [solvesideinput,constantsideinput]
		elif constantsideinput.contains(solvenumstring) and not solvesideinput.contains(solvenumstring):
			return [constantsideinput,solvesideinput]
		elif not constantsideinput.contains(solvenumstring) and not solvesideinput.contains(solvenumstring):
			return [constantsideinput,solvesideinput]

		solveside=solvesideinput.simplify(solvenum)
		constantside=constantsideinput.simplify(solvenum)
		if constantside.type()=="addition": #
			newconstantsideaddends=[]
			newsolvesideaddends=[solveside]
			for addend in constantside.addends:
				if addend.contains(solvenumstring):
					newsolvesideaddends.append( ent.maybeclass([ent.number(["-1"]),addend],ent.product)   )
				else:
					newconstantsideaddends.append(addend)
			newsolveside=ent.addition(newsolvesideaddends)
			newconstantside=ent.addition(newconstantsideaddends)
			return self.movesolvenumstoleftside(newsolveside,newconstantside,solvenum,False)
		elif constantside.type()=="product":
			newsolvedividors=[]
			newconstantsidefacts=[]
			for factor in constantside.factors:
				if factor.contains(solvenumstring):
					newsolvedividors.append(factor)
				else:
					newconstantsidefacts.append(factor)
			newsolveside=ent.division([solveside,ent.maybeclass(newsolvedividors,ent.product)])
			newconstantside=ent.maybeclass(newconstantsidefacts,ent.product)
			return self.movesolvenumstoleftside(newsolveside,newconstantside,solvenum,False)
		elif constantside.type()=="division":
			num=constantside.numerator
			denom=constantside.denominator
			if num.contains(solvenumstring):
				newsolveside=ent.addition([solveside,ent.product([ent.number(["-1"]),constantside])])
				newconstantside=ent.number(["0"])
			elif denom.contains(solvenumstring):
				newsolveside=ent.product([denom,solveside])
				newconstantside=num
			return self.movesolvenumstoleftside(newsolveside,newconstantside,solvenum,False)
		elif constantside.type()=="potens":
			root=constantside.root
			exponent=constantside.exponent
			newsolveside=ent.addition([solveside,ent.product([ent.number(["-1"]),constantside])])
			newconstantside=ent.number(["0"])
			return self.movesolvenumstoleftside(newsolveside,newconstantside,solvenum,False)
		elif constantside.type() in ["number","sine","cosine","tangent","arcsine","arccosine","arctangent","natlogarithm","comlogarithm","squareroot"]:
			newsolveside=ent.addition([solveside,ent.product([ent.number(["-1"]),constantside])])
			newconstantside=ent.number(["0"])	
			return self.movesolvenumstoleftside(newsolveside,newconstantside,solvenum,False)
	def tolatex(self):
		
		return self.leftexp.tolatex()+"="+self.rightexp.tolatex()
	def solve(self,solvenum): #solvenum er instance
		#simplify both sides
		if solvenum.type()!="number":
			raise ValueError("Bad value to solve for")
		movedarr1=[n.simplify(solvenum) for n in self.movesolvenumstoleftside(self.leftexp.simplify(solvenum),self.rightexp.simplify(solvenum),solvenum)]
		movedarr2=[n.simplify(solvenum) for n in self.movesolvenumstoleftside(self.rightexp.simplify(solvenum),self.leftexp.simplify(solvenum),solvenum)]
		solveside=movedarr1[0]
		constantside=movedarr1[1]
		solvetry1=self.recursesolve(solveside,constantside,solvenum)
		if solvetry1!=None:
			return solvetry1
		solvetry2=self.recursesolve(movedarr2[0],movedarr2[1],solvenum)
		return solvetry2
	def recursesolve(self,solvesideinput,constantsideinput,solvenum): #GOT TO RETURN ARRAYS OR BOOLS
		solvestring=solvenum.num
		solveside=solvesideinput.simplify(solvenum)
		constantside=constantsideinput
		if solvesideinput==solvenum:
			return [constantsideinput]
		if not solveside.contains(solvestring):
			return None
		if solveside.type()=="addition":
			returnfromindividualsolve=self.solveaddition(solveside,constantside,solvenum)
		elif solveside.type()=="product":
			returnfromindividualsolve=self.solveproduct(solveside,constantside,solvenum)
		elif solveside.type()=="division":
			returnfromindividualsolve=self.solvedivison(solveside,constantside,solvenum)
		elif solveside.type()=="potens":
			returnfromindividualsolve=self.solvepotens(solveside,constantside,solvenum)
		else:
			return None
		solutions=[]
		if returnfromindividualsolve==None:
			return None
		for nextstep in returnfromindividualsolve:
			if self.recursesolve(nextstep[0],nextstep[1],solvenum)!=None:
				for solution in self.recursesolve(nextstep[0],nextstep[1],solvenum):
					if solution not in solutions:
						solutions.append(solution)
		return [n.simplify() for n in solutions]
		
	def solveaddition(self,solveside,constantside,solvenum):
		newaddends=[]
		newconstandsideaddends=[constantside]
		for addend in solveside.addends:
			if addend.contains(solvenum.num):
				newaddends.append(addend)
			else:
				newconstandsideaddends.append(ent.product([ent.number(["-1"]),addend]))
		returnsolveside=ent.maybeclass(newaddends,ent.addition)
		returnconstantside=ent.maybeclass(newconstandsideaddends,ent.addition)
		if len(newaddends)!=1:
			degrees=False
			ispol=True
			poladdends=[[ent.product([ent.number(["-1"]),returnconstantside]).simplify(solvenum),0]]# [coeff,potens]
			subvalue=False #the part that contains x
			for addend in newaddends:
				coeffadd=False
				if addend.type()=="product":
					for index,fact in enumerate(addend.factors):
						if fact.contains(solvenum.num):
							if coeffadd==False:
								if fact.type()=="potens":
									if fact.exponent.evaluable(True) and eval(fact.exponent.tostring().replace("^","**"))%1==0 and (subvalue==False or fact.root==subvalue) and coeffadd==False:
										subvalue=fact.root
										coeffadd=[addend.delfactor(index),int(eval(fact.exponent.tostring().replace("^","**")))]
									else:
										ispol=False
										break
								elif fact.type()=="product": #damned negative number
									if fact.factors[1].type()=="potens":
										exponent=fact.factors[1].exponent
										if exponent.evaluable(True) and eval(exponent.tostring().replace("^","**"))%1==0 and (subvalue==False or fact1.factors[1].root==subvalue) and coeffadd==False:
											subvalue=fact.factors[1].root
											coeffadd=[ent.product([ent.number(["-1"]),addend.delfactor(index)]),int(eval(exponent.tostring().replace("^","**")))]
										else:
											ispol=False
											break
									else:
										thisval=fact.factors[1]
										if coeffadd==False and (subvalue==False or thisval==subvalue):
											subvalue=thisval
											coeffadd[ent.product([ent.number(["-1"]),addend.delfactor(index)]),1]
										else:
											ispol=False
											break
								else:
									if coeffadd==False and (subvalue==False or subvalue==fact):			
										subvalue=fact
										coeffadd=[addend.delfactor(index),1]
									else:
										ispol=False
										break
							else:
								ispol=False
								break
				elif addend.type()=="potens":
					if coeffadd==False and (addend.exponent.evaluable(True) and eval(addend.exponent.tostring().replace("^","**"))%1==0 and (subvalue==False or addend.root==subvalue)):
						subvalue=addend.root
						coeffadd=[ent.number(["1"]),int(eval(addend.exponent.tostring().replace("^","**")))]
					else:
						ispol=False
						break
				else:
					if coeffadd==False and (subvalue==False or addend==subvalue):
						subvalue=addend
						coeffadd=[ent.number(["1"]),1]

					else:
						ispol=False
						break
				if coeffadd!=False:
					poladdends.append(coeffadd)
			if subvalue==False or not ispol:
				return None
			polsolveresult=self.polsolve(poladdends)
			retvar=[]
			for solution in polsolveresult:
				retvar.append([subvalue,solution])
			return retvar
		return [[returnsolveside,returnconstantside]]
	def polsolve(self,coeffarr):
		degree=max([n[1] for n in coeffarr])
		if degree==2:
			a=ent.number(["0"])
			b=ent.number(["0"])
			c=ent.number(["0"])
			for n in coeffarr:
				if n[1]==0:
					if c!=ent.number(["0"]):
						raise ValueError("bad polynomial")
					c=n[0]
				elif n[1]==1:
					if b!=ent.number(["0"]):
						raise ValueError("bad polynomial")
					b=n[0]
				elif n[1]==2:
					if a!=ent.number(["0"]):
						raise ValueError("bad polynomial")
					a=n[0]

			minusfour=ent.product([ent.number(["-1"]),ent.number(["4"])])
			sqrtdiscriminant=ent.potens([ent.addition([ent.potens([b,ent.number(["2"])]),ent.product([minusfour,a,c])]),ent.division([ent.number(["1"]),ent.number(["2"])])])
			solvedenominator=ent.product([ent.number(["2"]),a])
			minusb=ent.product([ent.number(["-1"]),b])
			minussquarerootd=ent.product([ent.number(["-1"]),sqrtdiscriminant])
			solutionone=ent.division([ent.addition([minusb,sqrtdiscriminant]),solvedenominator])
			solutiontwo=ent.division([ent.addition([minusb,minussquarerootd]),solvedenominator])
			
			return [solutionone,solutiontwo]
	def solveproduct(self,solveside,constantside,solvenum):
		newsolvefactors=[]
		newconstdividors=[]
		for factor in solveside.factors:
			if factor.contains(solvenum.num):
				newsolvefactors.append(factor)
				
			else:
				newconstdividors.append(factor)
		returnsolveside=ent.maybeclass(newsolvefactors,ent.product)
		returnconstant=ent.division([constantside,ent.maybeclass(newconstdividors,ent.product)])
		if len(newsolvefactors)!=1:
			return None
		return [[returnsolveside,returnconstant]]
	def solvedivison(self,solveside,constantside,solvenum):
		if not solveside.denominator.contains(solvenum.num):
			returnsolveside=solveside.numerator
			returnconstantside=ent.product([constantside,solveside.denominator])
			return [[returnsolveside,returnconstantside]]
		if not solveside.numerator.contains(solvenum.num):
			returnsolveside=ent.product([solveside.denominator,constantside])
			returnconstantside=solveside.numerator
			return [[returnsolveside,returnconstantside]]
		return None
	def solvepotens(self,solveside,constantside,solvenum):
		root=solveside.root
		exponent=solveside.exponent
		if not exponent.contains(solvenum.num):
			#if exponent==ent.number(["2"]):

			#	returnsolveside=root
			#	returnconstantside=ent.squareroot([constantside])
			#	return [[returnsolveside,returnconstantside],[returnsolveside,ent.product([ent.number(["-1"]),returnconstantside])]]
			if exponent.evaluable(True) and eval(exponent.tostring().replace("^","**"))%2==0:
				returnsolveside=root
				returnconstantside=ent.potens([constantside,ent.division([ent.number(["1"]),exponent])])
				return [[returnsolveside,returnconstantside],[returnsolveside,ent.product([ent.number(["-1"]),returnconstantside])]]
			else:
				returnsolveside=root
				returnconstantside=ent.potens([constantside,ent.division([ent.number(["1"]),exponent])])
				return [[returnsolveside,returnconstantside]]
		if not root.contains(solvenum.num):
			returnsolveside=exponent
			returnconstantside=ent.division([ent.natlogarithm([constantside]),ent.natlogarithm([root])])
			return [[returnsolveside,returnconstantside]]

		return None
