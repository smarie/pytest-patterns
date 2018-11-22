from collections import OrderedDict
from math import ceil

import numpy as np
import pandas as pd

from tabulate import tabulate

import pytest

from pytest_cases import cases_fixture
from pytest_steps import test_steps, get_flattened_multilevel_columns, pivot_steps_on_df, \
    get_all_pytest_param_names_except_step_id, handle_steps_in_synthesis_dct
from pytest_harvest import get_session_synthesis_dct, create_results_bag_fixture


from pytest_patterns.data_science_benchmark import test_polyfit_cases


# ------------- To plot things along the way ------------
class SubPlotsManager(object):
    def __init__(self, nb_subplots):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, ceil(nb_subplots / 2), figsize=(25, 20))
        self.nb_subplots = nb_subplots
        self.cur_subplot = 0
        self.ax = ax

    def get_next_subplot(self):
        i = self.cur_subplot
        self.cur_subplot += 1
        return self.ax[i % 2][i // 2]

    def finalize_plots(self, title):
        import matplotlib.pyplot as plt
        f = plt.gcf()
        f.suptitle(title)
        f.set_size_inches(15, 20)
        plt.show()


@pytest.fixture(scope='session')
def plots_manager():
    """The fixture containing the axes where to plot"""

    nb_subplots_to_do = len(dataset._pytestfixturefunction.params)
    plt_mgr = SubPlotsManager(nb_subplots_to_do)
    yield plt_mgr
    plt_mgr.finalize_plots("Fitting Anscombe's quartet + other files with polynomial models")


colors = ['orange', 'maroon']


# ------------- To collect datasets ------------
@cases_fixture(module=test_polyfit_cases, scope='session')
def dataset(case_data, plots_manager):
    """
    Note: we use "scope=session" so that this method is called only once per case.
    This ensures that each file is read once, and each plot is done once as well.

    We could reach the same result by using lru_cache in the case function, but since
    we have several case functions it would be more cumbersome to do.
    """
    # get the dataset
    x, y = case_data.get()

    # plot it
    ax = plots_manager.get_next_subplot()
    ax.plot(x, y, 'o', color='gray', label='data')
    ax.set_title(str(case_data))

    return x, y, ax


# ------------- To collect benchmark results ------------
@pytest.fixture(autouse=True, scope='session')
def store():
    """The store where we will put our results_bag fixture"""
    yield OrderedDict()


results_bag = create_results_bag_fixture('store', name='results_bag')
"""The fixture where we will put all our benchmark results"""


# ------------- To evaluate the algorithms ------------
@test_steps('fit', 'predict', 'eval', 'plot')
@pytest.mark.parametrize('degree', [1, 2], ids=lambda d: "degree=%s" % d)
def test_poly_fit(dataset, degree, results_bag):
    """Tests the polyfit function from numpy on the provided case_data """

    # Get the test case at hand
    x, y, ax = dataset

    # Fit the model using polyfit
    model_coefs = np.polyfit(x, y, deg=degree)
    yield 'fit'

    # Use the model to perform predictions
    all_x_powers = np.c_[[x**d for d in range(degree, -1, -1)]]
    predictions = model_coefs.dot(all_x_powers)
    yield 'predict'

    # Evaluate the prediction error
    cvrmse = np.sqrt(np.mean((predictions-y)**2)) / np.mean(y)
    print("Relative error (cv-rmse) is: %.2f%%" % (cvrmse * 100))
    results_bag.cvrmse = cvrmse
    yield 'eval'

    # Plot the predictions
    ax.plot(x, predictions, 'x', color=colors[degree - 1],
            label='degree=%i (CVRMSE=%.2f%%))' % (degree, cvrmse * 100))
    ax.legend()
    yield 'plot'


# ------------- To create the final benchmark table ------------
def test_synthesis(request, store):
    """ Note: we could do this at many other places (hook, teardown of a session-scope fixture...) """

    # Get session synthesis filtered on the test function of interest, combined with our store
    results_dct = get_session_synthesis_dct(request.session, filter=test_synthesis.__module__,
                                            durations_in_ms=True,
                                            status_details=False, fixture_store=store,
                                            flatten=True, flatten_more='results_bag')
    # separate test id from step id when needed
    results_dct = handle_steps_in_synthesis_dct(results_dct, is_flat=True)

    # convert to a pandas dataframe
    results_df = pd.DataFrame.from_dict(results_dct, orient='index')
    results_df = results_df.loc[list(results_dct.keys()), :]          # fix rows order
    results_df.index.names = ['test_id', 'step_id']                   # set index name
    results_df.drop(['pytest_obj'], axis=1, inplace=True)             # drop pytest object column

    # pivot: we want one row per test, describing all steps at once (in columns)
    param_names = get_all_pytest_param_names_except_step_id(request.session, filter=test_synthesis.__module__)
    report_df = pivot_steps_on_df(results_df, cross_steps_columns=param_names)

    # print using tabulate
    report_df.columns = get_flattened_multilevel_columns(report_df)
    print("\n" + tabulate(report_df, headers='keys'))
