from random import choices


class Probability:

    def __init__(self, num_of_elements, weights):
        self.num_of_elements = num_of_elements
        self.weights = weights

    def draw_idx(self):
        return choices([i for i in range(self.num_of_elements)], self.weights)[0]
