# Data science benchmark example

A frequent need for teams developing data science algorithms and wishing to industrialize them, is to be able to **test algorithms against a quantity of datasets**, in other words to create a *reference benchmark*.

Teams might have two objectives in mind:

 - getting an overview of the **performance of a single algorithm** on a large quantity of cases, so as to be sure of its genericity
 - **comparing several algorithms or several configurations**, to see which one is the best overall and on specific cases.


It is obviously quite trivial to start developing a benchmark engine: a couple `for` loops can do the trick. However as soon as one wishes to

 * run each evaluation in an independent context (possibly distributed on several processors/platforms)
 * and for each evaluation, get an independent capability to:
 
     * Log (see what has been done)
     * Debug (understand why it does not work as expected)
     * Profile (understand what takes time to potentially improve speed)

Then one finds out that it is a bit more complex to develop. And by taking a step back we find that `pytest` and its ecosystem (`pytest-profile`, `pytest-logging`, `pytest-xdist`...) **already provide all of this** (plus a nice integration in your IDE) !

## Example description

In this simple example we want to benchmark the `np.polyfit` function, that fits polynomial functions to data, against a database made of code-generated data and csv files. This function has a `degree` parameter allowing to restrict the polynomial order of the function. We will compare two configurations: degree = 1 (linear regression) and degree = 2 (quadratic).

Here are the results illustrated with plots:

![Results_plots](benchmark_plots.png)

In each subplot you see a dataset (in gray), and the various challengers that are run against it: in yellow the linear regression and in red the quadratic function.

The code also produces a results table:

| dataset                   |   degree | fit/status   |   fit/duration_ms |   fit/cvrmse | predict/status   |   predict/duration_ms | eval/status   |   eval/duration_ms | plot/status   |   plot/duration_ms |
|---------------------------|----------|--------------|-------------------|--------------|------------------|-----------------------|---------------|--------------------|---------------|--------------------|
| Anscombe's quartet 1      |        1 | passed       |          2.00009  |  0.149122    | passed           |              0.999928 | passed        |           1.00017  | passed        |           10.9999  |
| Anscombe's quartet 1      |        2 | passed       |          1.00017  |  0.1444      | passed           |              0.999928 | passed        |           1.00017  | passed        |            9.00006 |
| Anscombe's quartet 2      |        1 | passed       |          0.999928 |  0.149196    | passed           |              0.999928 | passed        |           0.999928 | passed        |            6.99997 |
| Anscombe's quartet 2      |        2 | passed       |          0.999928 |  0.00019015  | passed           |              0.999928 | passed        |           0        | passed        |            9.00006 |
| ...      |        ... | ...       |          ... |  ...  | ...           |              ... | ...        |           ...        | ...        |            ... |
| Data file 'v-shape.csv'   |        2 | passed       |          1.00017  |  0.212283    | passed           |              0.999928 | passed        |           1.00017  | passed        |            7.9999  | 

## Solution description

The solution is made of two files located [here](https://github.com/smarie/pytest-patterns/blob/master/reference_examples/data_science_benchmark):

 - `test_polyfit.py` contains the benchmark logic including plots
 - `test_polyfit_cases.py` contains the code to generate or retrieve (from csv files) the benchmark datasets

In this solution we make use of several pytest features and plugins:

 - [pytest-cases](https://smarie.github.io/python-pytest-cases/) to **separate test code (the evaluation protocol) from test data (the datasets)**
 - [pytest parametrize](https://docs.pytest.org/en/latest/parametrize.html) to create two variants: degreee=1 and degree=2
 - [pytest-steps](https://smarie.github.io/python-pytest-steps/) to **decompose a test into incremental steps** while sharing the test context across the steps
 - [pytest fixture](https://docs.pytest.org/en/latest/reference.html#pytest.fixture) to create a results store and a plots manager 
 - [pytest-harvest](https://smarie.github.io/python-pytest-harvest/) to **collect applicative results from all runs**, put them in the store and create the synthesis table in the end

![Overview](./Overview_fig.png)