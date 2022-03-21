import logging
from pathlib import Path
from warnings import warn

import numpy as np

from pytest_cases import fixture, parametrize_with_cases


# logging configuration
exec_log = logging.getLogger('algo')
logs_dir = Path(__file__).parent / "logs"


@fixture(autouse=True)
def configure_logging(request, caplog):
    """ Set log file name same as test name, and set log level. You could change the format here too """
    log_file = logs_dir / ("%s.log" % request.node.name)
    request.config.pluginmanager.get_plugin("logging-plugin").set_log_path(log_file)
    caplog.set_level(logging.INFO)


@fixture
@parametrize_with_cases("algo", cases='.challengers_polyfit', prefix='algo_')
def challenger(algo):
    """ A fixture collecting all challengers from `challengers_polyfit.py` """
    # (optional setup code here)
    yield algo
    # (optional teardown code here)


@fixture
@parametrize_with_cases("data", cases='.datasets_polyfit', prefix='data_', scope="session")
def dataset(data):
    """ A fixture collecting all datasets from `datasets_polyfit.py`.
    Note: we use "scope=session" so that this method is called only once per case.
    This ensures that each file is read once.
    """
    # (optional setup code here)
    yield data
    # (optional teardown code here)


def test_poly_fit(challenger, dataset, results_bag):
    """ Evaluation protocol.
    Applies the `challenger` on the provided `dataset`, and stores the model accuracy (cv-rmse) in the results_bag
    """
    # log the dataset name
    results_bag.dataset_id = dataset.name

    # Fit the model
    exec_log.info("fitting model")
    challenger.fit(dataset.x, dataset.y)
    results_bag.model = challenger

    # Use the model to perform predictions
    exec_log.info("predicting")
    predictions = challenger.predict(dataset.x)

    # Evaluate the prediction error
    exec_log.info("evaluating error")
    cvrmse = np.sqrt(np.mean((predictions-dataset.y)**2)) / np.mean(dataset.y)
    print("Relative error (cv-rmse) is: %.2f%%" % (cvrmse * 100))
    results_bag.cvrmse = cvrmse


# ------------- To create the final benchmark table ------------
def test_synthesis(module_results_df):
    """
    Creates the benchmark synthesis table
    Note: we could do this at many other places (hook, teardown of a session-scope fixture...)
    as explained in `pytest-harvest` plugin
    """
    # ----------- (1) `module_results_df` contains the raw (12 rows) table -----------
    # rename columns and only keep useful information
    module_results_df = rename_with_checks(module_results_df, columns={'challenger_algo_param': 'degree',
                                                                       'dataset_id': 'dataset'})
    module_results_df['challenger'] = module_results_df['model'].map(str)  # only keep the string representation
    module_results_df = module_results_df[['dataset', 'challenger', 'degree', 'status', 'duration_ms', 'cvrmse']]

    # write to csv
    module_results_df.to_csv("polyfit_bench_results.csv", sep=';', decimal=',')

    # pretty-print (requires tabulate)
    try:
        from tabulate import tabulate
        print("\n" + tabulate(module_results_df, headers='keys', tablefmt='pipe'))
    except ImportError:
        warn("Please install tabulate to see the tables more nicely")

    # ----------- (2) graphical synthesis: bar chart (requires matplotlib)------------
    try:
        import matplotlib.pyplot as plt

        # convert all to categorical so that we can pivot
        module_results_df = module_results_df.apply(lambda s: s.astype("category") if s.dtype == 'object' else s)

        cvrmse_df = module_results_df[['dataset', 'challenger', 'cvrmse']].pivot(index='dataset',
                                                                                 columns='challenger',
                                                                                 values='cvrmse')

        ax = cvrmse_df.plot.bar()
        ax.set_ylabel("cvrmse")
        plt.xticks(plt.xticks()[0], plt.xticks()[1], rotation=30, ha='right')
        plt.subplots_adjust(left=0.20, bottom=0.25)
        print("Close the plots to continue...")
        plt.show()
    except ImportError:
        pass

    # ----------- (3) summarizing the results further - by challenger --------------
    summary_df = module_results_df[['degree', 'duration_ms', 'cvrmse']].groupby('degree', axis=0).agg({
        'duration_ms': ['mean', 'std'],
        'cvrmse': ['mean', 'std']
    })
    # pretty-print (requires tabulate)
    try:
        print("\n" + tabulate(summary_df, headers='keys'))
    except NameError:
        pass


def rename_with_checks(df, columns, **kwargs):
    """
    Same than df.rename(columns=<columns>, **kwargs) but checks that columns exist before executing.
    """
    missing = set(columns.keys()).difference(set(df.columns))
    if len(missing) > 0:
        raise ValueError("Missing columns: %s" % missing)

    return df.rename(columns=columns, **kwargs)
