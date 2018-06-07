import sys
filename = sys.argv[-1]
print filename


with open(filename,'r') as fi, open('_'+filename,'w') as fo:
     for line in fi:
         if line[:4]=="BODY" or line[:3]=="END":
             continue
         if line[0]==' ':
             line = ':'+line[1:]
             l = line.split()
         else:
             l = line.split()
             del l[1]
         #print l
         fo.write(','.join(l)+'\n')
