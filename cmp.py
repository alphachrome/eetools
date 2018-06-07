# Page to page parts compare

import os

PATH1 = "../ee/poppy.dev/soraka_mlb_pvt/worklib/soraka_mlb_pvt/sch_1"
PATH2 = "../ee/poppy/soraka_mlb_pvt/worklib/soraka_mlb_pvt/sch_1"
pagemap={}
for n in range(45):
    pagemap[n+1]=n+1


##################### SORAKA VS LUX ########
# Page for PATH1 -> page for PATH2
if True:
    PATH2 = "../ee/poppy/lux_mlb_dvt/worklib/lux_mlb_dvt/sch_1"
    PATH1 = "../ee/poppy/soraka_mlb_pvt/worklib/soraka_mlb_pvt/sch_1"

    pagemap[44]=45
    pagemap[45]=47
##################### SORAKA VS LUX ########



def read(path):
    
    csv_files=[]

    for file in os.listdir(path):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(path, file))

    pages={}

    for file in csv_files:
        page = int(file.split('page')[1].split('.')[0])
        pages[page]=[]
        with open(file, 'r') as fi:
            for line in fi:
                if line[0:4]=="$LOC" or line[0:4]=="LOCA":
                    part = line.split('"')[1]
                    pages[page].append(part)

    return pages

pages_sch1 = read(PATH1)
pages_sch2 = read(PATH2)

print "Number of page ({})= {}".format(PATH1.split('/')[-2], len(pages_sch1))
print "Number of page ({})= {}".format(PATH1.split('/')[-2], len(pages_sch2))

nd=0
for n1, n2 in pagemap.items():
    pg_sch1 = pages_sch1[n1]
    pg_sch2 = pages_sch2[n2]

    add_parts = []
    
    for ref in pg_sch1:
        if not (ref in pg_sch2):
            add_parts.append(ref)
            nd+=1

    del_parts = []
    for ref in pg_sch2:
        if not (ref in pg_sch1):
            del_parts.append(ref)
            nd+=1

    if len(add_parts)+len(del_parts):
        print "Page {}:".format(n1)
        if len(add_parts):
            print "  +", add_parts
        if len(del_parts):
            print "  -", del_parts
            
print "Total diff found: ", nd
