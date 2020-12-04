"""HMM_Algorithms.py

by Nuo Chen, Xin Lin

date: 12/03/2020

for CSE 473 Project Option 2, Autumn 2020
University of Washington

Provide your own implementations of the Forward algorithm and the Viterbi
algorithm in the provided function templates.

Your Forward algorithm should compute the belief vector B_t at each point t in
time. Here B_t(s) = P(S_t=s | E_1=e_1, E_2=e_2, ..., E_t=e_t). Here E_t
represents the emission at time step t. When show is True, it should display 
the belief values next to each of the nodes.

Your Viterbi algorithm should for each node compute the probability of reaching
that node from the start along the most probable path. When show is True, it
should display this probability next to each of the nodes, and it should
highlight the (or a) most probable path.
"""

import json

import hmm_vis as hv

RAD = 20

class HMM:
    """ class that represents an HMM model with functions for the Forward and
        Viterbi algorithms """

    def __init__(self, filename=None):
        """ initialize parameters and other helper variables """
        self.S = None
        self.O = None
        self.P_trans = None
        self.P_emission = None
        if filename is not None:
            self.load_parameters(filename)
        # Add other instance variables you might need below.

    def load_parameters(self, filename):
        """ load HMM model parameters from JSON file """
        with open(filename, 'r') as f:
            parameters = json.load(f)
        self.S = parameters['S']
        self.O = parameters['O']
        self.P_trans = parameters['P_trans']
        self.P_emission = parameters['P_emission']

    def forward_algorithm(self, obs_sequence, show=False):

        if show:
            hv.show_entire_trellis(self.S, obs_sequence,
                                   has_initial_state=True)
            # Demo of node highlighting.
            #hv.highlight_node(0, '<S>', highlight=True)
            # highlight/unhighlight other nodes as appropriate
            # to show progress.

        # Put your code implementing the Forward algorithm here. When
        # debugging, use calls to highlight_node and show_node_label to
        # illustrate the progress of your algorithm.
        b = []
        states = self.S[1:-1]
        n = len(states)
        b1 = []
        for i in range(n):
            prob = self.P_trans['<S>'][states[i]]
            prob = self.getProb(prob, obs_sequence, states, 0, i)
            b1.append(prob)
            if show:
                hv.highlight_node(1, states[i], highlight=True)
                hv.show_label_at_node(1,states[i], str(prob), dy=1.5*RAD, color='red')
                hv.highlight_node(1, states[i], highlight=False)
        b.append(b1)
        for i in range(1, len(obs_sequence)):
            bt = []
            for j in range(n):
                prob = sum([b[-1][k]*self.P_trans[states[k]][states[j]] for k in range(n)])
                prob = self.getProb(prob, obs_sequence, states, i, j)
                bt.append(prob)
                if show:
                    hv.highlight_node(i+1, states[j], highlight=True)
                    hv.show_label_at_node(i+1,states[j], str(prob), dy=1.5*RAD, color='red')
                    hv.highlight_node(i+1, states[j], highlight=False)
            b.append(bt)
        print(b)
        return b

    def getProb(self, prob, obs_sequence, states, i, j):
        contain = False
        for k, v in self.P_emission[states[j]].items():
            if obs_sequence[i].lower() == k.lower():
                contain = True
                prob *= v
        if not contain:
            return 0.0
        return prob

    def viterbi_algorithm(self, obs_sequence, show=False):
        if show:
            hv.show_entire_trellis(self.S, obs_sequence,
                                   has_initial_state=True)
            hv.highlight_node(0, '<S>')         # Demo of node highlighting.
            #hv.highlight_edge(0, '<S>', 'M')    # Demo of edge highlighting.
            # highlight other nodes and edges as appropriate
            # to show progress and results.

        # Put your code implementing the Viterbi algorithm here. When
        # debugging, use calls to highlight_node and show_node_label to
        # illustrate the progress of your algorithm.
        seqs = []
        states = self.S[1:-1]
        n = len(states)
        for i in range(n):
            prob = self.P_trans['<S>'][states[i]]
            prob = self.getProb(prob, obs_sequence, states, 0, i)
            seqs.append([prob, [states[i]]])

        for i in range(1, len(obs_sequence)):
            new_seqs = []
            for j in range(n):
                trans = [seqs[k][0]*self.P_trans[states[k]][states[j]] for k in range(n)]
                ind = 0
                prob = max(trans)
                for idx,e in enumerate(trans):
                    if e == prob:
                        ind = idx
                        break

                prob = self.getProb(prob, obs_sequence, states, i, j)
                best = [prob, seqs[ind][1].copy()]
                best[1].append(states[j])
                new_seqs.append(best)
            seqs = new_seqs
        seqs = sorted(seqs, key = lambda x: x[0])
        print(seqs)
        ret = seqs[-1][1]
        #ret.append('<E>')
        if show:
            hv.highlight_edge(0, '<S>', ret[0])
            hv.highlight_node(1, ret[0])
            for i in range(1, len(ret)):
                hv.highlight_node(i+1, ret[i])
                hv.highlight_edge(i, ret[i-1], ret[i])
            hv.highlight_node(len(ret), '<E>')
            hv.highlight_edge(len(ret), ret[-1], '<E>')
        ret.insert(0, '<S>')
        ret.append('<E>')
        return ret



if __name__ == '__main__':
    sample_obs_seq = ['Jane', 'will', 'spot', 'Will']
    model = HMM('toy_pos_tagger.json')
    beliefs = model.forward_algorithm(sample_obs_seq, show=True)
    #hv.hold()
    state_seq = model.viterbi_algorithm(sample_obs_seq, show=True)
    hv.hold()
