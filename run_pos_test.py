from hmm import HMM
import json
import sys

def get_hmm_prediction(filename, test_filename):
    model = HMM(filename)
    params = []
    total = 0.0
    correct = 0.0
    with open(test_filename, 'r') as f:
        for jsonObj in f:
            param = json.loads(jsonObj)
            total += len(param)
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
                correct += 1.0
    return total, correct

if __name__ == '__main__':
    filename = 'twitter_pos_hmm.json'
    laplace_filename = 'twitter_pos_hmm_laplace.json'
    test_filename = 'twt.test.json'
    total_count, correct_count = get_hmm_prediction(filename, test_filename)
    print("1. Nuo Chen, Xin Lin")
    print("2. Original HMM parameters:")
    print("    a. Total count of correctly tagged words in the test data: ", correct_count)
    print("    b. Total count of words in the test data: ", total_count)
    print("    c. Percentage correct (calculated from the previous two values): ", round(100.0 * (correct_count / total_count), 2))

    if len(sys.argv) == 2 and sys.argv[1] == "True":
        print("3. HMM parameters with Laplace smoothing:")
        total_count, correct_count = get_hmm_prediction(laplace_filename, test_filename)
        print("    a. Total count of correctly tagged words in the test data: ", correct_count)
        print("    b. Total count of words in the test data: ", total_count)
        print("    c. Percentage correct (calculated from the previous two values): ",round(100.0 * (correct_count / total_count), 2))
    print("4. Something you learned doing this assignment:")
    print("    It is very cool to use a model we created to predict the words type! We have a better understanding "
          "about the HMM model and a new method - laplace smoothing")
    print("5. Biggest challenge you faced doing this assignment:")
    print("    The biggest challenge is understanding the structure of existing code")
    # hv.hold()
