import forecastio
import datetime

api_key = "6b85de19d66775418502c7eb8482e44d"
# colombo
lat = 6.9271
lng = 79.8612
# barbados
# lat = 13.1132
# lng = -59.5988

current_time = datetime.date(2016, 6, 19)
# forecast = forecastio.load_forecast(api_key, lat, lng, time=current_time)
forecast = forecastio.load_forecast(api_key, lat, lng)
byHour = forecast.daily()

for hourlyData in byHour.data:
        print hourlyData.time
        print hourlyData.precipProbability
