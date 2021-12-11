import pandas as pd
import random

text='long time no see my friend!'
print(text)

df = pd.read_csv('3.csv')

no_rows=len(df.index)
row=[]
for i in range(no_rows):
    raw=df.iloc[i,0]
    time=raw.split()[1]
    Open=float(raw.split()[2])
    high=float(raw.split()[3])
    low=float(raw.split()[4])
    Close=float(raw.split()[5])
    row.append([time,Open,high,low,Close])
    
data=pd.DataFrame(row,columns=['Time','Open','High','Low','Close'])

test_data=data.head(len(data.index))

print(test_data)

profit=0
money_log=[]
wins=0
loss=0
buys=0
sells=0
nutral=False
for i in range(len(test_data.index)-1):
    
    print(i,'  ',test_data.iloc[i,])
    
    high_p=test_data.iloc[i,2]
    low_p=test_data.iloc[i,3]
    
    open_p=test_data.iloc[i,1]
    close_p=test_data.iloc[i,4]
    
    f_high_p=test_data.iloc[i+1,2]
    f_low_p=test_data.iloc[i+1,3]
    
    f_open_p=test_data.iloc[i+1,1]
    f_close_p=test_data.iloc[i+1,4]
    
    if i==0:
        price=round(random.uniform(high_p,low_p),5)
    print('*************************************************')
    print('\nPrice= ', price)
    
    print('\n'+"Buy b or Sell s? \n")
    
    if nutral==False:
        #action=input()
        acc=['b','s']
        action=random.choice(acc)
        print(action)

        if action=='b':
            buys+=1
        if action=='s':
            sells+=1
            
    else:
        action=action
        print('\nHolding ',action)
    
    if action=='b':
        
        tp=round(price+0.0005,5)
        sp=round(price-0.0015,5)
        print('TP= ',tp)
        print('SP= ',sp)
        
        if f_open_p <= sp or f_low_p <= sp or f_close_p <= sp:
            profit -= 15
            money_log.append(profit)
            print('LOSS $15! Profit= ', profit)
            nutral=False
            loss+=1
            price=round(random.uniform(high_p,low_p),5)
        
        elif f_open_p >= tp or f_high_p >= tp or f_close_p >= tp:
            profit +=5
            money_log.append(profit)
            print('WIN $5! Profit= ', profit)
            nutral=False
            wins+=1
            price=round(random.uniform(high_p,low_p),5)
            
        else:
            money_log.append(profit)
            print('No win No loss! Profit= ', profit)
            nutral=True
            price=price
            
    if action=='s':
        
        tp=round(price-0.0005,5)
        sp=round(price+0.0015,5)
        print('TP= ',tp)
        print('SP= ',sp)
        
        
        if f_open_p >= sp or f_high_p >= sp or f_close_p >= sp:
            profit -= 15
            money_log.append(profit)
            print('LOSS $15! Profit= ', profit)
            nutral=False
            loss+=1
            price=round(random.uniform(high_p,low_p),5)
        
        elif f_open_p <= tp or f_low_p <= tp or f_close_p <= tp:
            profit +=5
            money_log.append(profit)
            print('WIN $5! Profit= ', profit)
            nutral=False
            wins+=1
            price=round(random.uniform(high_p,low_p),5)
            
        else:
            money_log.append(profit)
            print('No win No loss! Profit= ', profit)
            nutral=True
            price=price
    print('*************************************************')

print('\n/////////////////////////////////////////////////////')
print('\nBuys= ',buys)
print('\nSells= ',sells)
print('\nWins= ',wins)
print('\nLosses= ',loss)
print('\nProfit= $',profit)
print('/////////////////////////////////////////////////////')

#print(money_log[99875])
#print(money_log)
