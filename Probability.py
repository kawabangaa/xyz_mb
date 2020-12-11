from random import choices
class Probability():

    def __init__(self, num_of_elements, weights):
        self.num_of_elements = num_of_elements
        self.weights = weights

    def increase(self, idx):
        self.weights[idx] += 1

    def decrease(self, idx):
        if self.weights[idx] > 0:
            self.weights[idx] -= 1

    def draw_idx(self):
        return choices([i for i in range(self.num_of_elements)], self.weights)

    def get_weights(self):
        out = []
        w_sum = sum(self.weights)
        for weight in self.weights:
            out.append(weight/w_sum * 100)
        return out
