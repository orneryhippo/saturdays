def load_file(fn):
	with open(fn,"r") as corpus:
		c = corpus.read()
		return c

def load_sentences(fn):
	with open(fn,"r") as corpus:
		c = corpus.read()
		return c.split('.')

def load_stripped_sentences(fn):
	with open(fn,"r") as corpus:
		c = corpus.read()
		return list(map(lambda x: x.strip(), c.split('.')))


def cleanup(corp, replacements = {",": " , "}):
	c = corp
	for k,v in replacements.items():
		c = c.replace(k,v)
	return c

def load_stripped_sentences(fn):
	with open(fn,"r") as corpus:
		c = cleanup(corpus.read())
		return list(map(lambda x: x.strip(), c.split('.')))


def trigram(sentences):
	tri = []
	allwords = " . ".join(sentences).split(" ")
	for i in range(len(allwords)-2):
		tri.append((allwords[i],allwords[i+1],allwords[i+2]))
	return tri



def ngram(sentences,n=2):
	#sentences should already be joined into a single string with spaces around all words and punct
	gram = []
	allwords = sentences.split(" ")
	for i in range(len(allwords) - n + 1):
		gram.append(tuple(allwords[i:i+n]))
	return gram


def ngram(letters,n=2):
	gram = []
	for i in range(len(letters) - n + 1):
		gram.append(tuple(letters[i:i+n]))
	return gram

def apsert(k,v,m):
	# creates a list of v associated with each k 
	if k in m:
		m[k].append(v)
	else:
		m[k] = [v]
	return m

def mk_tri_wl(lst):
	wl = {}
	for t in lst:
		a,b,c = t
		wl = apsert((a,b),c,wl)
	return wl


def sel_wl_word(wl, digram, default_word = '.'):
	if digram in wl:
		return wl[digram][randint(0,len(wl[digram])-1)]
	else:
		return default_word

######################
# harder version
######################

def count_items(lst):
	ct = {}
	for t in lst:
		if t in ct:
			ct[t] += 1
		else:
			ct[t] = 1
	return ct

def upsert(k,v,m):
	if k in m:
		val = m[k]
		if v in val:
			val[v] += 1
		else:
			val[v] = 1
		m[k] = val
	else:
		m[k] = {v:1}
	return m


def count_tri(lst):
	ct = {}
	for t in lst:
		a,b,c = t
		ct = upsert((a,b),c,ct)
	return ct

def get_cumul(markov,digram):
	opts = markov[digram] #returns a dict
	choices = []
	for k in opts.keys():
		ct = opts[k]
		for i in range(ct):
			choices.append(k)
	return choices

def select_word(cumul, default_word):
	return cumul[randint(0,len(cumul)-1)]


def get_word(markov, digram, default_word = '.'):
	if digram in markov:
		cumul = get_cumul(markov,digram)
		return select_word(cumul,default_word)
	else:
		return default_word 
##################
# end of harder version
##################

# dist_map is a dict of results and counts
def test_fn(dist_map):
	tot = float(sum(dist_map.values()))
	cp = 0.0
	prob_dist = {}
	for k in dist_map.keys():
		cp += dist_map[k]/tot
		prob_dist[cp] = k
	return prob_dist

dm = {'a':1, 'b':2, 'c':3}
pm = test_fn(dm)

def tf2(prob_map):
	r = random()
	for k in prob_map.keys():
		if r < k:
			return prob_map[k]

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


# e.g.
m = make_markov(trigram)
digram_key = get_random_key(m)
m[digram_key](random()) -> 'random' next item


#################
corpus_file = ".\\data\\lorem.txt"
t = trigram(load_stripped_sentences(corpus_file))
tc = count_items(t)
