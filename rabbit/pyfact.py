from __future__ import print_function

import math

def bar(y,z):
	return 0 == ((6*y*z + y + z) % 35)


def bar(y, z, ysgn = 1, zsgn = -1):
	return 0 == ((6*y*z + ysgn*y + zsgn*z) % 35)


def foo(ysgn,zsgn):
	for y in range(35):
		for z in range(35):
			if bar(y,z,ysgn,zsgn):
				yield y,z, (-1*(y*ysgn + z*zsgn-3))%6


def foo2(ysgn,zsgn):
	for y in range(35):
		for z in range(35):
			if bar(y,z,ysgn,zsgn):
				yield y,z, y%6, z%6, (-1*(y*ysgn + z*zsgn-3))%6


class IterContainer(object):

	def __init__(self, **params):
		self.params = **params

	def __iter__(self):
		with open(self.params) as foo:
			pass
			yield 


def factor(n):
	if 0 == (n % 2):
		return(2)
	if 0 == (n % 3):
		return(3)
	for i in range(5, int(math.sqrt(n)+1), 2):
		if 0 == n % i:
			return i
	return 1

def countem(r):
	count = 0
	for i in range(1,r):
		n = 35*i
		f1,f2 = (factor(6*n-1),factor(6*n+1))
		if f1==f2==1:
			count += 1
	return count


def listem(r):
	for i in range(1,r):
		n = 35*i
		f1,f2 = (factor(6*n-1),factor(6*n+1))
		if f1==f2==1:
			print(i)

def factorlist(n):
	f = []
	if 0 == (n % 2):
		f.append(2)
	if 0 == (n % 3):
		f.append(3)
	for i in range(5, n, 2):
		if 0 == n % i:
			f.append(i)
	return f


def foo(n):
	fs = []
	if 0 == (n % 2):
		fs.append(2)
		fs.append(int(n / 2))

	if 0 == (n % 3):
		fs.append(3)
		fs.append(int(n / 3))

	for i in range(5,int(math.sqrt(n))+1,2):
		if 0 == (n % i):
			fs.append(i)
			fs.append(int(n / i))

	return sorted(fs)






def foo(r,v=3):
	for i in range(1,r):
		n = 35*(6*i+v)
		f1,f2 = (factor(6*n-1),factor(6*n+1))
		if f1==f2==1:
			print(6*i+v,f1,f2,((f1+f2-v) % 6))


def foo2(r,v=3):
	for i in range(1,r):
		n = 35*(6*i+v)
		f1,f2 = (factor(6*n-1),factor(6*n+1))
		if f1 > 1:
			print(-1, 6*n-1, (6*n-1)/f1,f1, (f1+(6*n-1)/f1 - v) % 6)
		if f2 > 1:
			print(1, 6*n+1, (6*n+1)/f2,f2, (f2-(6*n+1)/f2 - v) % 6)
		


35x + m = 6yz + y + z
35x + m = 6yz - y - z
35x + m = 6yz - y + z
35x + m = 6yz + y - z

for x in range(100):
	n = 35*x
	for z in range(1,int(n/6)):
		if 0 == (n-z) % (6*z+1):
			y = (n-z)/(6*z+1)
			x1 = x % 6
			y1 = y % 6
			z1 = z % 6
			s = (z1+y1+x1)%6
			if 0 != s:
				print(n,x, x1, z, z1, y, y1, s)

		if 0 == (n+z) % (6*z-1):
			y = (n+z)/(6*z-1)
			x1 = x % 6
			y1 = y % 6
			z1 = z % 6
			s = (z1+y1-x1)%6
			if 0 != s:
				print(n,x, x1, z, z1, y, y1, s)


for x in range(100):
	n = 35*x
	for z in range(1,int(n/6)):
		if 0 == (n-z) % (6*z-1):
			y = (n-z)/(6*z-1)
			x1 = x % 6
			y1 = y % 6
			z1 = z % 6
			s = (-z1+y1-x1)%6
			if 0 != s:
				print(n,x, x1, z, z1, y, y1, s)
		if 0 == (n+z) % (6*z+1):
			y = (n+z)/(6*z+1)
			x1 = x % 6
			y1 = y % 6
			z1 = z % 6
			s = (z1-y1-x1)%6
			if 0 != s:
				print(n,x, x1, z, z1, y, y1, s)


def foo2(r,m=0,min=1):
	for x in range(min,r):
		n = 35*x+m
		for z in range(1,int(math.sqrt(n/6)+1)):
			if 0 == (n-z) % (6*z+1):
				y = (n-z)/(6*z+1)
				x1 = x % 6
				y1 = y % 6
				z1 = z % 6
				s = (z1+y1+x1)%6
				print('++',x,m,n,z,y,"{0}+{1}+{2}::{3}".format(z1,y1,x1,s))
			if 0 == (n+z) % (6*z-1):
				y = (n+z)/(6*z-1)
				x1 = x % 6
				y1 = y % 6
				z1 = z % 6
				s = (z1+y1-x1)%6
				print('--',x,m,n,z,y,"{0}+{1}-{2}::{3}".format(z1,y1,x1,s))
			if 0 == (n-z) % (6*z-1):
				y = (n-z)/(6*z-1)
				x1 = x % 6
				y1 = y % 6
				z1 = z % 6
				s = (-z1+y1-x1)%6
				print('+-',x,m,n,z,y,"-{0}+{1}-{2}::{3}".format(z1,y1,x1,s))
			if 0 == (n+z) % (6*z+1):
				y = (n+z)/(6*z+1)
				x1 = x % 6
				y1 = y % 6
				z1 = z % 6
				s = (z1-y1-x1)%6
				print('-+',x,m,n,z,y,"{0}-{1}-{2}::{3}".format(z1,y1,x1,s))



given x and m return 
n,z,y,cheklist



def fac(x,m,typ=0):
	n = 35*x + m
	for z in range(1,int(math.sqrt(n/6)+1)):
		pass

def fac0(x, m,sgn0=1,sgn1=1):
	"""Returns a function"""
	n = 35*x + m
	return lambda z: (n + sgn0 * z) % (6*z + sgn1)



def rat0(x, m,sgn0=1,sgn1=1):
	n = 35*x + m
	return lambda z: (n + sgn0 * z) /  float(6*z + sgn1)


def rat1(x, m,sgn0=1,sgn1=1):
	n = 35*x + m
	return lambda z: divmod((n + sgn0 * z) ,  (6*z + sgn1))

def foo22(r,m=0):
	for x in range(r):
		n = 35 * x + m
		t11 = rat1(x,m)
			
def foo21(r,m=0):
	for x in range(r):
		n = 35*x+m
		for z in range(1,int(math.sqrt(n/6))):
			if 0 == (n-z) % (6*z+1):
				y = (n-z)/(6*z+1)
				x1 = x % 6
				y1 = y % 6
				z1 = z % 6
				s = (z1+y1+x1)%6
				print(x,m,x1,y1,z1)
			if 0 == (n+z) % (6*z-1):
				y = (n+z)/(6*z-1)
				x1 = x % 6
				y1 = y % 6
				z1 = z % 6
				s = (z1+y1-x1)%6
				print(x,m,x1,y1,z1)
			if 0 == (n-z) % (6*z-1):
				y = (n-z)/(6*z-1)
				x1 = x % 6
				y1 = y % 6
				z1 = z % 6
				s = (-z1+y1-x1)%6
				print(x,m,x1,y1,z1)
			if 0 == (n+z) % (6*z+1):
				y = (n+z)/(6*z+1)
				x1 = x % 6
				y1 = y % 6
				z1 = z % 6
				s = (z1-y1-x1)%6
				print(x,m,x1,y1,z1)
				

#========refactored:
def typ2str(typ):
	ch = ['++','--','+-','-+']
	return ch[typ]


def s_func(typ=0):
	fun =[  lambda x,y,z: (z+y+x) % 6,
			lambda x,y,z: (z+y-x) % 6,
			lambda x,y,z: (-z+y-x) % 6,
			lambda x,y,z: (z-y-x) % 6]
	return fun[typ]


def cheklist(x,y,z,typ=0):
	formulae = ["{0}+{1}+{2}::{3}", "{0}+{1}-{2}::{3}", "-{0}+{1}-{2}::{3}", "{0}-{1}-{2}::{3}"]
	x1 = x % 6
	y1 = y % 6
	z1 = z % 6	
	return formulae[typ].format(z1,y1,x1,s_func(typ)(x,y,z))
	

def report(rem,x,y,z,n):
	if 0 == rem:
		print(x,y,z,cheklist(x,y,z,n))

def nums(n,z):
	return [n + z, n - z]

def denoms(z):
	return [6 * z - 1, 6 * z + 1]

def list_ntp(r,m=0):
	for x in range(r):
		n = 35*x+m
		for z in range(1,int(math.sqrt(n/6))):
			y,rem = divmod((n-z),(6*z+1))
			report(rem,x,y,z,0)

			y,rem = divmod((n+z),(6*z-1))
			report(rem,x,y,z,1)

			y,rem = divmod((n+z),(6*z+1))
			report(rem,x,y,z,2)

			y,rem = divmod((n-z),(6*z-1))
			report(rem,x,y,z,3)

#====================

def showall(r, m = 0):
	for x in range(r):
		n = 35*x + m
		for z in range(1,int(math.sqrt(n/6))):
			a = (n-z)
			b = (6*z-1)
			y=a/b
			print( divmod(a,b),x,n,z,a,b,a%6,x%6,y%6,z%6)


def showf(r, m = 0):
	for x in range(r):
		n = 35*x + m
		for z in range(1,int(math.sqrt(n/6))):
			a = (n-z)
			b = (6*z-1)
			y=a/b
			if 0 == a % b:
				print( divmod(a,b),x,n,z,a,b,a%6,x%6,y%6,z%6)

#def r15():
#	for i in range(35):
#		if 1 != i % 5 and 4 != i % 5 and 1 != i % 7 and 6 != i % 7:
#			print(i)

r15 = [0,2,3,5,7,10,12,17,18,23,25,28,30,32,33]
r51 = [0,-2,-3,-5,-7,-10,-12,-17,-18,-23,-25,-28,-30,-32,-33]

def tp_seeds(r,m=0):
	for x in range(1,r):
		n = 35*x + m
		f1 = factor(6*n-1)
		f2 = factor(6*n+1)
		if f1==f2==1:
			print(x,n,6*n-1,6*n+1)


def tp_seedx(r,m=0):
	for x in range(1,r):
		n = 210*x + 3
		f1 = factor(6*n-1)
		f2 = factor(6*n+1)
		if f1==f2==1:
			print(x,n,6*n-1,6*n+1)

def showfx(r, m = 0):
	for x in range(r):
		n = 210*x + 3
		for z in range(1,int(math.sqrt(n/6))):
			a = (n-z)
			b = (6*z-1)
			if 0 == a % b:
				y = a / b
				print(n,x,y,z)
				print( divmod(a,b),x,n,z,a,b,a%6,x%6,y%6,z%6)


def showfx(r, m = 0):
	for x in range(r):
		n = 210*x + m
		lesser = factor(6*n-1)
		if(1 == factor(6*n + 1) and 1 != lesser and m == x % 35):
			print(6*n-1, n,x,x%35,lesser%35,((6*n-1)/lesser)%35)

			
def foo(r1,r2,m=0):
	for x in range(r1,r2):
		n = 35 * 35 * x
		f1 = factor(6*n-1)
		f2 = factor(6*n+1)
		if(1 != f1 or 1 != f2):
			print(n, f1, f2, ((6*n-1)/f1) % 35,((6*n+1)/f2) % 35, f1%35, f2%35)
	


def chk_circuit(g,v):
	while(len(g) > 0):
		p = g.pop()
		if p in v:
			#print(p,v)
			print(len(v)+1)
			return False
		else:
			#print(p,v)
			v.append(p)
	return True

def test_circ(n=10):
	g = [randint(1,n)] + [x for x in range(n)]
	print(g)
	shuffle(g)
	print(chk_circuit(g,[]))




json.dump(
		obj, 
		fp, 
		skipkeys=False, 
		ensure_ascii=True, 
		check_circular=True, 
		allow_nan=True, 
		cls=None, 
		indent=None, 
		separators=None, 
		default=None, 
		sort_keys=False, 
		**kw )

json.dumps(
		obj, 
		skipkeys=False, 
		ensure_ascii=True, 
		check_circular=True, 
		allow_nan=True, 
		cls=None, 
		indent=None, 
		separators=None, 
		default=None, 
		sort_keys=False, 
		**kw )

json.load(
		fp, 
		cls=None, 
		object_hook=None, 
		parse_float=None, 
		parse_int=None, 
		parse_constant=None, 
		object_pairs_hook=None, 
		**kw )

json.loads(
		s, 
		encoding=None, 
		cls=None, 
		object_hook=None, 
		parse_float=None, 
		parse_int=None, 
		parse_constant=None, 
		object_pairs_hook=None, 
		**kw )

class json.JSONDecoder(
		object_hook=None, 
		parse_float=None, 
		parse_int=None, 
		parse_constant=None, 
		strict=True, 
		object_pairs_hook=None )



Simple JSON decoder.

step
on no
pets

