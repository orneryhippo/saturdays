from random import randrange
from datetime import datetime


def rsgn():
	return (2*flip() - 1)

def flip():
	return randrange(2)

def __make_ks(reverse=False):
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


def __make_preds(nvars,pvratio):
	preds = []
	pcount = int(nvars * pvratio)
	for a in range(pcount):
		i = randrange(0,nvars-2) 
		j = randrange(i+1,nvars-1) 
		k = randrange(j+1,nvars) 
		preds.append((i * rsgn(),j * rsgn(),k * rsgn())) 
	return tuple(preds)

def __kspack(ks):
	"""takes a kset and returns an 8-bit number"""
	bits = 0
	_ks = __make_ks()
	for i in range(8):
		if _ks[i] in ks:
			bits += 2**i
	return bits

def __ksunpack(bits):
	"""takes an 8-bit number and returns a kset"""
	ks = []
	_ks = __make_ks()
	for i in range(8):
		if ((bits >> i) & 1) == 1:
			ks.append(_ks[i])
	return ks


def __except_for(mask , pred):
	""" return a tuple that excludes the items where the bits of mask {0..7} are 0
	If mask is 0 then this pred is unsatisfiable under given conditions. 
	Probably should throw an exception under this case.
	"""
	x4 = []
	s,m,l= pred	
	if 4 & mask:
		x4.append(s)
	if 2 & mask:
		x4.append(m)
	if 1 & mask:
		x4.append(l)
	
	return tuple(x4) 


def __masked(pred_id):
	p = __predlist[pred_id]
	m = __masks[pred_id]
	return __except_for(m,p)

## work in progress--new version not assuming pred is len 3
def __vcounts(unsat):
	var_ct = [] 	
	for i in range(__nvars):
		var_ct.append(([],[])) #false list, true list
	
	for i,pred in enumerate(unsat):
		p = []
		for v in __masked(i):
			p.append(int((1+sgn(v))/2))
		
		ks = [p]
		for k in ks:	
			
			masked = __masked(i)
			#print(masked)
			for j in range(len(masked)):		
				#this puts the val of pk in v[a] true or false list based on the value of k[0]
				var_index = abs(masked[j])
				siglist = k[0]
				#print(var_index, siglist,i)
				var_ct[var_index][siglist].append(i) 
	#print(var_ct)
	return tuple(var_ct)


def __calc_anticorrelations(pl):
	ac = [] 
	for row,pr in enumerate(pl):
		rac = [0] * (len(pl)-row-1)
		r1,r2,r3,k = pr
		rk = __ksunpack(k)[0]
		rows = [r1,r2,r3]
		for col in range(row+1,len(pl)):			
			c1,c2,c3,k = pl[col]
			ck = __ksunpack(k)[0]
			cols = [c1,c2,c3]
			idx = ((rows.index(x),cols.index(x)) for x in rows if x in cols)
			for n in idx:
				if rk[n[0]] != ck[n[1]]:
					rac[col-row-1] -= 1
		ac.append(rac)
	return ac



def __reset__(nvars = None, pvratio = None):
	global __nvars, __predlist, __vars, __masks, __TAUT, __BLOCKED, __unsat, __assignments, __anticorrelations
	if nvars:
		__nvars = nvars
	else:
		__nvars = 10

	if pvratio:
		__pvratio = pvratio
	else:
		__pvratio = 3.0

	__TAUT = 2**3
	__BLOCKED = 2**4 - 1
	__assignments = []
	__predlist = __make_preds(__nvars,__pvratio)
	#__anticorrelations = __calc_anticorrelations(__predlist)
	__unsat = list(__predlist)
	__vars = __vcounts(range(__nvars)) # [[None] * __nvars,[None] * __nvars] #false_list, true_list
	__masks = [7] * len(__predlist)



def __findmax(blist):
	maxf = maxt = fidx = tidx = 0
	for i,b in enumerate(blist):
		if len(b[0]) > mf:
			maxf = len(b[0])
			fidx = i
		if len(b[1]) > mt:
			maxt = len(b[1])
			tidx = i
	return fidx,maxf,tidx,maxt



def __findmax(blist):
	maxf = 0
	maxt = 0
	false_ct = 0
	true_ct = 0
	for i,b in enumerate(blist):
		#print(i,b)
		if len(b[0]) > false_ct:
			false_ct = len(b[0])
			maxf = i
		if len(b[1]) > true_ct:
			true_ct = len(b[1])
			maxt = i
	return maxf,false_ct,maxt,true_ct

def __reduce_vars(vars,denied):
	#print(pred,__predlist[pred], denied)
	pass

def __reduce_list(unsat,vsol,short_circuit=False):
	vc = __vcounts(unsat)
	denied = -1
	maxf,false_ct,maxt,true_ct = __findmax(vc) #$
	print(maxf,false_ct,maxt,true_ct)
	if short_circuit and false_ct ==1 and true_ct == 1:
		print("singles")
		return ([],vsol)
	if false_ct > true_ct:		
		dependent_preds = vc[maxf][0]
		denied = maxt
		denied_preds = vc[maxf][1]
		vsol[maxf] = 0
		vc[maxf][0] = vc[maxf][1] = []
	else:
		dependent_preds = vc[maxt][1]
		denied = maxf
		denied_preds = vc[maxt][0]
		vsol[maxt] = 1
		vc[maxt][0] = vc[maxt][1] = []
	for pred in dependent_preds:
		#print(pred)
		if pred in unsat:
			#print("satisifed:",pred)
			unsat.remove(pred)
	for pred in denied_preds:
		if denied in __masked(pred):
			__reduce_vars(pred,denied)
	return unsat,vsol

def __bound(cert):
	for i in cert:
		if None == i:
			return False
	return True

def solve(short_circuit=False):
	vsol = [None] * __nvars
	lpl = len(__predlist)
	lpl0 = 0
	unsat = list(range(len(__predlist)))
	for pred in __predlist:
		#print(vsol)
		unsat,vsol = __reduce_list(unsat,vsol)
		lpl = len(unsat)
		if lpl > 0 and __bound(vsol):
			print("not satisfied. remainder:", unsat)
			return unsat,vsol
		lpl0 = lpl
	return unsat,vsol

def trial(n,p):
	__reset__(n,p)
	return solve()

