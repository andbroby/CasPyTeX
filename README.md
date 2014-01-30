CasPyTeX
------------------------------
**It's still in development.**

This is a simple CAS with different interfaces capable of outputting in LaTeX.

Right now, it has a working web interface which is opened by WebGUI.py

It also features a .cpt interpreter. The syntax of a .cpt (CasPyTex) file is showed in Doc/TextCAS Tutorial/tutorial.cpt.pdf . It's a lot like markdown.

The project is developed just for the fun of it. The code is not  well-written.

To-do
-------------
- Update the tutorial.cpt.pdf
- Add documentation
- More simplifying methods for functions (trig, logs and sqrt)
- Simplifying fractions (a lot of simplifying fractions, and making sure things cancels out in fractions)
- support for smart units (Make the CAS know that 1km=1000m)

Dependencies
-------------
- Python3.x
- MiKTeX (pdflatex needs to be in path)

Installation
--------------
1. Download and unzip the .zip of the repository
2. Run WebGUI.py for the webinterface to run as a server on LOCALHOST
3. Run Data/TextCAS.py with a .cpt file as an example 
