import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=list(csv.reader(open('spx_prices.csv')))
del(data[0])
data_prices=[]
for line in data:
    line[0],line[1]=int(line[0]),float(line[1])
    data_prices.append(line[1])
    
mean_tab=[]
var_tab=[]
min_tab=[]
max_tab=[]
best_10=[]
cum_26=[]
cum_28=[]

#Testuje strategie dla signal_window od 2 do 99, best_10 bedzie tabelka na 10 najlepszych wynikow 
#patrzac na sredni profit w latach 2004-2014.

for n in range(2,100):
    
    signal=0
    signal_window=n
    position=0
    max_position=100
    cum_pnl=[0.0]

    for i in range(100,len(data)):
        pnl_daily=0
    
        if data[i][1]>max(data_prices[i-signal_window:i]):
            signal=1
        elif data[i][1]<min(data_prices[i-signal_window:i]):
                signal=-1
    
        pnl_daily=50*position*(data[i][1]-data[i-1][1])
        cum_pnl.append(cum_pnl[-1]+pnl_daily)
        position=max_position*signal
    
    if n==26:
        cum_26=cum_pnl
    if n==28:
        cum_28=cum_pnl    
    
    mean_tab.append(np.mean(cum_pnl))
    var_tab.append(np.var(cum_pnl))
    min_tab.append(round(min(cum_pnl),2))
    max_tab.append(round(max(cum_pnl),2))
    
    if len(best_10)<10:
        best_10.append(np.mean(cum_pnl))
    else:
        if np.mean(cum_pnl)>min(best_10):
            for i,x in enumerate(best_10):
                if x==min(best_10):
                    del best_10[i]
                    best_10.append(np.mean(cum_pnl))
                    break        
#Teraz ogarniam statystyki dla 10 najlepszych wynikow do dataframe'a 
col_n=[]
col_mean=[]
col_var=[]
col_min=[]
col_max=[]
   
for i,x in enumerate(mean_tab):
    for el in best_10:
        if x==el :
            col_n.append(i+2)
            col_mean.append(round(mean_tab[i],2))
            col_var.append(round(var_tab[i]))
            col_min.append(min_tab[i])
            col_max.append(max_tab[i])
            break
        
#Dodaje sobie jeszcze wiersz ze srednimi wartosciami dla wszystkich parametrow signal_window
            
col_n.append('avg')
col_mean.append(round(np.mean(mean_tab),2))
col_var.append(round(np.mean(var_tab)))
col_min.append(round(np.mean(min_tab)))
col_max.append(round(np.mean(max_tab)))  
      
data={'Mean':col_mean,'Variance':col_var,'Min':col_min, 'Max':col_max}
df=pd.DataFrame(data,index=(col_n),columns=('Mean','Variance','Min','Max'))        
print(df)      

#Zatem najlepszy wynik strategia osiagnela dla signal_window=26, dla 28 byla najstabilniejsza, wiec sygnal
#generowany dl takiej wartosci byl najpewniejszy. Srednio przynosila strate prawie 670 000.

#Jeszcze widac ze strategia bylaby srednio oplacalna gdyby nie jedna seria spadkow miedzy 1000 a 1500 
#dniem z pobranych danych

plt.plot(cum_26)
plt.plot(cum_28)

plt.show()

