from sqlite3 import *
from collections import Counter
cnt = Counter()

con = connect("bar_data_test.db")
c = con.cursor()


rows = c.execute("SELECT NAME, \
				CATEGORY	from BARS ")
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist
comp="bars lounges lounges bars cocktail bars cocktail bars"
comp=' '.join(unique_list(comp.split()))
comp = comp.split()
categry_match=[]
#print comp
def words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())
for row in rows:
	print row[1]
	i=0
	for word in words_in_string(comp, row[1]):
		print(word)
		i+=1
	print i
	#print "********	"
	categry_match.append([i,row[0]])
categry_match.sort(key=lambda x: x[0], reverse=True)
j=0
while j<15:
	print categry_match[j][1]
	j+=1

		
	#print row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]
#suffix_array.sort(key=lambda a: buffer(content, a))