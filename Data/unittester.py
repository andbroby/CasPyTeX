import textparser
from debugger import *
debug.lvl=1
def unittest(filename,approx=False):
	print("Starting  "+filename.replace(".test","")+"\n---")
	f=open('Data/Tests/'+filename)
	problems = f.readlines()
	errors=0
	for problem in problems:
		if problem[0]=="#":continue
		errors+=problemtest(problem,approx)
	print(filename.replace(".test","")+"test results: "+str(errors)+" errors out of "+str(len(problems))+" problems"+ "\n")
	f.close()
	return errors
def problemtest(problem,approx=False):
	parts=problem.split("\"")
	parts=[parts[1],parts[3],parts[5]]
	inputstr=parts[0]
	resultstr=parts[1]
	focus=parts[2]
	if focus=="None":focus=None
	else:focus=textparser.TextToCAS(focus)
	print("         Trying to simplify: "+inputstr+"   =   "+resultstr)
	returningstr=textparser.TextToCAS(inputstr).simplify(focus).tostring()
	if approx:
		returningstr=textparser.TextToCAS(inputstr).simplify(focus).approx().tostring()

	if returningstr!=resultstr:
		print("ERROR:Tried to simplify: "+inputstr+"\n    CAS returned         : "+returningstr+"\n    But the answer was   : "+resultstr)
		return 1
	return 0
errors=0
errors+=unittest("Antidistributive.test")
errors+=unittest("Samerootofexponent.test")
errors+=unittest("sameexponentfrac.test")
errors+=unittest("sameroot.test")
errors+=unittest("antisameroot.test")
errors+=unittest("antisameexponentfrac.test")
errors+=unittest("sameexponent.test")
errors+=unittest("distributive.test")
errors+=unittest("antisameexponent.test")
errors+=unittest("Mixed.test")

print("\nSTARTING APPROX TESTS\n")
errors+=unittest("Approx.test",True)
print("TOTAL ERRORS:",errors)
