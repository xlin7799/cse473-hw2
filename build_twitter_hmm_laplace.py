import json


def load_parameters(train_filename, test_filename):
    params = []
    with open(train_filename, 'r') as f:
        for jsonObj in f:
            param = json.loads(jsonObj)
            params.append(param)

    e = {}
    s = ['<S>', 'N', 'O', 'S', '^', 'Z', 'L', 'M', 'V', 'A', 'R', '!', 'D', \
         'P', '&', 'T', 'X', 'Y', '#', '@', '~', 'U', 'E', '$', ',', 'G', '<E>']
    o = {}
    trans = {}
    for st in s:
        trans[st] = {}
        e[st] = {}
    for param in params:
        prev = None
        next = param[0][1]
        if next not in trans['<S>']:
            trans['<S>'][next] = 0
        trans['<S>'][next] += 1.0
        for a, b in param:
            if a not in o:
                o[a] = 0
            o[a] += 1

            if b not in e:
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
        if '<E>' not in trans[prev[1]]:
            trans[prev[1]]['<E>'] = 0
        trans[prev[1]]['<E>'] += 1.0

    # laplace smoothing
    af = 2.0
    with open(test_filename, 'r') as f:
        for jsonObj in f:
            param = json.loads(jsonObj)
            for a,b in param:
                if a not in o:
                    o[a] = af
                if a not in e[b]:
                    e[b][a] = 0.0

    o = [k for k, v in sorted(o.items(), key=lambda item: item[1], reverse=True)]
    for state in e:
        n = sum(e[state].values()) + af * len(e[state].values())
        for word in e[state]:
            e[state][word] = (e[state][word] + af) / n
    for state in trans:
        n = sum(trans[state].values())
        for next_state in s:
            if next_state == '<S>':
                continue
            if next_state in trans[state]:
                trans[state][next_state] /= n
            else:
                trans[state][next_state] = 0
    return s, o, trans, e


def write_parameters(filename, s, o, trans, e):
    with open(filename, 'w') as f:
        json.dump({'S': s, 'O': o, 'P_trans': trans, 'P_emission': e}, f, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    s, o, trans, e = load_parameters('twt.train.json', 'twt.test.json')
    write_parameters('twitter_pos_hmm_laplace.json', s, o, trans, e)
