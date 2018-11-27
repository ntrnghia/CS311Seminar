#cfg = {'S': {'P'}, 'P': {'aPb', 'e'}} #result not short as expected
#cfg = {'S': {'ASB'}, 'A': {'aAS', 'a', 'e'}, 'B': {'SbS', 'A', 'bb'}} #good ex
#cfg = {'S': {'ABCd'}, 'A': {'BC'}, 'B': {'bB', 'e'}, 'C': {'cC', 'e'}} #exist non-reachable in result
#cfg = {'S': {'XA', 'BB'}, 'B': {'b', 'SB'}, 'X': {'b'}, 'A': {'a'}} #exist non-reachable in result
#cfg = {'S': {'Ab', 'Be', 'Df'}, 'A': {'a', 'S', 'C'},'C': {'c', 'BC', 'e'}, 'E': {'aA', 'e'}, 'D': {'aDc'}} #exist non-reachable in result
cfg = {'S': {'Aa'}, 'A': {'a', 'BC'}, 'P': {'APa', 'B'}, 'B': {'aBC'}} #goood ex
#cfg = {'S': {'aXbX'}, 'X': {'aY', 'bY', 'e'}, 'Y': {'X', 'c'}} #bug mulitiple X is e
#cfg = {'S': {'ASA', 'ab'}, 'A': {'B', 'S'}, 'B': {'b', 'e'}} #good ex
#cfg = {'S': {'S', 'XY'}, 'X': {'a'}, 'Y': {'Z', 'b'}, 'Z': {'M'}, 'M': {'N'}, 'N': {'a'}} #exist non-reachable in result
#cfg = {'S': {'aXbX', 'aXbXcX'}, 'X': {'aY', 'bY', 'e'}, 'Y': {'X', 'c'}} #waiting for fix e bug
#cfg = {'S': {'aSb', 'e'}}
#cfg = {'S': {'XY', 'Xn', 'p'}, 'X': {'mX', 'm'}, 'Y': {'Xn', 'o'}}
#cfg = {'S': {'ASA', 'aB'}, 'A': {'B', 'S'}, 'B': {'b', 'e'}}


def new():
    res=[]
    for i in range(26):
        res.append(False)
    for i in cfg:
        res[ord(i)-65]=True
    for i in range(26):
        if res[i] == False:
            return chr(i+65)
    return chr(65)


def get(a):
    for i in cfg:
        if cfg[i] == {a}:
            return i
    return new()


def remove_recur_forever():
    recur=set()
    for i in cfg.copy():
        if i == 'S':
            continue
        recur_forever=True
        for j in cfg[i]:
            if i not in j:
                recur_forever=False
        if recur_forever:
            del cfg[i]
            recur.add(i)
    for i in cfg:
        for j in cfg[i].copy():
            for k in j:
                if k < 'a' and k in recur:
                    cfg[i].remove(j)
    return len(recur) > 0


def remove_e():
    while(True):
        e=set()
        for i in cfg:
            for j in cfg[i].copy():
                if j == 'e':
                    e.add(i)
                    cfg[i].remove(j)
        if (len(e) == 0):
            break
        for i in cfg:
            for j in cfg[i].copy():
                for k in range(len(j)):
                    if j[k] in e:
                        if len(j) == 1:
                            if i != 'S':
                                cfg[i].add('e')
                        else:
                            cfg[i].add(j[:k]+j[k+1:])


def remove_unit_production():
    for i in cfg:
        is_found=True
        while(is_found):
            is_found=False
            for j in cfg[i].copy():
                if len(j) == 1 and j < 'a':
                    is_found=True
                    cfg[i].remove(j)
                    if (j != i):
                        if j in cfg:
                            for k in cfg[j]:
                                cfg[i].add(k)


def remove_useless():
    start=set()
    for i in cfg:
        start.add(i)
    is_found=True
    while(is_found):
        is_found=False
        for i in cfg.copy():
            for j in cfg[i].copy():
                for k in j:
                    if k < 'a' and k not in start:
                        is_found=True
                        if (len(cfg[i]) > 1):
                            cfg[i].remove(j)
                        else:
                            del cfg[i]
                            start.remove(i)
    print('1.3.1: Removed varibles that have no production')
    output()

    is_found=True
    while(is_found):
        is_found=remove_recur_forever()
    print('1.3.2: Removed varibles that recur forever')
    output()

    start={'S'}
    queue=['S']
    while(queue):
        i=queue.pop()
        for j in cfg[i]:
            for k in j:
                if k < 'a' and k not in start:
                    start.add(k)
                    queue.append(k)
    for i in cfg.copy():
        if i not in start:
            del cfg[i]
    for i in cfg:
        for j in cfg[i].copy():
            for k in j:
                if k < 'a' and k not in start:
                    cfg[i].remove(j)
    print('1.3.3: Removed varibles that non-reachable')
    output()


def remove_terminal():
    terminal={}
    for i in cfg.copy():
        for j in cfg[i]:
            for k in range(1, len(j)):
                if j[k] >= 'a':
                    if j[k] not in terminal:
                        terminal[j[k]]=get(j[k])
                        cfg[terminal[j[k]]]={j[k]}
                    cfg[i].remove(j)
                    cfg[i].add(j[:k]+terminal[j[k]]+j[k+1:])


def eleminate_left_recur():
    map={}
    n=0
    for i in cfg:
        map[i]=n
        n += 1
    for i in cfg.copy():
        is_found=True
        recur=set()
        while(is_found):
            is_found=False
            for j in cfg[i].copy():
                if j[0] < 'a':
                    if map[i] > map[j[0]]:
                        is_found=True
                        cfg[i].remove(j)
                        for k in cfg[j[0]]:
                            cfg[i].add(k+j[1:])
                    if map[i] == map[j[0]]:
                        cfg[i].remove(j)
                        recur.add(j[1:])
        if len(recur) > 0:
            k=new()
            for j in cfg[i].copy():
                cfg[i].add(j+k)
            cfg[k]=set()
            for j in recur:
                cfg[k].update({j, j+k})


def find_and_convert():
    for i in cfg:
        is_found=True
        while(is_found):
            is_found=False
            for j in cfg[i].copy():
                if j[0] < 'a':
                    is_found=True
                    cfg[i].remove(j)
                    for k in cfg[j[0]]:
                        cfg[i].add(k+j[1:])


def output():
    for i in cfg:
        print(i, end = '')
        for j in cfg[i]:
            print(' '+j, end = '')
        print()
    print()


print('Initial CFG')
output()

remove_e()
print('1.1: Removed e')
output()

remove_unit_production()
print('1.2: Removed unit production')
output()

remove_useless()

eleminate_left_recur()
print('2: Eliminated direct and indirect left recursion')
output()

remove_terminal()
print('3: Removed terminal')
output()

find_and_convert()
print('4. Became GNF')
output()
