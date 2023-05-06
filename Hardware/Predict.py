import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import pickle

def forecst(element_name, current_rh, start_date, end_date):

    print("Predicting for {}...".format(element_name))
    with open(str(element_name)+'.pkl', 'rb') as f:
        model_fit = pickle.load(f)

    forecast_rh = model_fit.predict(start=start_date, end=end_date, dynamic=True, exog=current_rh)
    print(f'The 95% confidence interval for the forecasted {element_name} values is:')
    print(forecast_rh)
    
    dff = pd.DataFrame(forecast_rh)
    dff_string = dff.to_string()

    dff_string_list = dff_string.split('\n')
    dff_string_list.pop(0)

    print("Prediction Done...")
    return(dff_string_list)
