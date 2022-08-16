import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
from pandas_datareader import data as pdr 

def prev_quarter_last_day(q_date): #end of previous quarter
	if q_date.month < 4:
		return datetime(q_date.year -1, 12, 31) 
	elif q_date.month < 7:
		return datetime(q_date.year, 3, 31) 
	elif q_date.month < 10:
		return datetime(q_date.year, 6, 30)
	return datetime(q_date.year, 9, 30) 
def prev_quarter_first_day(q_date):
	if q_date.month < 4:
		return datetime(q_date.year -1, 10, 1)
	elif q_date.month < 7:
		return datetime(q_date.year, 1, 1)
	elif q_date.month < 10:
		return datetime(q_date.year, 4, 1)
	return datetime(q_date.year, 7, 1)
def set_quarter_date(q_date):
	if q_date.weekday() == 5:
		q_date += timedelta(+2)
		return q_date
	elif q_date.weekday() == 6:
		q_date += timedelta(+1)
		return q_date
	elif q_date == 5:
		q_date -= timedelta(1)
		return q_date
	elif q_date == 6:
		q_date -= timedelta(2)
		return q_date
	else:
		return q_date
def prev_month_last_day(m_date):
		date_prev_month_last_day = m_date - timedelta(m_date.day)
		if date_prev_month_last_day.weekday() == 5:
			date_prev_month_last_day -= timedelta(1)
		if date_prev_month_last_day.weekday() == 6:	
			date_prev_month_last_day -= timedelta(2)
		return date_prev_month_last_day
def prev_month_first_day(m_date):
	date_prev_month_first_day=  prev_month_last_day(m_date) - timedelta(prev_month_last_day(m_date).day-1)
	if (prev_month_last_day(m_date) - timedelta(prev_month_last_day(m_date).day-1)).weekday() == 5:
		date_prev_month_first_day += timedelta(2) 
	if (prev_month_last_day(m_date) - timedelta(prev_month_last_day(m_date).day-1)).weekday() == 6:
		date_prev_month_first_day += timedelta(1) 
	return date_prev_month_first_day
def set_date_lst(date_today):	
	date_prev_friday = date_today - timedelta(date_today.weekday()+3)
	days = [set_quarter_date(prev_quarter_first_day(date_today)), 
			set_quarter_date(prev_quarter_last_day(date_today)),
			prev_month_first_day(date_today) ,
			prev_month_last_day(date_today),
			date_prev_friday - timedelta(4),
			date_prev_friday, 
			date_today]
	if date_today.weekday() == 5:
		days[6] -= timedelta(1)
	elif date_today.weekday() == 6:
		days[6] -= timedelta(2)
	elif date_today.weekday() == 0:
		days[6] -= timedelta(3)
	else: 
		days[6] -= timedelta(1)
	for i in range(len(days)):
		days[i] = days[i].strftime('%Y-%m-%d 00:00:00')
	return days

def solution_dataframe(date):
	blocks = np.array([None, None, None, None, None, None, None])
	df_sol = pd.DataFrame({'Date': set_date_lst(date), 'Open': blocks, 'High': blocks, 'Low':blocks,'Close': blocks})
	df_sol = df_sol.set_index('Date')
	df_sol['daily_low'] = blocks.tolist()
	df_sol['daily_high']= blocks.tolist()
	df_sol['weekly_low']= blocks.tolist()
	df_sol['weekly_high']= blocks.tolist()
	df_sol['monthly_low']= blocks.tolist()
	df_sol['monthly_high']= blocks.tolist()
	df_sol['quarterly_low']= blocks.tolist()
	df_sol['quarterly_high']= blocks.tolist()
	df_sol.index = sorted(df_sol.index)
	df_sol.index.name='date'
	download_data(df_sol)
	

def download_data(add_df):
	stock = 'AAPL'
	df = pdr.get_data_yahoo(stock,
		prev_quarter_first_day( datetime.strptime(add_df.index[0], '%Y-%m-%d 00:00:00')), 
		add_df.index[6]).drop(columns=['Volume', 'Adj Close'])
	calc(df,add_df)
def calc(df, add_df): 
	for i in range(len(df.index)):
		for j in range(len(add_df.index)):
			if str(df.index[i]) == add_df.index[j]:
				add_df['High'][j] = df['High'][i]
				add_df['Low'][j] = df['Low'][i] #.round(1)
				add_df['Close'][j] = df['Close'][i]
				add_df['Open'][j] = df['Open'][i]
				add_df['daily_low'][j] = df['Low'][i]
				add_df['daily_high'][j] = df['High'][i]
				if add_df['weekly_low'][j] == None or add_df['weekly_high'][j] == None: 
					weekly(df,add_df, i, j)
				if add_df['monthly_low'][j] == None or add_df['monthly_high'][j] == None: 
					monthly(df,add_df, i, j)
				if add_df['quarterly_low'][j] == None or add_df['quarterly_high'][j] == None:
					quarterly(df,add_df, i, j)
	for i in range(len(add_df.index)):
		for j in add_df.columns:
			add_df[j][i] =  add_df[j][i].round(2)

	print(add_df)
def weekly(df,add_df,i,j):
	add_df['weekly_low'][j] = df['Low'][i-df.index[i].weekday()]
	add_df['weekly_high'][j] = df['High'][i-df.index[i].weekday()]
	rng = 5
	if i + 5 > df.shape[0]: 
		rng = df.index[i].weekday()
	for k in range(rng):
		if add_df['weekly_low'][j] > df['Low'][i-df.index[i].weekday()+k]:
			add_df['weekly_low'][j] = df['Low'][i-df.index[i].weekday()+k]
		if add_df['weekly_high'][j] < df['High'][i-df.index[i].weekday()+k]:
			add_df['weekly_high'][j] = df['High'][i-df.index[i].weekday()+k]	 

def monthly(df,add_df,i,j):	
	for k in range (len(df.index)):
		if df.index[k] == prev_month_first_day(df.index[i]):
			add_df['monthly_low'][j] = df['Low'][k]
		if add_df['monthly_low'][j] != None and add_df['monthly_low'][j] > df['Low'][k]:
			add_df['monthly_low'][j] = df['Low'][k]
		if df.index[k] == prev_month_last_day(df.index[i]):
			break
	for k in range (len(df.index)):
		if df.index[k] == prev_month_first_day(df.index[i]):
			add_df['monthly_high'][j] = df['High'][k]
		if add_df['monthly_high'][j] != None and add_df['monthly_high'][j] < df['High'][k]:	
			add_df['monthly_high'][j] = df['High'][k]
		if df.index[k] == prev_month_last_day(df.index[i]):
			break

def quarterly(df,add_df,i,j):
	for k in range(len(df.index)):
		if df.index[k].to_pydatetime() == set_quarter_date( prev_quarter_first_day(df.index[i])):
			add_df['quarterly_low'][j] = df['Low'][k]
		if add_df['quarterly_low'][j] != None and add_df['quarterly_low'][j] > df['Low'][k]:
			add_df['quarterly_low'][j] = df['Low'][k]
		if df.index[k].to_pydatetime() == set_quarter_date( prev_quarter_last_day(df.index[i])):
			break
	for k in range(len(df.index)):
		if df.index[k].to_pydatetime() == set_quarter_date( prev_quarter_first_day(df.index[i])):
			add_df['quarterly_high'][j] = df['High'][k]
		if add_df['quarterly_high'][j] != None and add_df['quarterly_high'][j] < df['High'][k]:
			add_df['quarterly_high'][j] = df['High'][k]
		if df.index[k].to_pydatetime() == set_quarter_date( prev_quarter_last_day(df.index[i])):
			break




def main():
	date_today = datetime.now()
	solution_dataframe(date_today)
if __name__ == '__main__':
	main()






