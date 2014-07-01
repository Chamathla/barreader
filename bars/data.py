from sqlite3 import *
from collections import Counter
cnt = Counter()

con = connect("bar_data_test.db")
c = con.cursor()


rows = c.execute("SELECT name, address from BARS ")

for row in rows:
	print row

		
	#print row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]
#suffix_array.sort(key=lambda a: buffer(content, a))