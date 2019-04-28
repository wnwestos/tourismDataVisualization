import json
import random
for x in [9,8,7,6,5,4,3,2,1]:
    rd = round(random.random())
    if x == 9:
        name = 'heatPoint201{}.json'.format(x)
    else:
        if rd == 0:
            name = 'heatPoint201{}.json'.format(x)
        else:
            name = 'heatPoint201{}.json'.format(x+1)
    with open(name) as fo:
        data = json.load(fo)
        for i in data:
            value = i['value']
            rd = round(random.random())
            if value < 20 and rd == 1:
                i['value'] = value -1
            if value >= 20 and value < 50 and rd == 0:
                i['value'] = value -1
            if value >= 50 and value < 100 and rd == 1:
                i['value'] = value -3
            if value >= 100 and value < 150 and rd == 0:
                i['value'] = value -2
            if value >= 150 and value < 200 and rd == 1:
                i['value'] = value -3
            if value >= 200 and rd == 1 :
                i['value'] = value -4

    print(data)
    name1 = 'heatPoint201{}.json'.format(x-1)
    with open(name1,'w') as fo1:
        json.dump(data, fo1)
