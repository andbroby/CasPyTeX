import textparser
import os
from subprocess import call
from sys import platform
class LatexFile:
	def __init__(self,filename="Test.tex"):
		if ".tex" not in filename:
			filename+=".tex"
		self.filename=filename
		#if os.path.exists(filename):
			#self.latexfile = open(filename, "r+")
		#else:
			#self.latexfile = open(filename, "w")
		self.lines=[r'\documentclass{article}'+"\n",r'\begin{document}'+"\n",r'\subsection{Esbens Maskine}'+"\n",r'\end{document}'+"\n"]
	def closefile(self):

		self.latexfile.close()
	def addline(self,rawstr):
		self.lines.pop()
		self.lines.append(rawstr+"\n")
		self.lines.append(r'\end{document}\n'+"\n")
	def writetofile(self):
		f=open("LaTeX Files/"+self.filename,"w")
		[f.write(line) for line in self.lines]
	def compiletolatex(self):
		self.writetofile()
		if platform=="win32":
			call([r'pdflatex','-interaction=nonstopmode',self.filename],shell=True,cwd=r'LaTeX Files')
		else:
			callstr="cd \"LaTeX Files\";pdflatex -interaction=nonstopmode "+self.filename
			call([callstr],shell=True)
#a=LatexFile("HEHEHE")
#a.addline(r"\[ e^{i\cdot x}+1=0\]")
#a.writetofile()
#a.compiletolatex()
fily=LatexFile("EXPERIMENTSANDFORSKNING")
fily.compiletolatex()
while 1:
	a=input("Enter an expression:  ")
	fily.addline(r"\\Input:")
	exp=textparser.TextToCAS(a)
	fily.addline(r"\["+exp.tolatex()+r"\]")
	result=exp.simplify("ThisIsForTheLatexCompiler")
	fily.addline(r"\\Possible forms:")
	for n in result:
		fily.addline(r"\["+n+r"\]")
	fily.compiletolatex()