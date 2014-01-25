
from sys import platform
from subprocess import call
class LatexFile:
	def __init__(self,filename="Test.tex",path=r"Latex Files"):
		if ".tex" not in filename:
			filename+=".tex"
		self.filename=filename
		self.path=path
		#if os.path.exists(filename):
			#self.latexfile = open(filename, "r+")
		#else:
			#self.latexfile = open(filename, "w")
		self.preamble=[r'\documentclass[11pt]{article}'+"\n",r"\usepackage{ae,aecompl}"+"\n",r"\usepackage[T1]{fontenc}"+"\n",r"\usepackage[utf8]{inputenc}"+"\n",r"\usepackage{color}"+"\n"]
		self.lines=[]
	def closefile(self):

		self.latexfile.close()
	def addline(self,rawstr):
		self.lines.append(rawstr+"\n")
	def addtopreamble(self,rawstr):
		self.preamble.append(rawstr+"\n")
	def linepop(self):
		if self.lines==[]:
			return True
		self.lines.pop()
	def writetofile(self):
		f=open(self.path+"/"+self.filename,"w")
		[f.write(line) for line in self.preamble+[r'\begin{document}'+"\n"]+self.lines+[r"\end{document}"+"\n"]]
	def compiletolatex(self):
		self.writetofile()
		if platform=="win32":
			call(["ls"],shell=True,cwd=self.path)
			call([r'pdflatex','-interaction=nonstopmode',self.filename],shell=True,cwd=self.path)
		else:
			callstr="cd \"LaTeX Files\";pdflatex -interaction=nonstopmode "+self.filename
			call([callstr],shell=True,cwd=self.path) 
	def clean(self):
		self.lines=[r'\documentclass{article}'+"\n",r'\begin{document}'+"\n",r'\subsection{Esbens Maskine}'+"\n",r'\end{document}'+"\n"]
