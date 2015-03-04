#coding=utf8
import sys
import random
#print random.randint(0, 99)
#print "====", random.uniform(0, 0.99)
def calRandomValue(total, num):
    '''
        Args:
            total: 钱的总数量
            num: 分发的总人数
    '''
    print total, num
    total = float(total)
    num = int(num)
    min = 0.01
    max = 0
    if(num < 1): 
        return
    if num == 1:
        print u"第%d个人拿到红包数为：%.2f" %(num, total)
        return
    i = 1 
    total_money = total
    #rtotal = (total*100 - min*num*100)/100
    while( i < num ):
        max = total_money - min*(num - i)
        k = int((num-i)/2)
        if num -i <= 2:
            k = num -i
        max = max/k
        monney = random.randint(int(min*100), int(max*100))
        monney = float(monney)/100
        total_money = total_money - monney
        print u"第%2d个人拿到红包金额为：%.2f, 余额为: %.2f" %(i, monney, total_money)
        i+=1
    print u"第%2d个人拿到红包金额为：%.2f, 余额为: %.2f" %(i, total_money, 0.0)
        
        
if __name__ == "__main__":
    total = sys.argv[1]
    num = sys.argv[2]
    calRandomValue(total, num)
    
    
