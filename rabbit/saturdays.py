from random import randrange
from datetime import datetime
from math import pi

class vmeta():
	from math import pi

	def __init__(self):
		self.truthval = None
		self.trues = []
		self.falses = []
		self.tct = 0
		self.fct = 0

	def truth(self, v = None):
		if None == v:
			return self.truthval
		else:
			if self.truthval == None:
				self.truthval = v
			else:
				raise RuntimeError("Can't change truthvalue from {0} to {1}".format(self.truthval,v))

	def clear(self):
		self.__init__()

	def mag(self):
		t = self.tc()
		f = self.fc()
		return (t+f)

	def theta(self):
		return pi * self.bayes()

	def bayes(self):
		t = self.tc()
		m = self.mag()
		return (t/float(m))

	def tc(self):
		if self.trues:
			return self.tct
		else:
			return 0

	def fc(self):
		if self.falses:
			return self.fct
		else:
			return 0

	def _add_trues(self,predlist):		
		for p in predlist:
			self.trues.append(p)
			self.tct += 1

	def _rem_trues(self, predlist):
		for p in predlist:
			if p in self.trues:
				self.trues.remove(p)
				self.tct -= 1
	
	def _add_falses(self,predlist):
		for p in predlist:
			self.falses.append(p)
			self.fct += 1

	def _rem_falses(self,predlist):
		for p in predlist:
			if p in self.falses:
				self.falses.remove(p)
				self.fct -= 1

	def add(self, which, predlist):
		if type(predlist) != list:
			pl = [predlist]
		else:
			pl = predlist
		if which:
			self._add_trues(pl)
		else:
			self._add_falses(pl)

	def remove(self, which, predlist):
		if type(predlist) != list:
			pl = [predlist]
		else:
			pl = predlist
		if which:
			self._rem_trues(pl)
		else:
			self._rem_falses(pl)
			

	def get(self,which=None):
		if None == which:
			return (self.trues,self.falses)
		elif True == which:
			return self.trues
		else:
			return self.falses


def testv():
	v = vmeta()	
	v.add(True, [1,2,3])
	v.add(False, [7,8,9,10])
	v.remove(True,2)
	v.remove(False, [8,10])
	return v.get()

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

def __vcounts(vs = None):
	if None == vs:
		vnew = []
		vc = __nvars
		for v in vc:
			vnew.append(vmeta())
		vs = vnew
	else:
		vc = len(vs)
		for v in vs:
			v.clear()
	for i,p in enumerate(masked(__predlist)):
		for c in p:
			vdx = abs(c)
			vs[vdx].add(sgn(c) > 0,i)
	return vs

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
	__vars = __vcounts()
	__masks = [7] * len(__predlist)




def __findmax(blist):
	maxf = 0
	maxt = 0
	false_ct = 0
	true_ct = 0
	for i,b in enumerate(blist):
		fct = b.fc()
		tct = b.tc()
		if fct > false_ct:
			false_ct = fct
			maxf = i
		if tct > true_ct:
			true_ct = tct
			maxt = i
	return maxf,false_ct,maxt,true_ct

def __reduce_vars(vars,denied):
	#print(pred,__predlist[pred], denied)
	pass

def __mask(pred,denied):
	print(pred,denied)

def __reduction_list(predlist):
	vs = set()
	for p in predlist:
		for c in p:
			vs.add(c)
	return vs

def __reduce_list(unsat,vsol,short_circuit=False):
	vc = __vcounts(unsat,vsol)
	denied = -1
	maxf,false_ct,maxt,true_ct = __findmax(vc) #$
	print(maxf,false_ct,maxt,true_ct)
	if true_ct > false_ct:
		remflag = True
		predlist = vsol[maxt].get(True)
		vsol[maxt].truthval(True)
	else:
		remflag = False
		predlist = vsol[maxf].get(False)
		vsol[maxf].truthval(False)

	redl = __reduction_list(predlist)
	for v in redl:
		v[abs(v)].remove(remflag, predlist)
	for p in predlist:
		unsat.remove(p)
	return unsat,vsol

def __bound(cert):
	for i in cert:
		if None == i:
			return False
	return True

def solve(short_circuit=False):
	vc = __vars

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

def frees():
	for i in range(__nvars):
		if None == __vars[i].truth():
			yield i



