import sys
filename = sys.argv[-1]
print filename
REF=""
net = {}
part = []


with open(filename,'r') as fi:
     for line in fi:
         if line[:4]=="BODY" or line[:3]=="END":
             continue
         if line[0]==' ':
             line = REF+line
             l = line.split()
         else:
             l = line.split()
             REF=l[0]
             del l[1]
         part.append(l)
         print l
         if not(l[2] in net):
             net[l[2]]=[]
         net[l[2]].append((l[0],l[1]))

         #fo.write(','.join(l)+'\n')
print net



