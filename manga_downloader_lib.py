import manga_downloader as md
library = open("lib.txt",'r')
position = library.readlines()
library.close()
lib = []
[lib.append(position[x].split(';')) for x in range(0,len(position))]
del position
pos = 1
for i in lib:
    print '/-- Sprawdzanie ' + i[0] + ' ['+ str(pos) +'/' + str(len(lib)) + ']'
    md.manga_fetch(i[0],i[1])
    print '\-- Zakonczono sprawdzanie ' + i[0]
    pos = pos + 1

