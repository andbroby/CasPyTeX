from __future__ import division
from __future__ import print_function
def debug(lvl,message): #niveau 1 er meget alvorligt, niveau 2 er knap saa alvorligt, lvl 3 er debug
	debug.lvl
	if lvl<=debug.lvl:
		print(message)
	else:
		return 0