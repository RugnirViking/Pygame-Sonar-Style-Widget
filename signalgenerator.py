import random

tlist = []
for x in range(0,300):
    tlist.append(random.randrange(0,9))

for x, val in enumerate(tlist):
   total = 0
   count = 0
   if x>0:
       total+=tlist[x-1]
       count+=1
   if x<len(tlist)-1:
       total+=tlist[x+1]
       count+=1
   total+=val
   count += 1

   tlist[x] = int(total/count)

print(tlist)