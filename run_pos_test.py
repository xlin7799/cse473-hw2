from hmm import HMM
import json

import hmm_vis as hv

RAD = 20

if __name__ == '__main__':
    filename = 'twitter_pos_hmm.json'
    test_filename = 'twt.test.json'
    # sample_obs_seq = ['Jane', 'will', 'spot', 'Will']
    model = HMM(filename)
    params = []
    total_count = 0.0
    correct_count = 0.0
    with open(test_filename, 'r') as f:
        for jsonObj in f:
            param = json.loads(jsonObj)
            total_count += len(param)
            params.append(param)

    for param in params:
        sample_obs_seq = []
        correct_tag = []
        for a, b in param:
            sample_obs_seq.append(a)
            correct_tag.append(b)
        state_seq = model.viterbi_algorithm(sample_obs_seq, show=False)
        for i in range(len(state_seq)):
            if state_seq[i] == correct_tag[i]:
                correct_count += 1.0
    print("1. Nuo Chen, Xin Lin")
    print("2. Original HMM parameters:")
    print("    a. Total count of correctly tagged words in the test data: ", correct_count)
    print("    b. Total count of words in the test data: ", total_count)
    print("    c. Percentage correct (calculated from the previous two values): ", correct_count / total_count)

    # hv.hold()