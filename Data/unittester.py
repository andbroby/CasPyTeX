import textparser
from debugger import *
"""
This is the script one can run to test all the tests in Data/Tests
It should be fairly straight forward to see what's going on
The syntax of a testing file should be simple; just look at the Mixed.test
"""

debug.lvl=0
def unittest(filename,approx=False):
	print("Starting  "+filename.replace(".test","")+"\n---")
	f=open('Tests/'+filename)
	problems = f.readlines()
	errors=0
	for problem in problems:
		if problem[0]=="#":continue
		errors+=problemtest(problem,approx)
	numofproblems=len(problems)
	print(filename.replace(".test","")+"test results: "+str(errors)+" errors out of "+str(len(problems))+" problems"+ "\n")
	f.close()
	return [errors, numofproblems]
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
errors=[0,0]
def vecadd(a,b):
	return [a[0]+b[0],a[1]+b[1]]
errors=vecadd(errors,unittest("Antidistributive.test"))
errors=vecadd(errors,unittest("Samerootofexponent.test"))
errors=vecadd(errors,unittest("sameexponentfrac.test"))
errors=vecadd(errors,unittest("sameroot.test"))
errors=vecadd(errors,unittest("antisameroot.test"))
errors=vecadd(errors,unittest("antisameexponentfrac.test"))
errors=vecadd(errors,unittest("sameexponent.test"))
errors=vecadd(errors,unittest("distributive.test"))
errors=vecadd(errors,unittest("antisameexponent.test"))
errors=vecadd(errors,unittest("Mixed.test"))

print("\nSTARTING APPROX TESTS\n")
errors=vecadd(errors,unittest("Approx.test",True))
print("Unittest finished: "+str(errors[0])+" errors out of "+str(errors[1])+" problems")
