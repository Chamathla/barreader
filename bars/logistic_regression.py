import pandas.io.sql as psql
import sqlite3 as lite
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm
from pandas.core.common import isnull
from sklearn import linear_model
from pandas import Series, DataFrame, Index
from numpy import *
from sqlite3 import *
con = connect("bar_data_test.db")
c = con.cursor() 

c.execute("DROP TABLE IF EXISTS LOGIC")

sql1 = """CREATE TABLE LOGIC (
         NAME  FLOAT,
		 DELIVERY FLOAT,
		 TAKEOUT FLOAT,
		 CREDITCARD FLOAT,
		 GOODFOR FLOAT,
		 PARKING FLOAT,
		 GOODFORKIDS FLOAT,
		 GOODFORGROUPS FLOAT,
		 ATTIRE FLOAT,
		 AMBIENCE FLOAT,
		 NOISELEVEL FLOAT,
		 ALCOHOL FLOAT,
		 OUTDOOR FLOAT,
		 HASTV FLOAT,
		 WAITERS FLOAT
		 )"""
	
c.execute(sql1)

with con:
	#sql = "SELECT * FROM BARS"
	#df = psql.frame_query(sql, con)
 	df1 = psql.read_frame('''SELECT NAME as N1, PRICE as P1, CREDITCARD as CC1, PARKING as PK1, WHEELCHAIR as WC1, HASTV as TV1, MUSIC as M1,\
				GOODFORGROUPS as GFG1, COATCHECK as CoatC1, OUTDOOR as OD1	from BARS, NOISELEVEL as NL1, ALCOHOL as AC1, BESTNIGHTS as BN1''',con)
				
	
	df = df1.ix[1:]
	print df
	print "***************"
	#df = df[pd.isnull(df['CC1'])]
	df2 = psql.read_frame('''SELECT NAME as N2, PRICE as P2, CREDITCARD as CC2, PARKING as PK2, WHEELCHAIR as WC2, HASTV as TV2, MUSIC as M2,\
				GOODFORGROUPS as GFG2, COATCHECK as CoatC2, OUTDOOR as OD2, NOISELEVEL as NL2, ALCOHOL as AC2, BESTNIGHTS as BN2\
				from BARS where NAME like "%northern lights lounge" ''',con)

	df_0=df2.ix[1:]
	print df_0
	def get_match(df,cat1,cat2):
		#df = df[np.isfinite(df['EPS'])]
		df_match = df[df[cat1].str.contains(cat2)]
		df_match['Match'] = np.ones(len(df_match))

		df_nomatch= df[~df[cat1].str.contains(cat2)]
		df_nomatch['Match'] = np.zeros(len(df_nomatch))
		df_merge = df_match.append(df_nomatch)
		columns = ['Amb1', 'OD1', 'TV1', 'M1', 'CoatC1', 'D1']
		#X[:,range(1,len(columns)+1)] = df[columns].values
		X = columns
		#return BuildX(df_merge['Match'])
		#p = df_merge.groupby('Match').size()
		return df_merge['N1'],df_merge['Match']
		#return p
	def BuildX(df):
		columns = ['Amb1', 'OD1', 'TV1', 'M1', 'CoatC1', 'D1']
		X = np.ones(shape=(len(df),len(columns)+1))
		X[:,range(1,len(columns)+1)] = df[columns].values
		return X
	select_list = list(df.columns.values)
	my_list=list(df_0.columns.values)
	columns = ['Amb1', 'OD1', 'TV1', 'M1', 'CoatC1', 'D1']
	i=1
	y=np.empty((6,10))
	print y
	x=[]
	X=[]
	
	K = [[1 for x in xrange(10)] for x in xrange(6)]
	while i<len(my_list):
		cat2=df2.iloc[0][my_list[i]]
		#cat1=df.iloc[0][select_list[i]]
		#cat1 = my_list[i]
		cat1 = select_list[i]
		print cat1, cat2
		
		name,p= get_match(df,cat1,cat2)
		
		#x = p[0]
		#y = p[1]
		
		y[i-1]= p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]
		#print p[1]
		#l = x.count()
		#print cat1,x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10]
		columns = ['Amb1', 'OD1', 'TV1', 'M1', 'CoatC1', 'D1']
		#y=array(p for i in y)
		#[[n+m*10 for n in range(5)] for m in range(5)]
		y=y
		#K[i] = np.array([y[1],y[2],y[3],y[4],y[5],y[6],y[7],y[8],y[9],y[10]])
		#print K
		uniques, x = np.unique(columns, return_inverse=True)
		X=np.array([x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10]])
		X=X
		print array(x[k] for k in range(l))
	
		#X[:,range(1,len(columns)+1)] = X.values
		f = 'y ~ x'
		#d = { "x": pd.Series(x), "y": pd.Series(y)}
		#dff = pd.DataFrame(d)
		#y, X = patsy.dmatrices(f, dff, return_type='dataframe')
		logit = linear_model.LogisticRegression()
	
		print x.values
		print X
		print y
		logit.fit(y,X)
		print logit.score(y, X)
		#joblib.dump(logit, "data/logit.joblib.pkl", compress=9) 
		i+=1
		#print sm.Logit(y, X).fit().summary()
		#print cross_validation.cross_val_score(logit, X, y, cv=5) 
		#print sm.formula.logit(f, data=dff).fit().summary()
	#	c.execute("insert into LOGIC values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,)",(name, delivery, takeout, creditCard, goodfor, parking, goodforKids, goodforGroups, attire, ambience, noiselevel, alcohol, outdoor, tv, waiter))
	#	conn1.commit()
	'''
		logit.fit(X, y)
		joblib.dump(logit, "data/logit.joblib.pkl", compress=9)    
		print cross_validation.cross_val_score(logit, X, y, cv=5)    

		df_match = helper.transform(df_match)
		X_match = helper.BuildX(df_match)
		y_match = df_match['Match'].values
		print logit.score(X_match, y_match)
	    X = helper.BuildX(df)
    y = df['Match'].values'''
	#print X
	#print y
#	print cross_validation.cross_val_score(logit, y, X, cv=5)
	logitscore = logit.score(y, X)
#	print "decision: ",logit.decision_function(y)
#	print logit.coef_
#	print "params: ",logit.get_params(deep=True)
	#joblib.dump(logit, "data/logit.joblib.pkl", compress=9) 
	#print sm.Logit(y, X).fit().summary()	
	
		#logit = linear_model.LogisticRegression()