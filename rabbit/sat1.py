
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


def reduce_plist(pl,nvars,vsol,unsat,short_circuit=False):
	pc = pl.copy()
	vsat=[]
	vc = vcounts(pl, nvars)
	mf,fc,mt,tc = findmax(vc)
	if short_circuit and fc ==1 and tc == 1:
		print("singles")
		return {},vsol
	if fc > tc:		
		#print("vsol {0} is false".format(mf))
		sat = vc[mf][0]
		usat = vc[mf][1]
		vsol[mf] = 0
	else:
		#print("vsol {0} is true".format(mt))
		sat = vc[mt][1]
		usat = vc[mt][0]
		vsol[mt] = 1
	#print(k)
	for p in sat:
		pc.pop(p)
	for p in usat:
		
	return pc,vsol


def solve(pl, nvars,unsat, short_circuit=False):
	vsol = [None] * nvars
	
	lpl0 = len(pl) - 1
	for i in range(len(pl)):
		lpl = len(pl)
		#each time redlist is called, pl is reduced and vsol is updated
		#print(lpl)
		pl,vsol,unsat = reduce_plist(pl, nvars, vsol, unsat, short_circuit)
		if lpl == lpl0 and lpl > 0:
			print("not satisfied. remainder:", pl)
			return vsol,unsat
		lpl0 = lpl
		if lpl == 0:
			#print(vsol)
			return vsol,unsat

