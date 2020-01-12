from flask import Flask
import pandas as pd
import folium
from folium.plugins import HeatMap

app = Flask(__name__)


@app.route('/')
def index():
    pollution_data = pd.read_csv('input/' + 'air-pollution-england-wales.csv')
    station_data = pd.read_csv('input/' + 'monitoring-station-locations.csv')[['Site Name', 'Latitude', 'Longitude']]

    # Rearrange columns, un-pivot, clean and join together
    pollution_data['Date Time'] = pollution_data['Date'].astype(str) + ' ' + pollution_data['Time']
    cols = list(pollution_data.columns.values)
    cols.pop(cols.index('Date'))
    cols.pop(cols.index('Time'))
    cols.pop(cols.index('Date Time'))
    pollution_data = pollution_data[['Date Time'] + cols]

    pollution_data = pollution_data.melt(id_vars=["Date Time"],
                                         var_name="Site Name",
                                         value_name="Reading")

    geolocated_pollution_data = pollution_data.merge(station_data)

    geolocated_pollution_data['Reading'] = pd.to_numeric(geolocated_pollution_data['Reading'], errors='coerce')
    geolocated_pollution_data.replace('NaN', 0)

    # print(pollution_data.head())
    # print(station_data.head())
    print(geolocated_pollution_data.head())

    print(geolocated_pollution_data[['Latitude', 'Longitude', 'Reading']].groupby(
        ['Latitude', 'Longitude']).max().reset_index().values.tolist())
    # print(geolocated_pollution_data[['Latitude', 'Longitude', 'Reading']].groupby(['Latitude', 'Longitude']).max(
    # ).reset_index().values.tolist())

    base_map = folium.Map(location=[54.57206, -5.80078], control_scale=True, zoom_start=6)

    HeatMap(data=geolocated_pollution_data[['Latitude', 'Longitude', 'Reading']].groupby(['Latitude', 'Longitude']).max().reset_index().values.tolist(), radius=12, max_zoom=2, max_val=200).add_to(base_map)

    return base_map._repr_html_()


if __name__ == '__main__':
    app.run()
