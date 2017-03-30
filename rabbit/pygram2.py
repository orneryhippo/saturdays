from random import random, randint

# load word list
def load_file(fn, enc = "UTF-8"):
	with open(fn,"r", encoding = enc) as corpus:
		c = corpus.read()
		return c


# cleanup

# words.subst(",", " ")
# words.subst(".", " ")
def cleanup(corp, replacements = {"\n": " ", "“": "\"", "”":"\"","‘":"\'","’":"\'", "-":" - "}):
	c = corp
	for k,v in replacements.items():
		c = c.replace(k,v)
	return c

def count_items(lst):
	ct = {}
	for t in lst:
		if t in ct:
			ct[t] += 1
		else:
			ct[t] = 1
	return ct


# this produces [0]..[base-1], [0,0]..[0,base-1],[1,0]..[base-1,base-1],[0,0,0]...
def inclist(lst, base):
	if len(lst) < 1:
		lst = [-1]
	l = lst[-1]
	if l == base - 1:
		return inclist(lst[:-1],base) + [0]
	else:
		return lst[:-1] + [l+1]

# show it works
def print_inclist():
	l = []
	b = 3
	for i in range(200):
		l = inclist(l,b)
		print(l)

# make a generator
def g_inclist(n = 200, base =3):
	l = []
	b = base
	while c < n:
		c += 1
		l = inclist(l,b)
		yield l


# ngrams
def ngram(letters,n=3):
	gram = []
	for i in range(len(letters) - n + 1):
		gram.append(tuple(letters[i:i+n]))
	return gram



# ngrams
def ngramX(letters,n=3):
	gram = []
	#modification: multiply the collection by n so that it loops
	ndx = len(letters) - n + 1
	for i in range(n * ndx):
		ind = i % ndx
		gram.append(tuple(letters[ind: ind + n]))
	return gram

# markov_gen(ngrams)
def mk_wl(lst):
	#given a list of tuples as lst, use the first n as the key and the last element as the value in upsert count
	wl = {}
	for t in lst:
		wl = upsert(t[:-1],t[-1],wl)
	return wl

# deprecated, use mk_wl(lst) instead
def mk_tri_wlu(lst):
	return mk_wl(lst)
	
	#wl = {}
	#for t in lst:
	#	a,b,c = t
	#	wl = upsert((a,b),c,wl)
	#return wl



# create a generating function from the distribution, which returns the keys with appropriate probabilities
# takes a dict of {items:counts, ...} and returns a function which takes a value {0..1} and returns a 
# key from the given dict with prob = item_count/sum(item_counts)
# when used with a markov process, a dict is constructed in which each key is a state and the value is the generator
# 
def gen_fn(dist_map):
	tot = float(sum(dist_map.values()))
	cp = 0.0
	prob_dist = {}
	for k in dist_map.keys():
		cp += dist_map[k]/tot
		prob_dist[cp] = k
	def inn(x):
		for k in prob_dist.keys():
			if x < k:
				return prob_dist[k]
	return inn

# takes a markov_list, composed of {items: {next:ct, ...}, ...}
# returns {item: gen_fn(), ...}
def make_markov(markov_list):
	ml ={}
	for k in markov_list.keys():
		ml[k] = gen_fn(markov_list[k])
	return ml


def get_random_key(my_dict, r = 1):
	if r != 0:
		r = randint(0,len(my_dict)-1)
	return list(my_dict)[r]


def get_rand_seed(lst, ct = 2):
	# take the first ct from a random word in lst
	return tuple(list(lst[randint(0,len(lst)-1)][:ct]))


def mk_markov_generator(markov_list, seed, n = 2):
	# given a dict of keys and generators
	# return a generator 
	# seed = get_rand_seed(seedlist,n)
	ml = make_markov(markov_list)
	def m():
		nonlocal seed,ml,n
		if seed in ml.keys():
			nxt = ml[seed](random())
		else:
			nxt = " "
		s = list(seed[1:])
		s.append(nxt)
		seed = tuple(s)
		return nxt
	return m


def print_words(corpus_file, nl = 3, wds = 20):
	words = cleanup(load_file(corpus_file).lower())
	charlist = []
	for w in words.split(" "):
		charlist += list(w)
	ng = ngram(charlist,nl)
	ll = mk_wl(ng)

	for j in range(wds):
		r = randint(0,len(charlist)-nl+1)
		s = charlist[r:r+nl-1]
		sent = list(s)
		mg = mk_markov_generator(ll,tuple(s),nl)
		for i in range(10):
			sent.append(mg())
		wd = " ".join(sent)
		print(wd)
		print("\n")


def print_paras(corpus_file, nl = 3, paras = 20):
	words = cleanup(load_file(corpus_file).lower())
	wd = words.split(" ")
	
	ng = ngram(wd,nl)
	wl = mk_wl(ng)

	for j in range(paras):
		r = randint(0,len(wd)-nl+1)
		s = wd[r:r+nl-1]
		sent = list(s)
		mg = mk_markov_generator(wl,tuple(s),nl)
		for i in range(100):
			sent.append(mg())
		par = " ".join(sent)
		print(par)
		print("\n")


def mk_paras(corpus_file, nl = 3, paras = 20):
	words = cleanup(load_file(corpus_file).lower())
	wd = words.split(" ")
	
	ng = ngram(wd,nl)
	wl = mk_wl(ng)

	for j in range(paras):
		r = randint(0,len(wd)-nl+1)
		s = wd[r:r+nl-1]
		sent = list(s)
		mg = mk_markov_generator(wl,tuple(s),nl)
		for i in range(100):
			sent.append(mg())
		par = " ".join(sent)
		yield par


# try it out
corpus_file = ".\\data\\lorem2.txt"
words = cleanup(load_file(corpus_file).lower())
# parse to units (letters & sp)
wg = mk_paras(words)
for p in wg:
	print(p)

exp = range(levels)
for x in exp:

d = dict(zip([chr(x+ord('a')) for x in range(3)],[list(range(z,z+10)) for z in range(1,31,10)]))
# produces:
# {'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#  'b': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
#  'c': [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}
#; (require '[clojure.string :as s])
#; (zipmap (for [x (range 3)] x) (for [y (range 7 20) :when (odd? y)] y))
#; (zipmap (map keyword (.split #"" "abc")) (for [x (range 1 31 10)] (range x (+ 10 x))))
#; produces similar, but with keyword keys, same as below without the require
#; (zipmap (map keyword (s/split "abc" #"")) (for [x (range 1 31 10)] (range x (+ 10 x))))
#; this does it without the keyword change
#; (zipmap (s/split "abc" #"") (for [x (range 1 31 10)] (into [] (range x (+ 10 x)))))