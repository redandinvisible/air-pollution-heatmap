from flask import Flask, render_template
import pandas as pd
import datetime as dt
import folium
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime

app = Flask(__name__)


@app.route('/')
def index():
    pollution_data = pd.read_csv('input/' + 'air-pollution-england-wales.csv')
    station_data = pd.read_csv('input/' + 'monitoring-station-locations.csv')[['Site Name', 'Latitude', 'Longitude']]

    # Rearrange columns, un-pivot, clean and join together, and give json-friendly names
    pollution_data['datetime'] = pollution_data['Date'].astype(str) + ' ' + pollution_data['Time']
    cols = list(pollution_data.columns.values)
    cols.pop(cols.index('Date'))
    cols.pop(cols.index('Time'))
    cols.pop(cols.index('datetime'))
    pollution_data = pollution_data[['datetime'] + cols]

    pollution_data = pollution_data.melt(id_vars=["datetime"],
                                         var_name="Site Name",
                                         value_name="Reading")

    geolocated_pollution_data = pollution_data.merge(station_data)

    geolocated_pollution_data = geolocated_pollution_data.rename(columns={"Site Name": "sitename", "Reading": "reading", "Latitude": "latitude", "Longitude": "longitude"}, errors="raise")

    geolocated_pollution_data['reading'] = pd.to_numeric(geolocated_pollution_data['reading'], errors='coerce')
    geolocated_pollution_data.replace('NaN', 0)

    # the data file is large, so take a sample
    gl_pln_minus_midnight = geolocated_pollution_data[~geolocated_pollution_data['datetime'].str.contains(" 24:")]
    # gl_pln_spring = gl_pln_minus_midnight[gl_pln_minus_midnight['datetime'].str.contains("-04-")]
    # gl_pln_summer = gl_pln_minus_midnight[gl_pln_minus_midnight['datetime'].str.contains("-07-")]
    # gl_pln_autumn = gl_pln_minus_midnight[gl_pln_minus_midnight['datetime'].str.contains("-10-")]
    # gl_pln_winter = gl_pln_minus_midnight[gl_pln_minus_midnight['datetime'].str.contains("-01-")]
    # sample_pln_data = pd.concat([gl_pln_spring, gl_pln_summer, gl_pln_autumn, gl_pln_winter])
    sample_pln_data = gl_pln_minus_midnight[gl_pln_minus_midnight['datetime'].str.contains("2019-07-29 17:00:00")]

    maxReading = sample_pln_data['reading'].max()

    # build a time-sorted list for use with folium's HeatMapWithTime
    # geolocated_pollution_data.loc[geolocated_pollution_data['Date Time'].str.contains(" 24:"), 'Date Time'] = geolocated_pollution_data.loc[geolocated_pollution_data['Date Time'].str.contains(" 24:"), 'Date Time'].apply(airline_datetime)
    # geolocated_pollution_data['Date Time'] = geolocated_pollution_data['Date Time'].apply(airline_datetime)
    # pat = '(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})(?P<second>\d{2})'
    # pd.to_datetime(gl_pln_minus_midnight['Date Time'])
    timestamp_list = []
    # for t in gl_pln_minus_midnight['Date Time'].sort_values().unique():
    #     timestamp_list.append(gl_pln_minus_midnight.loc[gl_pln_minus_midnight['Date Time'] == t, ['Latitude', 'Longitude', 'Reading']].groupby(['Latitude', 'Longitude']).max().reset_index().values.tolist())

    print(sample_pln_data.head())
    # print(station_data.head())
    # print(geolocated_pollution_data.head())
    # print(geolocated_pollution_data[['Latitude', 'Longitude', 'Reading']].groupby(
    #     ['Latitude', 'Longitude']).max().reset_index().values.tolist())
    print(maxReading)
    # print(geolocated_pollution_data[geolocated_pollution_data['Date Time'].str.contains(" 24:")].head())

    # base_map = folium.Map(location=[54.57206, -5.80078], control_scale=True, zoom_start=6)
    # HeatMap(data=geolocated_pollution_data[['Latitude', 'Longitude', 'Reading']].groupby(['Latitude', 'Longitude']).max().reset_index().values.tolist(), radius=12, max_zoom=2, max_val=maxReading, min_opacity=5).add_to(base_map)
    # HeatMapWithTime(sample_pln_data, radius=12, min_opacity=0.5, max_opacity=0.8, use_local_extrema=True).add_to(base_map)

    return render_template('map.html', data={'max': maxReading, 'data': sample_pln_data.to_dict('records')}, message="groovy")
    # return base_map._repr_html_()

if __name__ == '__main__':
    app.run()
