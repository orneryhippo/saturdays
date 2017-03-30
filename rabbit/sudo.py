from bitarray import bitarray
# __alfa__ = 'abcdefghijklmnopqrstuvwxyz'
# __ALFA__ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
__alfa__ = "".join(list(map(lambda x: chr(x+ord('a')),range(26))))
__ALFA__ = __alfa__.upper()
__alfarray__ = list(__alfa__)
__ALFARRAY__ = list(__alfa__.upper())


n = 3
n2 = n*n
n3 = n2*n
n4 = n2*n2

rows = []
cols = []

for i in range(n2):
	rb = bitarray(n4)
	rb.setall(0)
	rb[i*n2:n2*(i+1)] = 1
	rows.append(rb)
	cb = bitarray(n4)
	cb.setall(0)
	cb[i:n4:n2] = 1
	cols.append(cb)


grp = []
for i in range(n2):
	grp.append([])

for cell in range(n4):
	r = int(cell/n2)
	c = cell % n2
	g = n * int(r/n) + int(c/n)
	grp[g].append(cell)
	#print(r,c,g)

g = []
for r in range(n2):
	gb = bitarray(n4)
	gb.setall(0)
	for c in range(n2):
		gb[grp[r][c]] = 1
	g.append(gb)


syms = []
for s in range(n2):
	sym = bitarray(n2)
	sym.setall(0)
	sym[n2-s-1]= 1
	syms.append(sym)


symmap = []
for s in range(n2):
	sym = bitarray(n4)
	sym.setall(0)
	symmap.append(sym)


def mk_row_mask(r):
	b = bitarray(n4)
	b.setall(0)
	for i in range(r*n2,r*n2+n2):
		b[i] = 1
	return b


def mk_col_mask(c):
	b = bitarray(n4)
	b.setall(0)
	for i in range(n2):
		b[n2*i+c] = 1
	return b


cm = []
for i in range(n2):
	cm.append(mk_col_mask(i))

cm


def group(r,c):
	return ((r/n)*n2+c)/n

def list_rc_in_g(g):
	"""given a group number, list the (r,c) tuples that comprise it"""
	return [(r,c) for r in range(n2) for c in range(n2) if g == group(r,c)]


# this makes a derangement, but not necessarily a proper on for this use.
# this only guarantees row non-dup and non-match of value to column.
# before one of these can be used, need to check against box and col duplication
# for each row, there is a move w.r.t. the first row which takes each el out of the
# box it starts in
def mk_derangement(n = 10):
	#der = []
	der = n * [-1]
	cand = list(range(n))
	for i in range(n):
		r = randint(0,len(cand)-1)	
		while i == r:
			r = randint(0,len(cand)-1)
		c = cand[r]
		der[i] = c
		cand.remove(c)
	return der



#my initial setup comes as a dict
init = {1:3, 2:8, 3:1,...}
state = init.copy()
whatif = state.copy()

def validate(state):
	""" dict |-> bool
	This predicate function takes a state dict and returns a bool
	which is True if the state is valid and False if it is not valid
	This does not check options, only if the state itself is consistent."""
	return False

def count_options(state):
	""" dict |-> array(int)
	This function takes a state dict and returns an array of the count of
	the available options. If any is zero and there are more locs to be assigned, this is an infeasible state
	"""
	pass

def feasible(options):
	""" array(int) |-> bool
	This predicate function takes an options array and returns True if it is feasible (no zeros) or False if it is not ()
	"""
	pass

# it is part of the game, that there must be no guessing -- all puzzles have one unique solution and all steps
# can be determined purely rationally without resorting to guessing.
# This should not require look-ahead beyond the current move implications.
def r13(c):
	if not c.isalpha():
		return c
	if c.isupper():
		base = ord(__ALFA__[0])
	else:
		base = ord(__alfa__[0])
	b = (ord(c) - base + 13) % 26
	return chr(base + b)

def rot13(s):
	return "".join(list(map(r13, s)))


# minimum possible known is 18, with 17 not theoretically impossible but none known.

#evil 26 entries
evil = {0:8, 5:7, 6:6, 12:3, 14:6, 15:5, 16:2, 19:7, 27:6, 31:4, 33:2, 34:5, 37:5, 43:1, 45:7, 47:2, 49:1, 53:9,
61:3, 64:1, 65:7, 66:6, 68:9, 74:5, 75:8, 80:2} 

#medium 29 entries
med = {7:6, 10:9, 14:6, 17:4, 18:6, 19:5, 21:2, 22:3, 23:8, 27:7, 31:6, 32:4, 35:5, 38:1, 40:9, 42:4, 45:4, 48:1, 49:2, 
53:9, 57:9, 58:7, 59:2, 61:5, 62:8, 63:5, 66:6, 70:2, 73:3}

#easy, 10 extra clues #36 entries
ez = {0:2,1:9, 4:6, 6:4, 9:7, 11:4, 15:5, 21:9, 23:4, 24:8, 26:7, 28:1, 30:6, 31:7, 33:3, 34:8, 38:2, 39:5, 41:3,
42:6, 46:7, 47:3, 49:4, 50:8, 52:5, 54:9, 56:5, 57:4, 59:6, 65:7, 69:1, 71:6, 
74:6, 76:8, 79:9, 80:5 } 

## 
## use AI/ML and big data to produce heuristics
## look at full grid and determine if swaps are possible

#write a generator that produces alphabet strings in order a-z,aa-az,ba-bz,...,za-zz,aaa-aaz,
#equivalent to rendering positive integers in base 26 using only lc alpha symbols in alpha order...

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


# given an array of integers, translate to a string of characters
#def int_arr_to_str(int_arr):
def ia2s(int_arr):
	alfa = 'abcdefghijklmnopqrstuvwxyz'
	s = []
	for n in int_arr:
		s.append(alfa[n])
	return "".join(s)

d = dict(zip('a b c'.split(),))
def string_gen(leng = 2,ctr = 0, base = 26):
	while ctr > -1:
		yield int_arr_to_str(numberToBase(ctr,base))
		ctr += 1
## defect, when rolling over to new decimal place it is skipping 'a'
## going from 9 -> 10 skips [0,0], which was represented as [0]
## if my number generator produced [0], [1], [2], ... [base-1], [0, 0], [0,1]
## it would work
## generate all the len=1 arrays, len=2 arrays, etc.
## for base = 3 it would look like this, up to leng = 2
from itertools import cycle
p = []
for digits in range(leng):
	p.append(cycle(range(base)))
nums = [[0], [1], [2], [0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

# e.g.
s = string_gen() # s is a generator
for i in range(200):
	print(next(s)) # s.__next__()


#using the dist array, produce the proxrank array which has the index to the nth smallest dist for each pt
proxrank=[[self_ndx, nearest_ndx, ndx_2nd, ndx_3rd, ..., ndx_furthest]
		  [self_ndx, nearest_ndx, ndx_2nd, ndx_3rd, ..., ndx_furthest]
		  [self_ndx, nearest_ndx, ndx_2nd, ndx_3rd, ..., ndx_furthest]
		  [self_ndx, nearest_ndx, ndx_2nd, ndx_3rd, ..., ndx_furthest] 
		  ...
		  ]

#indexes for each point to nearest, i.e. prox list
start_ndxs = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1...,1,1,1]

#calc cost of moving each to the next nearest neighbor (from 1 to 2)
costs = [cost(0,1,2), cost(1,1,2), cost(r,current_ndx,current_ndx+1)]
cost_ranks = rank(costs)

#calc how many groups the naive start makes
def mk_rt(prank,ndxs):
	pass
	return []

naive_rt = mk_rt(proxrank,start_ndxs)

def count_groups(rts):
	pass

count_groups(naive_rt)

#search for least-cost way to make a single circuit
#if we change the index with the lowest incremental cost
#have we reduced the number of groups?
#can we analyze the proxrank directly to find a derangement of the original? must avoid short circuits too.
#short circuit e.g. [2,3,1,5,6,4] consists of two subcycles

#at least half the ndxs will need to be 2 or greater to make a circuit, because dupes a->b == b->a
#so theoretical rank limit is closer to 1/s[s/2+2s/2] = 3/2 for symmetric, planar costs/distances

#try to find a derangement from ndx 1s and 2s
#starting with all the first indexes, dupes and cost_ranks


b5XeoL=z=x
