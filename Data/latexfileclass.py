import os
from sys import platform
from subprocess import call
class LatexFile:
	"""
	Represents a latex file
	Important variables
	Lines : a list of strings that represents each line in the document
	preamble: a list of strings that represents each line the preamble
	"""
	def __init__(self,filename="Test.tex",path=r"Latex Files"):
		"""
		initiates the values
		"""
		if ".tex" not in filename:
			filename+=".tex"
		self.notex=filename[:-4]
		self.filename=filename
		self.path=path
		#if os.path.exists(filename):
			#self.latexfile = open(filename, "r+")
		#else:
			#self.latexfile = open(filename, "w")
		self.preamble=[r'\documentclass[11pt]{article}'+"\n",r"\setlength{\topmargin}{-.5in}"+"\n",r"\setlength{\textheight}{9in}"+"\n",r"\setlength{\oddsidemargin}{.125in}"+"\n",r"\setlength{\textwidth}{6.25in}"+"\n",r"\usepackage{ae,aecompl}"+"\n",r"\usepackage[T1]{fontenc}"+"\n",r"\usepackage[utf8]{inputenc}"+"\n",r"\usepackage{color}"+"\n"]
		self.lines=[]
	def closefile(self):
		"""
		Closes the file 
		"""
		self.latexfile.close()
	def addline(self,rawstr):
		"""
		Adds a line to the document (inside \begin{document})
		"""
		self.lines.append(rawstr+"\n")
	def addtopreamble(self,rawstr):
		"""
		Adds a line to the preamble
		"""
		self.preamble.append(rawstr+"\n")
	def linepop(self):
		"""
		Removes the last line from the document (not the preamble)
		"""
		if self.lines==[]:
			return True
		self.lines.pop()
	def writetofile(self):
		"""
		Writes the preamble and the lines to the document

		"""
		if platform=="win32":
			f=open(self.path+"\\"+self.filename,"w")
		else:
			f=open(self.path+"/"+self.filename,"w")
		[f.write(line) for line in self.preamble+[r'\begin{document}'+"\n"]+self.lines+[r"\end{document}"+"\n"]]
	def compiletolatex(self):
		"""
		Compiles to latex via pdflatex
		"""
		self.writetofile()
		if platform=="win32":
			diditwork=call([r'pdflatex','-interaction=nonstopmode',self.filename],shell=True,cwd=self.path,stdout=open(os.devnull,'wb'))
		else:
			callstr="pdflatex -interaction=nonstopmode "+self.filename
			diditwork=call([callstr],shell=True,cwd=self.path,stdout=open(os.devnull,'wb')) 
		for line in open(self.path+"/"+self.notex+".log").readlines():
			if "Output written on" in line:
				return True
		return False
	def clean(self):
		"""
		removes all document lines
		"""
		self.lines=[r'\documentclass{article}'+"\n",r'\begin{document}'+"\n",r'\subsection{Esbens Maskine}'+"\n",r'\end{document}'+"\n"]
