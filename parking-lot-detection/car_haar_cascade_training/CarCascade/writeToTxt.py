import os
#write to txt file all file path
path = 'C:\\Users\\BAG\\Desktop\\CarCascade\\OwnCollection\\caryok\\non-car\\'

fac= open('C:\\Users\\BAG\\Desktop\\CarCascade\\OwnCollection\\caryok\\non-car\\bg.txt', 'w+')
files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.png' in file:
            files.append(os.path.join(r, file))


for f in files:
    fac.write(f+"\n")


