import sys

def find(line):
    result=[]
    for item in sephora:
        if similar(item, line):
            result.append(sephora[item])
    for item in belk:
        if similar(item, line):
            result.append(belk[item])
    return result

def similar(item, line):
    if len(item)<len(line):
        return similar(line, item)
    total=len(item)
    same=sum(item[i]==line[i] for i in range(0, len(line)))
    if float(same)/float(total)>0.75:
        return True
    return False

def update(name, line, dict):
    dict[name]=line
    print line

def suggest(price, name):
    results=[]
    for item in sephora:
        p=sephora[item][2][1:sephora[item][2].index(".")]
        if int(p) <= price:
            results.append(sephora[item])
    return results


sephora={}
with open('sephora.txt', 'rU') as f1:
    for line in f1.readlines():
        parts=line.split('\t')
        newline=[]
        for p in parts:
            newline.append(p)
        name='('+parts[0]+')+('+parts[1]+')'
        sephora[name]=newline

belk={}
with open('belk.txt', 'rU') as f2:
    for line in f2.readlines():
        parts=line.split('\t')
        newline=[]
        for p in parts:
            newline.append(p)
        name = parts[0] + '\t' + parts[1]
        belk[name] = newline

print "please enter brand and name"
brand=sys.argv[1]
name=sys.argv[2]
combine='('+brand+')+('+name+')'
print find(combine)

print '\n'

tmp=sys.argv[3]
price=int(sys.argv[4])
result=suggest(price, tmp)
for line in result:
    # print line
    # print '\n'
    print ("%20s\t%50s\t%10s") % (line[0], line[1], line[2])

