def main():
	pass # no non-local variables
	
	def sqrt(n, shift):
		pass # no non-local variables
		x = None
		x_old = None
		n_one = None
		
		
		if (n) > (65535):
			return (2) * (sqrt((n) / (4), shift))
		else:
			pass
		
		x = shift
		n_one = (n) * (shift)
		while True:
			x_old = x
			x = ((x) + ((n_one) / (x))) / (2)
			if (abs((x) - (x_old))) <= (1):
				return x
			else:
				pass
			
		
	def abs(x):
		pass # no non-local variables
		
		
		if (x) < (0):
			return (0) - (x)
		else:
			return x
		
		
	
	print(sqrt(25735, 8192), end='\n')

main()


# status: {status}
# {message}