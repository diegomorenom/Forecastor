
---

# Forecastor API

**Accurate daily time series forecasting using advanced machine learning and statistical models.**

## Overview
Forecastor API is designed to provide high-accuracy forecasts for daily time series data. Users can upload a CSV file containing their historical data, specify columns, the number of forecast days, and select models for the predictions. Forecastor offers a robust selection of machine learning and statistical models, including:

- **HoltWinters**
- **MovingAverage**
- **NeuralNetworkFF**
- **RandomForest**
- **NeuralNetworkLSTM**
- **FacebookProphet**
- **NeuralProphet**
- **XGBoost**

This API returns forecasted values in a downloadable CSV format, allowing you to make data-driven decisions efficiently and effectively.

---

## API Documentation

### Base URL
`https://api.rapidapi.com/forecastor`

### Authentication
Each request must include an `api_key` in the headers for authentication.

### Endpoint
`POST /process_forecast`

### Request Headers
- `api_key` (str): Your unique API key for authentication.
- `Content-Type`: `multipart/form-data`

### Form Data Parameters
| Parameter           | Type        | Description                                                                                                      |
|---------------------|-------------|------------------------------------------------------------------------------------------------------------------|
| `prediction_column` | `str`       | Name of the column in the CSV file containing the values you want to predict.                                    |
| `date_column`       | `str`       | Name of the column with daily date values (must be without gaps or missing data).                                |
| `forecast_days`     | `int`       | Number of days to predict into the future.                                                                      |
| `selected_models`   | `str`       | Comma-separated list of models to use for forecasting (e.g., `NeuralNetworkLSTM, FacebookProphet, NeuralProphet`). Available models: **HoltWinters, MovingAverage, NeuralNetworkFF, RandomForest, NeuralNetworkLSTM, FacebookProphet, NeuralProphet, XGBoost**. |
| `csv_file`          | `UploadFile`| The CSV file containing historical data with `date_column` and `prediction_column`.                             |

### Example Request
```python
import requests

url = "https://api.rapidapi.com/forecastor/process_forecast"
headers = {
    "api_key": "YOUR_API_KEY"
}
files = {
    "csv_file": open("historical_data.csv", "rb")
}
data = {
    "prediction_column": "sales",
    "date_column": "date",
    "forecast_days": 30,
    "selected_models": "NeuralNetworkLSTM,FacebookProphet,NeuralProphet"
}

response = requests.post(url, headers=headers, files=files, data=data)
with open("forecasted_output.csv", "wb") as f:
    f.write(response.content)
```

### Response
- **200 OK**: Returns a CSV file with the forecasted values for the specified number of days.
- **403 Forbidden**: If an invalid `api_key` is provided.

---

## Model Information

- **HoltWinters**: A time series forecasting technique based on exponential smoothing for seasonal data.
- **MovingAverage**: A method averaging recent values to predict the next data point.
- **NeuralNetworkFF**: A simple feedforward neural network suited for time series forecasting.
- **RandomForest**: An ensemble of decision trees that enhances forecasting accuracy by reducing variance.
- **NeuralNetworkLSTM**: Long Short-Term Memory networks, ideal for sequence prediction and handling long-term dependencies.
- **FacebookProphet**: A model developed by Facebook, suited for time series data with strong seasonal components.
- **NeuralProphet**: A hybrid model combining neural networks with Facebook Prophet for enhanced accuracy.
- **XGBoost**: An optimized gradient boosting algorithm known for its efficiency and predictive performance.

---

## Terms of Use

1. **Usage Limits**: Each user must comply with API usage limits as per their subscription plan.
2. **Data Privacy**: User data is only processed temporarily and not stored beyond the duration required for each request.
3. **Liability**: Forecastor is provided "as is." We are not liable for any damages resulting from use of the API.
4. **Payments**: Users must adhere to payment terms per their subscription. Non-compliance may result in suspended access.
5. **Termination**: We reserve the right to terminate access for users violating these terms.

---

## Support

For questions, customization requests, or issues, please reach out via diegoem93@gmail.com.

