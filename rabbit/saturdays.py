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

## work in progress--new version not assuming pred is len 3
def __vcounts(predlist):
	var_ct = [] 
	trues = []
	falses = []
	for i in range(__nvars):
		var_ct.append(([],[])) #false list, true list
	
	for i,pred in enumerate(predlist):
		p = []
		for v in pred:
			p.append(int((1+sgn(v))/2))
		
		ks = [p]
		#print(i,a,b,c)
		#ks = __ksunpack(pred[3]) # this may lead to redundancy, but it's already in place. If desired, make the predlist simply 2**x values
		for k in ks:	
			for j in range(len(p)):		
				var_ct[abs(p[j])][k[0]].append(tuple(pred)) #this puts the val of pk in v[a] true or false list based on the value of k[0]
	return tuple(var_ct)

def __vcounts(predlist):
	var_ct = [] 
	trues = []
	falses = []
	for i in range(__nvars):
		var_ct.append(([],[])) #false list, true list
	
	for i,pred in enumerate(predlist):
		small,med,large = pred
		ks = [[int((1+sgn(small))/2),int((1+sgn(med))/2),int((1+sgn(large))/2)]]
		#print(i,a,b,c)
		#ks = __ksunpack(pred[3]) # this may lead to redundancy, but it's already in place. If desired, make the predlist simply 2**x values
		for k in ks:			
			var_ct[abs(small)][k[0]].append(tuple(pred)) #this puts the val of pk in v[a] true or false list based on the value of k[0]
			var_ct[abs(med)][k[1]].append(tuple(pred))
			var_ct[abs(large)][k[2]].append(tuple(pred))

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
		__nvars = 100

	if pvratio:
		__pvratio = pvratio
	else:
		__pvratio = 3.0

	__TAUT = 2**3
	__BLOCKED = 2**4 - 1
	__assignments = []
	__predlist = __make_preds(__nvars,__pvratio)
	__anticorrelations = __calc_anticorrelations(__predlist)
	__unsat = list(__predlist)
	__vars = __vcounts(__predlist) # [[None] * __nvars,[None] * __nvars] #false_list, true_list
	__masks = [0] * len(__predlist)



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


def __reduce_list():
	""" rewrite this with __masks and __assignments
	pc = pl.copy()
	vsat=[]
	vc = vcounts(pl, nvars)
	mf,fc,mt,tc = findmax(vc)
	if short_circuit and fc ==1 and tc == 1:
		print("singles")
		return {},vsol
	if fc > tc:		
		k = vc[mf][0]
		vsol[mf] = 0
	else:
		k = vc[mt][1]
		vsol[mt] = 1
	for p in k:
		pc.pop(p)
	return pc,vsol
	"""
	# for pred in predlist:
	# 
	pass

def except_for(mask , pred):
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
