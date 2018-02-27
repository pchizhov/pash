import math


def divide(string):
    word = ''
    word_list = []
    for i in range(len(string)):
        if string[i] != ' ':
            word += string[i]
        else:
            word_list.append(word)
            word = ''
    word_list.append(word)
    return word_list


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.table = [[], [], [], [], [], [], []]
        self.p_good = 0
        self.p_maybe = 0
        self.p_never = 0

    def fit(self, x, y):
        """ Fit Naive Bayes classifier according to x, y. """
        good, maybe, never = 0, 0, 0
        for i in range(len(y)):
            if y[i] == 'good':
                y[i] = 1
                good += 1
            elif y[i] == 'maybe':
                y[i] = 2
                maybe += 1
            elif y[i] == 'never':
                y[i] = 3
                never += 1
        self.p_good = good / (good + maybe + never)
        self.p_maybe = maybe / (good + maybe + never)
        self.p_never = never / (good + maybe + never)

        for i in range(len(x)):
            words = divide(x[i])
            for word in words:
                if word in self.table[0]:
                    self.table[y[i]][self.table[0].index(word)] += 1
                else:
                    self.table[0].append(word)
                    self.table[y[i]].append(1)
                    self.table[y[i] % 3 + 1].append(0)
                    self.table[(y[i] % 3 + 1) % 3 + 1].append(0)
                    self.table[4].append(0)
                    self.table[5].append(0)
                    self.table[6].append(0)

        n_good = sum(self.table[1])
        n_maybe = sum(self.table[2])
        n_never = sum(self.table[3])
        dim = len(self.table[0])

        for i in range(len(self.table[0])):
            self.table[4][i] = (self.table[1][i] + self.alpha) / (n_good + self.alpha * dim)
            self.table[5][i] = (self.table[2][i] + self.alpha) / (n_maybe + self.alpha * dim)
            self.table[6][i] = (self.table[3][i] + self.alpha) / (n_never + self.alpha * dim)

    def predict(self, x):
        """ Perform classification on an array of test vectors X. """
        labels = []
        for string in x:
            string_good = math.log(self.p_good)
            string_maybe = math.log(self.p_maybe)
            string_never = math.log(self.p_never)
            words = divide(string)
            for word in words:
                if word in self.table[0]:
                    string_good += math.log(self.table[4][self.table[0].index(word)])
                    string_maybe += math.log(self.table[5][self.table[0].index(word)])
                    string_never += math.log(self.table[6][self.table[0].index(word)])
                else:
                    string_good += 0
                    string_maybe += 0
                    string_never += 0
            probability = max(string_good, string_maybe, string_never)
            if string_good == probability:
                labels.append('good')
            elif string_maybe == probability:
                labels.append('maybe')
            else:
                labels.append('never')
        return labels

    def score(self, x_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        prediction = self.predict(x_test)
        count = 0
        for i in range(len(prediction)):
            if prediction[i] == y_test[i]:
                count += 1
        score = count / len(y_test)
        return score
