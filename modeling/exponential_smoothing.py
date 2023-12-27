from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# single exponential smoothing
def exp_smoothing_forecast(data):
    # create class
    model = SimpleExpSmoothing(data)
    # fit model
    model_fit = model.fit
    # make prediction
    yhat = model_fit.predict()
    return yhat

# prepare data
def exp_smoothing_forecast(data):
    # create class
    model = ExponentialSmoothing(data)
    # fit model
    model_fit = model.fit()
    # make prediction
    yhat = model_fit.predict()
    return yhat