CasPyTeX
------------------------------
**It's still in development.**

This is a simple CAS with different interfaces capable of outputting in LaTeX.

Right now, it has a working web interface which is opened by WebGUI.py

It also features a .cpt interpreter. The syntax of a .cpt (CasPyTex) file is showed in Doc/TextCAS Tutorial/tutorial.cpt.pdf . It's a lot like markdown.

The project is developed just for the fun of it. The code is not  well-written.

To-do
-------------
- Update the Webinterface, and remove any interfaces that are not used
- Add documentation
- More simplifying methods for functions (trig, logs and sqrt)
- Simplifying fractions (when the numerator of a fraction is a fraction it self)
- Support for smart units (Make the CAS know that 1km=1000m)
- Fix bug in line 424 (units not getting put up in the numerator of the fraction)

Dependencies
-------------
- Python3.x
- MiKTeX (pdflatex needs to be in path)

Installation
--------------
1. Download and unzip the .zip of the repository
2. Run WebGUI.py for the webinterface to run as a server on LOCALHOST
3. Run Data/TextCAS.py with a .cpt file as an argument