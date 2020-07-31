import numpy as np

from pytest_cases import parametrize


class BenchmarkChallenger(object):
    """ Represents the API that a challenger should implement to enter the benchmark """

    def fit(self, x, y):
        """ Implementors should train the model based on (x, y) """
        raise NotImplementedError()

    def predict(self, x):
        """ Implementors should return a numpy array of predictions. """
        raise NotImplementedError()


class PolyFitChallenger(BenchmarkChallenger):
    """ A benchmark challenger implementation relying on np.polyfit """
    def __init__(self, degree):
        self.coefs = None
        self.degree = degree

    def __str__(self):
        return "NumpyPolyfit(degree=%i)" % self.degree

    def fit(self, x, y):
        self.coefs = np.polyfit(x, y, deg=self.degree)

    def predict(self, x):
        all_x_powers = np.c_[[x ** d for d in range(self.degree, -1, -1)]]
        predictions = self.coefs.dot(all_x_powers)
        return predictions


@parametrize(degree=[1, 2])
def algo_polyfit(degree):
    """ The two challengers based on polyfit, to be injected in the benchmark. """
    return PolyFitChallenger(degree=degree)
