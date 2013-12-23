for x in range(11,100):
	bytom=(x%10)*10+x//10
	if (bytom-x)/x==3/4:
		print(x)
