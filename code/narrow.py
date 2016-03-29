import random

f = open('data_with_location.csv')
fin = open('data_narrow.csv','w')

for each in f:
    i = random.random()
    if i < 0.01:
        fin.write(each)

f.close()
fin.close()
