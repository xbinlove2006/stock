
import baostock as bs
import pandas as pd
#所有股票
ALL_STOCKS=[
    {'code':'000969','date':'2020-11-06'},
    {'code':'603909','date':'2020-11-06'},
    {'code':'603456','date':'2020-11-06'},

    {'code':'300569','date':'2020-11-09'},
    {'code':'603333','date':'2020-11-09'},
    {'code':'300183','date':'2020-11-09'},
    {'code':'600486','date':'2020-11-09'},
    {'code':'002709','date':'2020-11-09'},
    {'code':'688189','date':'2020-11-09'},
    {'code':'300271','date':'2020-11-09'},
    
    {'code':'603007','date':'2020-11-10'},
    {'code':'600699','date':'2020-11-10'},
    {'code':'601717','date':'2020-11-10'},
    {'code':'000668','date':'2020-11-10'},
    
    {'code':'300442','date':'2020-11-12'},
    {'code':'000016','date':'2020-11-12'},
    {'code':'300624','date':'2020-11-12'},
    
    {'code':'000990','date':'2020-11-13'},
    {'code':'300108','date':'2020-11-13'},
    {'code':'300678','date':'2020-11-13'},
    {'code':'002465','date':'2020-11-13'},
    
    {'code':'002856','date':'2020-11-16'},
    {'code':'002553','date':'2020-11-16'},
    {'code':'002623','date':'2020-11-16'},
    {'code':'600581','date':'2020-11-16'},
    
    {'code':'300413','date':'2020-11-17'},
    {'code':'002099','date':'2020-11-17'},
    {'code':'688289','date':'2020-11-17'},
    {'code':'000063','date':'2020-11-17'},
    {'code':'603535','date':'2020-11-17'},

    {'code':'600438','date':'2020-11-18'},
    {'code':'000813','date':'2020-11-18'},
    
    {'code':'000966','date':'2020-11-19'},
    {'code':'603214','date':'2020-11-19'},
    {'code':'002434','date':'2020-11-19'},

    {'code':'002735','date':'2020-11-24'},
    {'code':'002465','date':'2020-11-24'},
    {'code':'603713','date':'2020-11-24'},
    {'code':'300617','date':'2020-11-24'},
    
    {'code':'002510','date':'2020-11-26'},
    {'code':'002683','date':'2020-11-26'},
    {'code':'600509','date':'2020-11-26'},

    {'code':'002514','date':'2020-11-27'},
    {'code':'000777','date':'2020-11-27'},

    {'code':'601018','date':'2020-11-30'},
    {'code':'603185','date':'2020-11-30'},
    {'code':'300131','date':'2020-11-30'},
    {'code':'000048','date':'2020-11-30'},

    {'code':'603879','date':'2020-12-01'},
    {'code':'000785','date':'2020-12-01'},
    {'code':'002813','date':'2020-12-01'},
    {'code':'600155','date':'2020-12-01'},
    ]
datalist=[]
def transcode():
    for i in range(len(ALL_STOCKS)):
            if ALL_STOCKS[i]['code'][0]=='6':
                ALL_STOCKS[i]['code']='sh.'+ALL_STOCKS[i]['code']
            else:
                ALL_STOCKS[i]['code']='sz.'+ALL_STOCKS[i]['code']
    print(ALL_STOCKS)
def getdata():
    # 获取数据放入datalist
    bs.login()
    for stock in ALL_STOCKS:
        rs = bs.query_history_k_data_plus(stock['code'],"date,code,open,high,low,close,preclose",start_date=stock['date'])
        while (rs.error_code == '0') & rs.next():
            datalist.append(rs.get_row_data())
        pass
    bs.logout()
    # 处理数据
    index=0#当前股票开始下标，用来计算天数
    code=datalist[0][1]#当前股票代码
    buy=datalist[0][2]#开盘买入价
    tmpdata=[]
    newlist=[]
    tmplist=[]
    for i in range(len(datalist)):
        if i==0:
            index=0
            code=datalist[index][1]
            buy=float(datalist[index][2])
            high=float(datalist[index][3])
            low=float(datalist[index][4])
            close=float(datalist[index][5])
            tmpdata=datalist[index][:]
            tmpdata.append((low-buy)*100/buy)
            tmpdata.append((high-buy)*100/buy)
            tmpdata.append((close-buy)*100/buy)
        elif datalist[i][1]!=code:
            if len(tmpdata)<16:
                tmplist=['' for j in range(16-len(tmpdata))]
                tmpdata.extend(tmplist)
            newlist.append(tmpdata)
            index=i
            code=datalist[index][1]
            buy=float(datalist[index][2])
            high=float(datalist[index][3])
            low=float(datalist[index][4])
            close=float(datalist[index][5])
            tmpdata=datalist[index][:]
            tmpdata.append((low-buy)*100/buy)
            tmpdata.append((high-buy)*100/buy)
            tmpdata.append((close-buy)*100/buy)
        print('index',index,'i:',i)
        
        if i-index==2 or i-index==4 or i-index==9:
            saleopen=float(datalist[i][2])
            saleclose=float(datalist[i][5])
            changeopen=(saleopen-buy)*100/buy
            tmpdata.append(changeopen)
            changeclose=(saleclose-buy)*100/buy
            tmpdata.append(changeclose)
        pass
    if len(tmpdata)<16:
        tmplist=['' for j in range(16-len(tmpdata))]
    tmpdata.extend(tmplist)
    newlist.append(tmpdata)
    #计算成功率
    rate=['' for j in range(16)]
    rate[8]='成功率'
    acc=[0 for j in range(16)]
    for list in newlist:
        for k in range(9,16):
            if list[k]!='':
                if float(list[k])>0:
                    acc[k]=acc[k]+1
        pass
    for j in range(9,16):
        rate[j]=acc[j]/len(newlist)
    newlist.append(rate)
    result = pd.DataFrame(newlist, columns=['日期','股票代码','开盘','最高','最低','收盘','昨日收盘','当日最大回撤','当日最大涨幅','当日盈利','3天开盘卖','3天收盘卖','5天开盘卖','5天收盘卖','10天开盘卖','10天收盘卖'])
    result.to_csv("stock.csv", index=False)
    result.to_csv('stock_gbk.csv',index=False,encoding='gbk')
    
    pass
if __name__ == "__main__":
    transcode()
    getdata()

    pass