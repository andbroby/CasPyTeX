
def debug(lvl,message): 
	"""
	Really simple debugging tool
	one can make a debugging message like this:
	debug(0,"This is a very important debugging message")
	The first argument represents the urgency of the debugging message, 
	and can be any number.  
	Has the variable debug.lvl which one definds in the script you're debugging in
	if the function is called, it will print the message if the lvl you input is 
	smaller or equal than the set debug.lvl
	This way, one can change how verbose
	"""
	debug.lvl
	if lvl<=debug.lvl:
		print(message)
	else:
		return 0