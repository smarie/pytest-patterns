import numpy as np


class BenchmarkChallenger(object):
    """
    Represents the API that a challenger should implement to enter the benchmark
    """
    def fit(self, x, y):
        pass

    def predict(self, x):
        pass


class PolyFitChallenger(BenchmarkChallenger):
    """
    Represents a benchmark challenger implementation relying on np.polyfit
    """
    def __init__(self, degree):
        self.coefs = None
        self.degree = degree

    def __str__(self):
        return "polyfit(degree=%i)" % self.degree

    def fit(self, x, y):
        self.coefs = np.polyfit(x, y, deg=self.degree)

    def predict(self, x):
        all_x_powers = np.c_[[x ** d for d in range(self.degree, -1, -1)]]
        predictions = self.coefs.dot(all_x_powers)
        return predictions
