CasPyTeX
------------------------------
![alt tag](http://i.imgur.com/14PCKRd.png)

*CasPyTex is able to solve equations with units. The blue color is optional, and can be changed in the config.*

**CasPyTex is still in development, so there's almost definitely bugs**

This is a simple CAS with different interfaces capable of outputting in LaTeX.

Right now, it has a working web interface which is opened by WebGUI.py

It also features a .cpt interpreter. The syntax of a .cpt (CasPyTex) file is showed in Doc/TextCAS Tutorial/tutorial.cpt.pdf . It's a lot like markdown.

The project is developed just for the fun of it.

To-do
-------------
- Update the Webinterface, and remove any interfaces that are not used
- More simplifying methods for functions (trig, logs and sqrt)
- Still more simplifying methods for fractions (WHEN WILL IT EEEEND)
- Support for smart units (Make the CAS know that 1km=1000m)
- Solving methods for more of the expression classes


Dependencies
-------------
- Python3.x
- MiKTeX (pdflatex needs to be in path)

Installation
--------------
1. Download and unzip the .zip of the repository
2. Run WebGUI.py for the webinterface to run as a server on LOCALHOST
3. Run Data/TextCAS.py with a .cpt file as an argument