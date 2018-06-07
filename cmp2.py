# Page to page parts compare

import os

file1 = "soraka_pvt.net"
file2 = "slate.net"

PATH1 = "../ee/poppy.dev/soraka_mlb_pvt/worklib/soraka_mlb_pvt/sch_1"
PATH2 = "../ee/poppy/soraka_mlb_pvt/worklib/soraka_mlb_pvt/sch_1"
pagemap={}
for n in range(45):
    pagemap[n+1]=n+1


##################### SORAKA VS LUX ########
# Page for PATH1 -> page for PATH2
if True:
    file1 = "soraka_pvt.net"
    file2 = "lux_dvt.net"
    
    PATH1 = "../ee/poppy/soraka_mlb_pvt/worklib/soraka_mlb_pvt/sch_1"
    PATH2 = "../ee/poppy/lux_mlb_dvt/worklib/lux_mlb_dvt/sch_1"

    pagemap[44]=45
    pagemap[45]=47
##################### SORAKA VS LUX ########

def pageread(path):
    
    csv_files=[]

    for file in os.listdir(path):
        if file.endswith(".csv"):
            csv_files.append(os.path.join(path, file))

    pages={}

    for file in csv_files:
        page = int(file.split('page')[1].split('.')[0])
        pages[page]={}
        with open(file, 'r') as fi:
            for line in fi:
                if line[0:4]=="$LOC" or line[0:4]=="LOCA":
                    part = line.split('"')[1]
                    for line in fi:
                        if line[0:10]=="JEDEC_TYPE":
                            jedec = line.split('"')[1]
                            break
                    for line in fi:
                        if line[0:5]=="VALUE":
                            value = line.split('"')[1]
                            pages[page][part]="{}_{}".format(jedec, value)
                            break

    return pages


def netread(filename):
    np=0
    with open(filename,'r') as fi:
        netlist={}  # net: [ref.pin, ...]
        sch={}      # sch: {ref:{pin: net, ...}, ...}
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
             
             if not(l[2] in netlist):
                 netlist[l[2]]=[]

             if not(l[0] in sch):
                 sch[l[0]]={}
                 
             netlist[l[2]].append("{}.{}".format(l[0],l[1]))
             
             sch[l[0]][l[1]]=l[2]
             np+=1

    for net in netlist.keys():
        netlist[net].sort()

    print "<{}>".format(filename)
    print "  Number of Parts: ", len(sch)
    print "  Number of Pins: ", np
    print "  Number of Nets: ", len(netlist)

    return netlist, sch

def pages_to_parts(pages):
    parts={}
    for _, pg in pages.items():
        for ref, val in pg.items():
            parts[ref]=val
    return parts

pages_sch1 = pageread(PATH1)
pages_sch2 = pageread(PATH2)

parts_sch1 = pages_to_parts(pages_sch1)

print "Number of page ({})= {}".format(PATH1.split('/')[-2], len(pages_sch1))
print "Number of page ({})= {}".format(PATH1.split('/')[-2], len(pages_sch2))

netlist1, sch1 = netread(file1)
netlist2, sch2 = netread(file2)

ref = "U47"
pins=sch1[ref]
for pin,net in pins.items():
    if not net in ["GND"]:
        print "{}.{} [{}]:".format(ref,pin,net)
        connected_parts = []
        
        for ref_pin in netlist1[net]:
            if ref_pin[0] in ['R', 'C']:
                ref=ref_pin.split('.')[0]
                part = parts_sch1[ref]
                connected_parts.append(part)
            else:
                connected_parts.append(ref_pin)

                
        print "  ", connected_parts
            


     


