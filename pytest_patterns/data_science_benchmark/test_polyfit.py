from collections import OrderedDict

import numpy as np
import pandas as pd

import pytest
from pytest_cases import cases_fixture
from pytest_harvest import get_session_synthesis_dct, create_results_bag_fixture
from pytest_harvest.results_bags import ResultsBag

from .challengers_polyfit import PolyFitChallenger
from . import datasets_polyfit


# ------------ The two challengers ----------
@pytest.fixture(params=[1, 2], ids="polyfit(degree={})".format)
def challenger(request):
    """
    A fixture creating the two challengers
    """
    return PolyFitChallenger(degree=request.param)


# ------------- To collect datasets ------------
@cases_fixture(module=datasets_polyfit, scope='session')
def dataset(case_data):
    """
    A fixture collecting all 'cases' (datasets) in `datasets_polyfit`.

    Note: we use "scope=session" so that this method is called only once per case.
    This ensures that each file is read once. We could reach the same result by using
    lru_cache in the case function, but since we have several case functions it would
    be more cumbersome to do.
    """
    # get the dataset
    x, y = case_data.get()
    return x, y


# ------------- To collect benchmark results ------------
@pytest.fixture(autouse=True, scope='session')
def store():
    """The store where we will put our results_bag fixture"""
    return OrderedDict()


results_bag = create_results_bag_fixture('store', name='results_bag')
"""The fixture where we will put all our benchmark results"""


# ------------- To evaluate the algorithms ------------
def test_poly_fit(challenger, dataset, results_bag):
    """
    Tests the polyfit function with `degree` on the provided `dataset`,
    and stores the model accuracy (cv-rmse) in the results_bag
    """

    # Get the test case at hand
    x, y = dataset

    # Fit the model
    challenger.fit(x, y)
    results_bag.model = challenger

    # Use the model to perform predictions
    predictions = challenger.predict(x)

    # Evaluate the prediction error
    cvrmse = np.sqrt(np.mean((predictions-y)**2)) / np.mean(y)
    print("Relative error (cv-rmse) is: %.2f%%" % (cvrmse * 100))
    results_bag.cvrmse = cvrmse


# To make sure that the benchmark is not biased by import times on the first run, we perform a first run here
test_poly_fit(PolyFitChallenger(degree=1), (np.arange(10), np.arange(10)), ResultsBag())


# ------------- To create the final benchmark table ------------
def test_synthesis(request, store):
    """
    Creates the benchmark synthesis table
    Note: we could do this at many other places (hook, teardown of a session-scope fixture...)
    as explained in `pytest-harvest` plugin
    """

    # Get session synthesis filtered on the test function of interest, combined with our store
    results_dct = get_session_synthesis_dct(request.session, filter=test_poly_fit,
                                            durations_in_ms=True, test_id_format='function', status_details=False,
                                            fixture_store=store, flatten=True, flatten_more='results_bag')

    # convert to a pandas dataframe
    results_df = pd.DataFrame.from_dict(results_dct, orient='index')
    results_df = results_df.loc[list(results_dct.keys()), :]          # fix rows order
    results_df.index.name = 'test_id'                                 # set index name
    results_df.drop(['pytest_obj'], axis=1, inplace=True)             # drop pytest object column
    results_df = results_df.apply(lambda s: s.astype("category") if s.dtype == 'object' else s)  # convert all to categorical

    # print to csv
    results_df = results_df.rename(columns={'challenger': 'degree'})
    results_df['challenger'] = results_df['model'].astype("object").map(str)
    results_df = results_df[['dataset', 'challenger', 'degree', 'status', 'duration_ms', 'cvrmse']]
    # print("\n" + results_df.to_csv(sep=';', decimal=','))
    results_df.to_csv("polyfit_bench_results.csv", sep=';', decimal=',')

    # print to markdown-like (requires tabulate)
    try:
        from tabulate import tabulate
        print("\n" + tabulate(results_df, headers='keys', tablefmt='pipe'))
        tabulate_is_available = True
    except ImportError as e:
        tabulate_is_available = False

    # plot (requires matplotlib)
    try:
        import matplotlib.pyplot as plt
        cvrmse_df = results_df.pivot(index='dataset', columns='challenger', values='cvrmse')
        ax = cvrmse_df.plot.bar()
        ax.set_ylabel("cvrmse")
        plt.xticks(plt.xticks()[0], plt.xticks()[1], rotation=30, ha='right')
        plt.subplots_adjust(left=0.20, bottom=0.25)
        plt.show()
    except ImportError as e:
        pass

    # summarize results by challenger
    summary_df = results_df.groupby('degree', axis=0).agg({'duration_ms': ['mean', 'std'], 'cvrmse': ['mean', 'std']})
    # print("\n" + summary_df.to_csv(sep=';', decimal=','))
    if tabulate_is_available:
        print("\n" + tabulate(summary_df, headers='keys'))
