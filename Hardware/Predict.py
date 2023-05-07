import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import pickle
import numpy as np

def forecst(loc, element_name, current_rh, start_date, end_date, dys):

    print("Predicting {}...".format(element_name))
    with open(loc + str(element_name)+'.pkl', 'rb') as f:
        model_fit = pickle.load(f)
   
    #forecast_rh = model_fit.predict(start=start_date, end=end_date)
    # forecast_rh = model_fit.predict(start=start_date, end=end_date, dynamic=True, exog=current_rh)
    # modified_values = np.where(current_rh > 0.5, forecast_rh*1.2, forecast_rh)
    
    dys += 1 	

    forecast_rh = model_fit.forecast(steps=dys)
    forecast_rh.index = pd.date_range(start=start_date, end=end_date, freq='D')
    forecast_rh = round(forecast_rh, 2)

    print(f'The 95% confidence interval for the forecasted {element_name} values is:')
    print(forecast_rh)
    
    dff = pd.DataFrame(forecast_rh)
    dff_string = dff.to_string()

    dff_string_list = dff_string.split('\n')
    dff_string_list.pop(0)

    print("Prediction Done...")
    return(dff_string_list)
