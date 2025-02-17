def main():
	pass # no non-local variables
	disc = None
	
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
		
		
	def calc_disc(a, b, c):
		pass # no non-local variables
		d = None
		
		
		d = ((b) * (b)) + (((4) * (a)) * (c))
		return d
		
	
	disc = calc_disc(2, 3, 2)
	print(disc, end='\n')
	print(sqrt(disc, 1), end='\n')
	print(sqrt(25735, 8192), end='\n')
	

main()


# status: {status}
# {message}