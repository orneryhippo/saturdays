
(defn contradiction? 
	[masked-list] 
	(any? empty? masked-list))

(def *empty-list* '())

(defn is-any? [pred the-list]
	(cond 
		(empty? the-list) false
		(if (pred (first the-list))
			true
			(is-any? pred (rest the-list)))))


(defn in? [an-item the-list]
	(cond
		(empty? the-list) false
		(= an-item (Math/abs (first the-list))) true
		:else (in? an-item (rest the-list))))

(defn without [an-item the-pred]
	(cond
		(empty? the-pred) '()
		(not= an-item (Math/abs (first the-pred))) (cons (first the-pred) (without an-item (rest the-pred)))
		:else (without an-item (rest the-pred))))

(defn withan [an-item the-list]
	(filter #(in? an-item %) the-list))

(defn withoutan [an-item the-list]
	(filter #(not (in? an-item %)) the-list))


(defn make-empty-plist [n] 
	(take n (repeat [])))



(defn m-pred)
(defn masked-list 
	[plist masks] 
	(cond 
		(empty? plist) ()
		(empty? masks) plist
		(cons (mask-pred (first plist) (first masks)) (masked-list (rest plist) (rest masks)))))

(defn renorm [t f] 
	(* (+ t f) (abs (- (* 2 (/ t (+ t f))) 1))))

(map count pl)

(defn sat? [pred v]
	(cond 
		(= v (first pred)) :true
		(= v (first (rest pred))) :true
		(= v (first (rest (rest pred)))) :true
		:else :false))

(defn unsat [plist v]
	(cond 
		(empty? plist) nil
		(sat? (first plist) v) (unsat (rest plist v))
		(cons (first plist) (unsat (rest plist v)))))


(defn rand-sig [] (- 1 (* 2 (rand-int 2))))
(defn rand-range [min max] (+ min (rand-int (- max min))))
(defn make-triple [min max]
	(let [x  (rand-range min (- max 2))
		  y  (rand-range (+ 1 x) (- max 1))
		  z  (rand-range (+ 1 y) max)]
	(list (* (rand-sig) x) (* (rand-sig) y) (* (rand-sig) z))))
	

(defn make-plist [npred nvars]
	(for [x (range npred)]
		(make-triple 1 (+ 1 nvars))))


(defn count-tf [pred ct]
	(let [p1  (first pred)
		  p2  (second pred)
		  p3 (second (rest pred))
		  ct1 (+ 1 (get ct (first pred) 0))
		  ct2 (+ 1 (get ct (second pred) 0))
		  ct3 (+ 1 (get ct (second (rest pred)) 0))]
		  (merge ct {p1 ct1} {p2 ct2} {p3 ct3})))


(defn add-item [acc itm]
    (assoc acc itm (+ 1 (get acc itm 0))))


(defn counter [the-lol]
    "Takes a list of list of integers and returns a map with the ints as keys and their counts as values"
    (reduce add-item {} (flatten the-lol))
)

(defn prob [t f]
	(double (/ t (+ t f))))

(defn vkeys [v] 
	(set (map #(Math/abs %) (keys v)))) ;; assumes keys as integers

