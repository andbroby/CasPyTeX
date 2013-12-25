import os
from subprocess import call
from sys import platform
from tkinter import *
from tkinter import ttk
import sys

sys.path.insert(0, 'Data/')
import textparser
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
	def clean(self):
		self.lines=[r'\documentclass{article}'+"\n",r'\begin{document}'+"\n",r'\subsection{Esbens Maskine}'+"\n",r'\end{document}'+"\n"]
fily=LatexFile("EXPERIMENTSANDFORSKNING")
fily.compiletolatex()
def SimplifyButton(*args):
	a=simplifyinput.get()
	fily.addline(r"\\Input:")
	exp=textparser.TextToCAS(a)
	fily.addline(r"\["+exp.tolatex()+r"\]")
	result=exp.simplify("ThisIsForTheLatexCompiler")
	fily.addline(r"\\Possible forms:")
	for n in result:
		fily.addline(r"\["+n+r"\]")
	fily.compiletolatex()

def pdfwipe(*args):
	fily.clean()
	fily.compiletolatex()

root = Tk()
root.title("CAS")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

simplifyinput = StringVar()

Simplifyentry = ttk.Entry(mainframe, width=30, textvariable=simplifyinput)
Simplifyentry.grid(column=2, row=1, sticky=(W, E))

ttk.Button(mainframe, text="Simplify", command=SimplifyButton).grid(column=3, row=1, sticky=E)
ttk.Button(mainframe, text="Clean PDF", command=pdfwipe).grid(column=3,row=3,sticky=E)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

Simplifyentry.focus()
root.bind('<Return>', SimplifyButton)

root.mainloop()
