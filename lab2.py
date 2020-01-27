import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
 
#русскоязычные подписи на графиках
rcParams['font.family']='sans-serif'
rcParams['font.fantasy']='Arial'
 
Pi=[0.2599,0.2638,0.5499,0.5132,0.1839]
n=[1,2,3,4,5]

def polnoe_dublirovanie(pi,ni): #вероятность отказа системы с полным дублированием
    p_otk_pdubl = []
    pr=1-pi[0]
    for i in range(len(pi)-1):
        pr=pr*(1-pi[i+1])
    for j in range(len(ni)):
        p_otk_pdubl.append((1-pr)**ni[j])
    return p_otk_pdubl
 
def dulirovanie_sys(pi,ni): #вероятность отказа системы с дублированием подсистем
    p_otk_dubsys=[]
    for j in range(len(ni)):
        pr=1-(pi[0]**ni[j])
        for i in range(len(pi)-1):
            pr=pr*(1-(pi[i+1]**ni[j]))
        p_otk_dubsys.append((1-pr))
    return p_otk_dubsys
 
def polnoe_dublirovanie_practica(pi,ni): #система с полным дублированием моделирование работы системы с полным дублированием
    massiv1=[]
    #для нескольких блоков
    for block in range(len(ni)):
        otkaz=0
        iterations=0
        if block==0:
            p_ver=np.array([pi])
        else: 
            p_ver=np.insert(p_ver,block,p_ver[block-1],axis=0)
        while otkaz<10000:
            flag = False
            for row in range(ni[block]): #по кол-ву блоков
                for element in range(5): #по подсистем
                    random_value = np.random.sample()
                    if row == ni[block]-1: #проверка, что блок последний
                        if random_value<p_ver[row][element]: #проверка по значению
                            otkaz += 1
                            iterations+=1
                            flag = True
                            break
                        elif element == 4: #если if не выполнялся, то на последней подсистеме сюда
                            iterations+=1
                        else: continue
                    elif row != ni[block] - 1: #если блок НЕ последний
                        if random_value < p_ver[row][element]: #проверка по значению
                            break
                        elif element == 4: #если if не выполнялся, то на последней подсистеме сюда
                            iterations += 1
                            flag = True
                            break
                        else: continue
                if flag:
                    break
        massiv1.append(otkaz/iterations)
    return massiv1
 
def dulirovanie_sys_practica(pi,ni): #моделирование работы системы с дублированием подсистем для нескольких блоков
    massiv2=[]
    #для нескольких блоков
    for block in range(len(ni)):
        otkaz=0
        iterations=0
        if block==0:
            p_ver=np.array([pi])
        else: 
            p_ver=np.insert(p_ver, block, p_ver[block-1], axis=0)
        check_size=p_ver.shape
        check_size=check_size[0]
        while otkaz<10000:
            flag=False
            row=0 #изначально блоков
            for i in range(5): # по количеству подсисистем
                random_value=np.random.sample()
                if random_value<p_ver[row][i]:
                    if check_size!=1: #проверка, что блоков не 1
                        for duplication in range(check_size-1): #дублирование по количеству блоков
                            random_value=np.random.sample()
                            if random_value<p_ver[row][i]:
                                if duplication==check_size - 2: #так как один блок проверили изначальо, то до минус 2
                                    otkaz+=1
                                    iterations+=1
                                    flag=True
                                    break
                                else: 
                                    continue
                            else:
                                if i==4:
                                    iterations+=1
                                break
                    else: #если блок был 1
                        otkaz+=1
                        iterations+=1
                        flag=True
                        break
                elif i==4:
                    iterations+=1
                    flag=True
                    break
                else:
                    continue          
                if flag:
                    break
        massiv2.append(otkaz/iterations)
    return massiv2
 
P1_teor=polnoe_dublirovanie(Pi,n)
P1_pract=polnoe_dublirovanie_practica(Pi,n)
P2_teor=dulirovanie_sys(Pi,n)
P2_pract=dulirovanie_sys_practica(Pi, n)
#P_teor=teoreticheskoe(Pi,n)
 
print('Значения полного дублирования')
print('Теоретическое|Практическое')
for i in range(len(P1_teor)):
    print(round(P1_teor[i],4),'|',round(P1_pract[i],4))
print("") 
print('Значения с дублирование блоков')
print('Теоретическое|Практическое')
for i in range(len(P2_teor)):
    print(round(P2_teor[i],4),'|',round(P2_pract[i],4))   
 
 
fig = plt.figure(1)
ax1 = fig.add_axes([0,1.2,1,1])
ax1.grid(True, color = [0,0,0], lw = 2)
ax1.set_title('График зависимости отказоустойчивости системы от количества блоков',fontsize=18,color='black')
ax1.plot(n, P1_pract, color='r', label='Полное дублирование (практическое)')
ax1.scatter(n, P1_teor, color=[0,1,0], label='Полное дублирование (теоретическое)',s=100)
ax1.plot(n, P2_pract, color='b', label='Дублирование подсистем(практическое)')
ax1.scatter(n, P2_teor, color=[1,0,1], label='Дублирование подсистем(теоретическое)',s=100) 
ax1.set_ylabel('Вероятность отказа', fontsize = 15, color = 'black')
ax1.set_xlabel('Количество блоков', fontsize = 15, color = 'black')
ax1.legend(loc=0, shadow=True, fontsize=13)
fig.savefig('lab5_1.png', bbox_inches='tight')
