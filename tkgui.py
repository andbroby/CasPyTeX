import os
from tkinter import *
from tkinter import ttk
import sys

sys.path.insert(0, 'Data/')
import textparser
from latexfileclass import LatexFile
import textparser as cas
fily=LatexFile("EXPERIMENTSANDFORSKNING")
fily.compiletolatex()

def SimplifyButton(*args):
	a=simplifyinput.get()
	fily.addline(r"\\Input:")
	exp=textparser.TextToCAS(a)
	fily.addline(r"\["+exp.tolatex()+r"\]")
	#result=exp.simplify("ThisIsForTheLatexCompiler")
	result=exp.posforms(2,False)
	if type(result)==type(cas.TextToCAS("a")):
	    result=[result.tolatex()]

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
