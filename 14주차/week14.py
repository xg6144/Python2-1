with open('sales.txt','r',encoding='utf-8') as file:
    sales_list=[]
    for line in file:
        sales_list.append(line.rstrip('\n'))

a_list=[]

a0 = sales_list[1]
a_list.append(a0)
a1 = sales_list[3]
a_list.append(a1)
a2 = sales_list[5]
a_list.append(a2)

a_list=list(map(int,a_list))

x0 = sum(a_list) # 총 매출
x1 = sum(a_list)/3 #매출 평균

with open('sales_amount.txt','w',encoding='utf-8') as file:
    file.write("총 매출은 %d 이고, 매출 평균은 %d 입니다." % (x0,x1))