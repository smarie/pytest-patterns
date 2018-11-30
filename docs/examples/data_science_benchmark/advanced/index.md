## To go further

There are a couple things that we could wish to do in real-world situations. We present below two of them that are included in the `data_science_benchmark_advanced/` example files, also available from [here]().

**TODO continue**


### Steps in the evaluation protocol

You may wish to decompose the evaluation protocol into distinct steps (i.e. distinct pytest nodes), for several reasons:

 - you do not want to get a "fail" outcome when only a very small (maybe even optional) part of the evaluation protocol failed.
 - you want to easily spot where the error happens in case of failure
 - you would like to measure the execution of each step independently, without requiring profiling tools 

It is quite easy to do so thanks to [pytest-steps](https://smarie.github.io/python-pytest-steps/):

```bash
>>> pip install pytest-steps
```

Then a tiny modification in our main test function and *Voilà*:

```python

```




###


 - [pytest-steps](https://smarie.github.io/python-pytest-steps/) to **decompose a test into incremental steps** while sharing the test context across the steps

In this solution we make use of several pytest features and plugins:


 - [pytest parametrize](https://docs.pytest.org/en/latest/parametrize.html) to create two variants: degreee=1 and degree=2

 - [pytest fixture](https://docs.pytest.org/en/latest/reference.html#pytest.fixture) to create a results store and a plots manager 




Here are the results illustrated with plots:

![Results_plots](benchmark_plots2.png)

In each subplot you see a dataset (in gray), and the various challengers that are run against it: in yellow the linear regression and in red the quadratic function.

The code also produces a results table:





## trash
 
In this solution we make use of several pytest features and plugins:

 - [pytest-cases](https://smarie.github.io/python-pytest-cases/) to **separate test code (the evaluation protocol) from test data (the datasets)**
 - [pytest parametrize](https://docs.pytest.org/en/latest/parametrize.html) to create two variants: degreee=1 and degree=2
 - [pytest-steps](https://smarie.github.io/python-pytest-steps/) to **decompose a test into incremental steps** while sharing the test context across the steps
 - [pytest fixture](https://docs.pytest.org/en/latest/reference.html#pytest.fixture) to create a results store and a plots manager 
 - [pytest-harvest](https://smarie.github.io/python-pytest-harvest/) to **collect applicative results from all runs**, put them in the store and create the synthesis table in the end
