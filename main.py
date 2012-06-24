import sys

BUFFER 		   = [int(i) for i in '0' * 3000] 
ip			   =  0 # stands for instruction pointer

# API


def inc_p():
	global ip
	global  BUFFER
	ip += 1
	
def dec_p():
	global ip
	global BUFFER
	ip -= 1

def inc_b():
	global ip
	global BUFFER
	BUFFER[ip] += 1

def dec_b():
	global ip
	global BUFFER
	BUFFER[ip] -= 1

def out_b():
	global ip
	global BUFFER
	sys.stdout.write(chr(BUFFER[ip]))
	#print BUFFER[ip]
def inp_b():
	global ip
	global BUFFER
	BUFFER[ip] = getchar()

def loop(code):
	global ip
	global BUFFER
	#print '---In loop---'
	while BUFFER[ip] != 0:
	#	print '-> In loop loop', BUFFER[:5], code
		eval_brainfuck(code)

legal_commands = {'>' : inc_p,
  				  '<' : dec_p,
				  '+' : inc_b,
				  '-' : dec_b,
				  '.' : out_b,
				  ',' : inp_b,
				  '[' : loop }
				 # ']' => loop] we will never get to '[' according to the design of the API

def getchar():
	return ord(raw_input()[0])

def no_of_occurences(code, c):
	depth = 0
	a = code.find(c)
	while a != -1:
		#print a
		a = code.find(c, a+1)
		depth += 1
	return depth

def skip_occurences(code, a, times):
	c = -1
	while times > 0:
		c = code.find(a, c+1)
		if c == -1:
			return -1
		times -= 1
	return c

# Note: The code gets really ugly from this point. User discretion is advised

def eval_brainfuck(code):
	if not isinstance(code, str):
		return -1
	else:
		c = 0 # loop counter
		while c < len(code):
			#print code[c], c
			if code[c] in legal_commands:
				if code[c] == '[':
					a = 0 # another loop counter
					depth = 0 # depth of the loop
					# let us check that there are no loops i.e '[' inside this loop block					
					end_loop = code.find(']', c)
					if end_loop == -1:
						return -1
					depth = no_of_occurences(code[c+1:end_loop], '[')
					#print depth, code[c+1:end_loop]
					# now we know the depth of this loop lets now figure out the ending point
					if depth > 0:
						rel_c = skip_occurences(code[c+1:], ']', depth)
						a 	  = rel_c + len(code[:c+1]) 
						b = code.find(']', a+1)
						if b == -1:
							return -1
						else:
							depth = no_of_occurences(code[a+1:b], '[')
							if depth > 0:
								# We got more loops inside the parent loop
								rel_a = skip_occurences(code[a+1:], ']', depth) # this position is relative to a+1 we want it withit relative to c+1
								a 	  = rel_a + a 
								b = code.find(']', a+1)
								if b == -1:
									return -1
							end_loop = b
					#		print code[c:end_loop]
					#		print c, b, a, depth
					#print 'Calling Loop =>' , ip, code[c+1:end_loop], BUFFER[0:5]
					loop(code[c+1:end_loop])
					#print '\n\n----loop ends----\n\n'
					c = end_loop
				else:
					legal_commands[code[c]]()
			c += 1

eval_brainfuck(raw_input())