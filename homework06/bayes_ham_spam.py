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
        self.table = [[], [], [], [], []]
        self.p_ham = 0
        self.p_spam = 0

    def fit(self, x, y):
        """ Fit Naive Bayes classifier according to X, y. """
        ham, spam = 0, 0
        for i in range(len(y)):
            if y[i] == 'ham':
                y[i] = 1
                ham += 1
            else:
                y[i] = 2
                spam += 1
        self.p_ham = ham / (ham + spam)
        self.p_spam = spam / (ham + spam)

        for i in range(len(x)):
            words = divide(x[i])
            for word in words:
                if word in self.table[0]:
                    self.table[y[i]][self.table[0].index(word)] += 1
                else:
                    self.table[0].append(word)
                    self.table[y[i]].append(1)
                    self.table[y[i] % 2 + 1].append(0)
                    self.table[3].append(0)
                    self.table[4].append(0)

        n_ham = sum(self.table[1])
        n_spam = sum(self.table[2])
        dim = len(self.table[0])

        for i in range(len(self.table[0])):
            self.table[3][i] = (self.table[1][i] + self.alpha) / (n_ham + self.alpha * dim)
            self.table[4][i] = (self.table[2][i] + self.alpha) / (n_spam + self.alpha * dim)

    def predict(self, x):
        """ Perform classification on an array of test vectors X. """
        labels = []
        for string in x:
            string_ham = math.log(self.p_ham)
            string_spam = math.log(self.p_spam)
            words = divide(string)
            for word in words:
                if word in self.table[0]:
                    string_ham += math.log(self.table[3][self.table[0].index(word)])
                    string_spam += math.log(self.table[4][self.table[0].index(word)])
                else:
                    string_ham += 0
                    string_spam += 0
            if string_ham < string_spam:
                labels.append('spam')
            else:
                labels.append('ham')
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
