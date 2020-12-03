import json

def load_parameters(filename):
    params = []
    with open(filename, 'r') as f:
        for jsonObj in f:
            param = json.loads(jsonObj)
            params.append(param)
    e = {}
    s = []
    o = []
    trans = {}
    for param in params:
        prev = None
        for a, b in param:
            if a not in o:
                o.append(a)
            if b not in s:
                s.append(b)
                e[b] = {}
                trans[b] = {}
            if a not in e[b]:
                e[b][a] = 0
            e[b][a] += 1
    
            if prev is not None:
                if b not in trans[prev[1]]:
                    trans[prev[1]][b] = 0
                trans[prev[1]][b] += 1
            prev = [a, b]
            
    for state in e:
        n = sum(e[state].values())
        for word in o:
            if word in e[state]:
                e[state][word] /= n
            else:
                e[state][word] = 0
    for state in trans:
        n = sum(trans[state].values())
        for next_state in s:
            if next_state in trans[state]:
                trans[state][next_state] /= n
            else:
                trans[state][next_state] = 0
    return e, s, trans

if __name__ == "__main__":
    e,s,trans = load_parameters('twt.dev.json')
    #print(s)
    print(e['V']['watching'])
    #print(trans['V'])
