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
        self.labels = []
        self.table = []
        self.p_labels = []

    def fit(self, x, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.labels = [i for i in set(y)]
        self.labels.sort()
        classes = len(self.labels)
        labels_count = [0] * classes
        for i in range(len(y)):
            y[i] = self.labels.index(y[i]) + 1
            labels_count[y[i] - 1] += 1

        self.table = [[] for _ in range(classes * 2 + 1)]
        self.p_labels = [math.log(number / sum(labels_count)) for number in labels_count]

        for i in range(len(x)):
            words = divide(x[i])
            for word in words:
                if word in self.table[0]:
                    self.table[y[i]][self.table[0].index(word)] += 1
                else:
                    self.table[0].append(word)
                    self.table[y[i]].append(1)
                    index = y[i]
                    for j in range(classes - 1):
                        index = (index % classes) + 1
                        self.table[index].append(0)
                    for column in range(classes + 1, classes * 2 + 1):
                        self.table[column].append(0)

        sums = [sum(self.table[i + 1]) for i in range(classes)]
        dim = len(self.table[0])

        for line in range(dim):
            for column in range(classes + 1, classes * 2 + 1):
                self.table[column][line] = (self.table[column - classes][line] + self.alpha) / \
                                           (sums[column - classes - 1] + self.alpha * dim)

    def predict(self, x):
        """ Perform classification on an array of test vectors X. """
        labels = []
        classes = len(self.labels)
        for string in x:
            string_labels = [i for i in self.p_labels]
            words = divide(string)
            for word in words:
                if word in self.table[0]:
                    for i in range(classes):
                        string_labels[i] += math.log(self.table[i + classes + 1][self.table[0].index(word)])
            for i in range(classes):
                if string_labels[i] == max(string_labels):
                    labels.append(self.labels[i])
                    break
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
