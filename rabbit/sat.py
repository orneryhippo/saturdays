# 3SAT test
from random import randrange
import datetime

T = 1
F = 0
S = 2

#predlist = {(0,1,2):0, (0,1,3):0}
#negs = {(0,1,2):255, (0,1,3):255}


def make_ks(reverse=False):
	"""ks are the bits of the ints from 0 to 7, used as truth flags
	for vars in predicates. I.e. 0 means the denial of a var, 0  for var X means notX
	1 for var X means X is true
	"""
	ks = []
	for i in range(2):
		for j in range(2):
			for k in range(2):
				if reverse:
					ks.append((1-i,1-j,1-k))
				else:
					ks.append((i,j,k))
	return ks


def make_preds0(pcount = 100, nvars = 99):
	preds = {}
	for a in range(pcount):
		si = randrange(0,2)*2 - 1
		sj = randrange(0,2)*2 - 1
		sk = randrange(0,2)*2 - 1
		si = sj = sk = 1
		i = randrange(0,nvars-2)
		j = randrange(i+1,nvars-1)
		k = randrange(j+1,nvars)
		preds[(si*i,sj*j,sk*k)] = 255-randrange(0,255)
	return preds



def make_preds(pcount = 100, nvars = 99):
	preds = {}
	for a in range(pcount):
		si = randrange(0,2)*2 - 1
		sj = randrange(0,2)*2 - 1
		sk = randrange(0,2)*2 - 1
		si = sj = sk = 1
		i = randrange(0,nvars-2)
		j = randrange(i+1,nvars-1)
		k = randrange(j+1,nvars)
		preds[(si*i,sj*j,sk*k)] = 2**randrange(8) # 255-randrange(0,255)
	return preds


def make_negs(pcount = 100, nvars = 99):
	negs = {}
	for a in range(pcount):
		i = randrange(0,nvars-1)
		j = randrange(i+1,nvars)
		k = randrange(j+1,nvars+1)
		negs[(i,j,k)] = randrange(0,255)
		#negs[(i,j,k)] = 2**randrange(0,8)
	return negs

def pred2neg(pred):
	#given a predicate, return its negative
	pass


def brute():
	#given a number of variables N and a predicate list PL try all certs of lenght N against all predicates
	cert = (2 ** (N+1)) - 1
	for pred in predlist:
		pass
	return cert

def depcount(var, predlist):
	t = 0
	f = 0
	for pred in predlist:
		for el in pred:
			if el == var:
				t += 1
			elif el == -var:
				f += 1

	return (t,f)


def check_overconst(predlist):
	for pred in predlist:
		if predlist.get(pred) and predlist[pred] < 1:
			return True
	return False


def mk_randcert(nvar = 100):
	cert = []
	for i in range(nvar):
		cert.append(randrange(0,2))
	return cert


def check_cert(cert, neglist, ks):
	for pred in sorted(list(neglist.keys())):
		p0,p1,p2 = pred
		print(pred,neglist[pred])
		mflags = neglist[pred]
		for i in range(8):
			if ((mflags >> i) & 1) == 0:
				next
			else: 				
				k0,k1,k2 = ks[i]
				if not( cert[p0] == k0 and cert[p1] == k1 and cert[p2] == k2):
					print("OK  ",i,cert[p0],cert[p1],cert[p2],ks[i], p0,p1,p2)
					next
				else:
					print("Fail",i,cert[p0],cert[p1],cert[p2],ks[i], p0,p1,p2)
					return False
		print("\n")
	return True


def print_cert(cert):
	for i in range(0,len(cert),20):
		print(cert[i:i+20])


def coverage(predlist):
	cov = []
	for pred in predlist:
		cov.append(pred[0])
		cov.append(pred[1])
		cov.append(pred[2])
	return sorted(set(cov))

# first, make sure that no var triple has more than 2**3 - 1 constraints, else the group of preds is unsat
# count ts and fs from each var
# choose the largest group from the most connected var
# reduce the remaining vars by extracting the already-satisfied preds
# then take the largest group from the remaining vars and repeat

# bottom-up
# trips, reduced to no more than 7 distinct constraints
# then tied to pairs and singles to further reduce. From trips to pairs and singles will add additional
# constraints 

def snippets():
	nvars = 100
	v = []
	for i in range(nvars):
		v.append(set())

	pl = make_negs()
	predlist = list(predlist.keys())
	for i in range(len(predlist)):
		pred = predlist[i]
		for el in pred:
			v[el].add(i)

	m1 = {}
	m2 = {}
	for i in range(256):
		for j in range(256):
			for k in range(1,10):
				m1[(i,j,k)] = match(i,j,k)
				m2[(i,j,k)] = match(i,j,k+10)



	for i in range(256):
		for j in range(256):
			for k in range(1,10):
				print("{0:3d} {1:3d} {2:2d} {3:>2s}     {0:3d} {1:3d} {2:2d} {4:>2s}".format(i,j,k,["T","F"][match(i,j,k)],["T","F"][match(i,j,k+10)]))


def t1():
	t = list(range(8)) #satisfiers
	s = [] #predicate constraints
	k = [] #incompatibles
	for i in range(7):
		s.append(randrange(0,8))
	s = set(s)
	print("Constraints\t", list(s))
	for el in s:
		t.remove(7-el)
		k.append(7-el)

	print("Incompatible\t", k)
	print("Compatible\t"	,t)

def mk_randpred():
	s = [] #predicate constraints
	for i in range(7):
		s.append(randrange(0,8))
	s = set(s)
	return list(s)
	
def g(n):
	if n < 1 or n > 6:
		raise OutOfBoundsException
	elif n == 1:
		_g = ([x] for x in range(8))
	elif n == 2:
		_g = ([x, y] for x in range(8) for y in range(8) if x != y)
	elif n == 3:
		_g = ([x,y,z] for x in range(8) for y in range(8) for z in range(8) if x != y and y != z and x != z)
	elif n == 4:
		_g = ([w, x,y,z] for w in range(8) for x in range(8) for y in range(8) for z in range(8) if w != x and w != y and w != z 
			and x != y and y != z and x != z)
	elif n == 5:
		_g = ([v, w, x,y,z] for v in range(8) for w in range(8) for x in range(8) for y in range(8) for z in range(8) 
			if w != x and w != y and w != z and x != y and y != z and x != z and v != w and v != x and v != y and v != z)
	elif n == 6:
		_g = ([u,v, w, x,y,z] for u in range(8) for v in range(8) for w in range(8) for x in range(8) for y in range(8) for z in range(8) 
			if w != x and w != y and w != z and x != y and y != z and x != z and v != w and v != x and v != y and v != z
			and u != v and u != w and u != x and u != y and u != z)
	return _g

def g2(n):
	if n < 1 or n > 6:
		raise OutOfBoundsException
	elif n == 1:
		_g = ([x] for x in range(8))
	elif n == 2:
		_g = ([x, y] for x in range(8) for y in range(8) if x < y)
	elif n == 3:
		_g = ([x,y,z] for x in range(8) for y in range(8) for z in range(8) if x < y and y < z )
	elif n == 4:
		_g = ([w, x,y,z] for w in range(8) for x in range(8) for y in range(8) for z in range(8) if w < x and x < y and y < z)
	elif n == 5:
		_g = ([v, w, x,y,z] for v in range(8) for w in range(8) for x in range(8) for y in range(8) for z in range(8) 
			if v < w and w < x and x < y and y < z)
	elif n == 6:
		_g = ([u,v, w, x,y,z] for u in range(8) for v in range(8) for w in range(8) for x in range(8) for y in range(8) for z in range(8) 
			if u < v and v < w and w < x and x < y and y < z)
	return _g

def compat(constraints):
	c = list(range(8))
	for el in constraints:
		c.remove(7-el)
	assert(len(c)>0)
	return c


def _validate(cpart,pred):
	a,b,c = cpart
	d,e,f = list(pred.keys())
	return ((a == d) or (b == e) or (c == f))

def kspack(ks):
	"""takes a kset and returns an 8-bit number"""
	bits = 0
	_ks = make_ks()
	for i in range(8):
		if _ks[i] in ks:
			bits += 2**i
	return bits

def ksunpack(bits):
	"""takes an 8-bit number and returns a kset"""
	ks = []
	_ks = make_ks()
	for i in range(8):
		if ((bits >> i) & 1) == 1:
			ks.append(_ks[i])
	return ks

def _match1(a, b, p1, p2):
	return (((a >> p1) & 1) == ((b >> p2) & 1))

def _match2(a,b, p11, p12, p21, p22):
	#return ((((a >> p11) & 1) == ((b >> p21) & 1)) and (((a >> p12) & 1) == ((b >> p22) & 1)))
	return _match1(a,b, p11,p21) and _match(a,b,p12,p22)

def match(a, b, p):
	# 18 partial match possibilities
	if ((p < 1) or (p == 10) or (p > 19)):
		raise AssertionError #"{1} must be 1-9 or 11-19".format(p)

	if p == 1:
		return _match1(a,b,0,0)
	elif p == 2:
		return _match1(a,b,0,1)
	elif p == 3:
		return _match1(a,b,0,2)
	elif p == 4:
		return _match1(a,b,1,0)
	elif p == 5:
		return _match1(a,b,1,1)
	elif p == 6:
		return _match1(a,b,1,2)
	elif p == 7:
		return _match1(a,b,2,0)
	elif p == 8:
		return _match1(a,b,2,1)
	elif p == 9:
		return _match1(a,b,2,2)

	elif p == 11:
		return _match2(a,b,0,0,1,1)
	elif p == 12:
		return _match2(a,b,0,0,1,2)
	elif p == 13:
		return _match2(a,b,0,0,2,1)
	elif p == 14:
		return _match2(a,b,0,0,2,2)
	elif p == 15:
		return _match2(a,b,1,0,2,1)
	elif p == 16:
		return _match2(a,b,1,0,2,2)
	elif p == 17:
		return _match2(a,b,0,1,2,1)
	elif p == 18:
		return _match2(a,b,0,1,2,2)
	elif p == 19:
		return _match2(a,b,1,1,2,2)

def consolidate3(preds):
	# given a list of trips, consolidate the bitflags
	# flags should be all 1s except 0 for the 1 at a power of 2 which corresponds to a predicate in ks
	bf = 0
	for f in list(preds.values()):
		assert((f == 1) or (f == 2) or (f == 4) or (f == 8) or (f == 16) or (f == 32) or (f == 64) or (f == 128))
		if (0 == (bf & f)): #ignore redundants
			f = 0
		bf += f
		assert(bf < 255) # this would be unsatisfiable for a single predicate
	return bf



def reduce3(predlist):
	trips = {}
	for pred in predlist:
		a,b,c = pred
		if trips.get((a,b,c)):
			trips[(a,b)].append(pred)
		else:
			trips[(a,b,c)] = [pred]
		
	return trips


def reduce2(predlist):
	pairs = {}
	for pred in predlist:
		a,b,c = pred
		if pairs.get((a,b)):
			pairs[(a,b)].append(pred)
		else:
			pairs[(a,c)] = [pred]
		if pairs.get((a,c)):
			pairs[(a,c)].append(pred)
		else:
			pairs[(a,c)] = [pred]
		if pairs.get((b,c)):
			pairs[(b,c)].append(pred)
		else:
			pairs[(b,c)] = [pred]
	return pairs

def reduce1(predlist):
	singles = {}
	for pred in predlist:
		a,b,c = pred
		if singles.get((a)):
			singles[(a)].append(pred)
		else:
			singles[(a)] = [pred]
		if singles.get((b)):
			singles[(b)].append(pred)
		else:
			singles[(b)] = [pred]
		if singles.get((c)):
			singles[(c)].append(pred)
		else:
			singles[(c)] = [pred]
	return singles


def bitrev(bits):
	stib = 0
	for i in range(8):
		if bits & 2**i > 0:
			stib += 2**(7-i)
	return stib

def revinv(nflags):
	flag = 255 ^ nflags
	return bitrev(flag)




def red(a,b,p):
	ka = ksunpack(a)
	kb = ksunpack(b)
	reda = []
	redb = []
	for ela in ka:
		for elb in kb:
			if match(ela,elb,p):
				reda.append(ela)
				redb.append(elb)
	return kspack(reda), kspack(redb)

def summarize(ks):
	a0,b0,c0 = ks[0]
	res = [a0,b0,c0]	
	for el in ks[1:]:
		a,b,c = el
		if a != a0:
			res[0] = 2
		if b != b0:
			res[1] = 2
		if c != c0:
			res[2] = 2
	return res[0],res[1],res[2]

def nonslack(vlist):
	pivot = 0
	nonslacks = [] # list(range(len(vlist)))
	slack = ([],[])
	if vlist.count(slack) > 0:
		for i in range(len(vlist)):
			if vlist[i] != slack:
				nonslacks.append(i)				
	return nonslacks

def vcounts(predlist,nvpars):
	var_ct = [] 
	for i in range(nvpars):
		var_ct.append(([],[])) #false list, true list
	pk = list(predlist.keys())
	for i,val in enumerate(pk):
		small,med,large = val
		#print(i,a,b,c)
		k = ksunpack(predlist[val]) # this may lead to redundancy, but it's already in place. If desired, make the predlist simply 2**x values
		for pred in k:
			#print(pred)
			#pred is a triple-bool e.g. (0,1,0)

			var_ct[small][pred[0]].append(val) #this puts the val of pk in v[a] true or false list based on the value of pred[0]
			var_ct[med][pred[1]].append(val)
			var_ct[large][pred[2]].append(val)
	return var_ct

def print_v(vlist, ct=False):
	"""given a list of vars, print the trues and falses
	"""
	for i,v in enumerate(vlist):
		vs = sorted(v)
		eps=0.0000001

		vt = len(v[1])+eps
		vf = len(v[0])+eps
		pr = vf/(vf+vt)
		#print(pr)
		if ct:
			print("var: {2:4d}\ntrue:  {0}\nfalse: {1}\nprob:  {3}\n".format(vt,vf,i,pr))
		else:
			print("var: {2:4d}\ntrue:  {0}\nfalse: {1}\nprob:  {3}\n".format(sorted(v[1]),sorted(v[0]),i,pr))
		

def check_cert(cert, plist):
	proof = []
	fails = []
	for i,pred in enumerate(plist):
		small, med, large = pred
		kset = ksunpack(plist[pred])
		for j,k in enumerate(kset):
			if cert[small] == 2 or k[0] == cert[small]:
				proof.append(i)
				continue
			if cert[med] == 2 or k[1] == cert[med]:
				proof.append(i)
				continue
			if cert[large] == 2 or k[2] == cert[large]:
				proof.append(i)
				continue
			fails.append(i)
	if len(proof)<len(plist):
		print("failed:",fails)
		return fails

	return []

def cert_gen(nvars=8):
	v = [0] * nvars
	#yield v
	while (v != [1]*nvars):
		for i in range(nvars):
			if v[-i] == 0:
				v[-i] = 1
				break
			else:
				v[-i] = 0
		yield v


def brute_check(ps,nvars = 8):
	for c in cert_gen(nvars):
		if check_cert(c,ps):
			print(c)
			for i,p in enumerate(ps):
				print(p,ksunpack(ps[p]))
			return c
	print('unsat')
	return False



def merge_ps(ps1,ps2):
	trips = ps1
	for i,p in enumerate(ps2):
		if(trips.get(p)):
			trips[p] |= ps2[p]
			assert(trips[p] < 255)
		else:
			trips[p] = ps2[p]
	return trips


def splitsort(vct,ps):
	p_ct = len(ps)
	mx_t = 0
	mx_f = 0
	t_idx = 0
	f_idx = 0
	for i,falsies in enumerate(vct[0]):
		if mx_f < falsies:
			mx_f = falsies
			f_idx = i
	for i,trulies in enumerate(vct[1]):
		if mx_t < trulies:
			mx_t = trulies
			t_idx = i
	return t_idx, vct[1][t_idx], f_idx, vct[0][f_idx]


def findmax(blist):
	mf = 0
	mt = 0
	fi = 0
	ti = 0
	for i,b in enumerate(blist):
		if len(b[0]) > mf:
			mf = len(b[0])
			fi = i
		if len(b[1]) > mt:
			mt = len(b[1])
			ti = i
	
	#print(fi,mf,ti,mt)
	return fi,mf,ti,mt

def remslack(vlist):
	v = vlist[:]
	for i in range((v.count(([],[])))):
		v.remove(([],[]))
	return v

def nonslack(vlist):
	pivot = 0
	nonslacks = [] # list(range(len(vlist)))
	slack = ([],[])
	if vlist.count(slack) > 0:
		for i in range(len(vlist)):
			if vlist[i] != slack:
				nonslacks.append(i)				
	return nonslacks

def redlist(pl,nvars,vsol,short_circuit=False):
	pc = pl.copy()
	vsat=[]
	vc = vcounts(pl, nvars)
	mf,fc,mt,tc = findmax(vc)
	if short_circuit and fc ==1 and tc == 1:
		print("singles")
		return {},vsol
	if fc > tc:		
		print("vsol {0} is false".format(mf))
		k = vc[mf][0]
		vsol[mf] = 0
	else:
		print("vsol {0} is true".format(mt))
		k = vc[mt][1]
		vsol[mt] = 1
	#print(k)
	for p in k:

		pc.pop(p)
	return pc,vsol

def solve(pl, nvars,unsat, short_circuit=False):
	vsol = [2]* (nvars)
	
	lpl0 = len(pl) - 1
	for i in range(len(pl)):
		lpl = len(pl)
		#each time redlist is called, pl is reduced and vsol is updated
		#print(lpl)
		pl,vsol = redlist(pl, nvars,vsol,short_circuit)
		if lpl == lpl0 and lpl > 0:
			print("not satisfied. remainder:", pl)
			return False
		lpl0 = lpl
		if lpl == 0:
			#print(vsol)
			return vsol,unsat

def multitrials(trials=20, vstep=100, pratio=20, show_cert=False,short_circuit=False):
	for i in range(1,trials+1):
		v = vstep*i
		p = pratio*v
		unsat = None
		trial(p,v,unsat,show_cert,short_circuit)


def check_bit(pl,offset):
	for i,k in enumerate(pl):
		if offset in k:
			print(k, ksunpack(pm[k]))

def trial(npred,nvars, unsat=None, show_cert=False,short_circuit=False):
	if unsat == None:
		unsat = []
	st = datetime.datetime.now()
	pm = make_preds(npred,nvars)
	md = datetime.datetime.now()
	v,u = solve(pm,nvars,unsat, short_circuit)
	if len(u) < 1:
		proof = check_cert(v,pm)
	else:
		show_fails(v,pm)
	if len(proof)>0:
		show_fails(proof,v,pm)
			
	fin = datetime.datetime.now()
	print("number of variables: ", nvars)
	print("number of predicates: ", len(pm))
	print("elapsed time to solve: {0}\n".format(fin-md))
	return pm,v


def unsat(pl,cert):
	pm = pl.copy()
	for p in pm:
		k = ksunpack(pm[p])
		for i in range(3):
			if cert[p[i]] == k[i]:
				if pm.get(p):
					pm.remove(p)
				break



def cur(num,sym="$",isep=",",fsep="."):
	nums = str(num).split(".")
	snum = nums[0]
	if len(nums) == 2:
		fnum = nums[1]
		if len(fnum) == 1:
			fnum += "0"
	else:
		fsep = fnum = ""

	p = []
	d,m = divmod(len(snum),3)
	p.append(snum[:m])
	for i in range(m,len(snum),3):
		p.append(snum[i:i+3])

	if "" in p:
		p.remove('')
	
	return sym + isep.join(p) + fsep + fnum
	

def proc(cert,v):
	for i,c in enumerate(cert):
		if 2 == c:
			continue
		else:
			if v[i] == c:
				print(i,c)


def show_fails(fails, cert, plist):
	for i,p in enumerate(plist):
		if p in fails:			
			print(i,p,ksunpack(plist[p]),cert[p[0]],cert[p[1]],cert[p[2]])


def print_p(plist):
	for i,p in enumerate(plist):
		print(p,ksunpack(plist[p]))


def check_cert(cert,plist):
	fails = []
	for i,p in enumerate(plist):
		s,m,l = p
		ks = ksunpack(plist[p])
		for k in ks:
			sk,mk,lk = k
			incomp = (1-sk,1-mk,1-lk)
			if cert[s] == incomp[0] and cert[m] == incomp[1] and cert[l] == incomp[2]:
				fails.append(p)
	return fails