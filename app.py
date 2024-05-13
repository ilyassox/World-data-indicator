'''from flask import Flask, render_template, request
from meteostat import Stations, Daily , Monthly
from datetime import datetime, timedelta

import pandas as pd

app = Flask(__name__)

start = datetime(2017, 1, 1)

# Set end date to yesterday's date
end = datetime.now() - timedelta(days=1)


def get_data(station, country, city, wmo_code):
    data = Daily(station, start, end).fetch()
    data.insert(0, 'station', f'{country}-{city}-{wmo_code}')
    data['sun_hours'] = round(data['tsun'] / 60, 2)
    data['country'] = country
    data['city'] = city
    data['wmo_station_code'] = wmo_code
    return data[['country', 'city', 'wmo_station_code', 'station',
                 'date', 'tavg', 'tmin', 'tmax', 'prcp', 'wspd',
                 'pres', 'tsun', 'sun_hours']]

stations = [
    ('FR', 'Paris', '07156'),
    ('FR', 'Marseille', '07610'),
    ('FR', 'Lyon', '07481'),
    ('FR', 'Toulouse', '07630'),
    ('FR', 'Nice', '07510'),
    ('FR', 'Nantes', '07434'),
    ('FR', 'Strasbourg', '07207'),
    ('FR', 'Montpellier', '07650'),
    ('FR', 'Bordeaux', '07510'),
    ('FR', 'Lille', '07110'),
    ('FR', 'Rennes', '07240'),
    ('FR', 'Reims', '07168'),
    ('FR', 'Le Havre', '07207'),
    ('FR', 'Saint-Étienne', '07497'),
    ('FR', 'Toulon', '07610'),
    ('FR', 'Grenoble', '07434'),
    ('FR', 'Dijon', '07299'),
    ('FR', 'Angers', '07434'),
    ('FR', 'Nîmes', '07650'),
    ('FR', 'Villeurbanne', '07481'),
    ('FR', 'Saint-Denis', '07110'),
    ('FR', 'Le Mans', '07434'),
    ('FR', 'Aix-en-Provence', '07610'),
    ('FR', 'Clermont-Ferrand', '07434'),
    ('FR', 'Brest', '07460'),
    ('FR', 'Limoges', '07460'),
    ('FR', 'Tours', '07240'),
    ('FR', 'Amiens', '07168'),
    ('FR', 'Perpignan', '07680'),
    ('FR', 'Metz', '07168'),
    ('FR', 'Besançon', '07299'),
    ('FR', 'Orléans', '07240'),
    ('FR', 'Mulhouse', '07207'),
    ('FR', 'Rouen', '07207'),
    ('FR', 'Caen', '07207'),
    ('FR', 'Saint-Denis', '07110'),
    ('FR', 'Nancy', '07168'),
    ('FR', 'Saint-Paul', '07610'),
    ('FR', 'Montreuil', '07110'),
    ('FR', 'Argenteuil', '07156'),
    ('FR', 'Roubaix', '07110'),
    ('FR', 'Tourcoing', '07110'),
    ('FR', 'Avignon', '07650'),
    ('FR', 'Poitiers', '07434'),
    ('FR', 'Fort-de-France', '97200'),
    ('FR', 'Courbevoie', '07156'),
    ('FR', 'Vitry-sur-Seine', '07156'),
    ('FR', 'Versailles', '07156'),
    ('FR', 'Colombes', '07156'),
    ('FR', 'Asnières-sur-Seine', '07156'),
    ('FR', 'Saint-Pierre', '07110'),
    ('FR', 'Aulnay-sous-Bois', '07156'),
    ('FR', 'Rueil-Malmaison', '07156'),
    ('FR', 'Pau', '07510'),
    ('FR', 'La Rochelle', '07434'),
    ('FR', 'Champigny-sur-Marne', '07156'),
    ('FR', 'Nanterre', '07156'),
    ('FR', 'Courcouronnes', '07156'),
    ('FR', 'Calais', '07110'),
    ('FR', 'Vénissieux', '07481'),
    ('FR', 'Antibes', '07510'),
    ('FR', 'Troyes', '07168'),
    ('FR', 'Niort', '07434'),
    ('FR', 'Sarcelles', '07156'),
    ('FR', 'Villejuif', '07156'),
    ('FR', 'Cholet', '07434'),
    ('FR', 'Hyères', '07610'),
    ('FR', 'Meaux', '07156'),
    ('FR', 'Chambéry', '07434'),
    ('FR', 'Saint-Quentin', '07168'),
    ('FR', 'Beziers', '07650'),
    ('FR', 'Épinay-sur-Seine', '07156'),
    ('FR', 'Évry', '07156'),
    ('FR', 'Cergy', '07156'),
    ('FR', 'Villepinte', '07156'),
    ('FR', 'Noisy-le-Grand', '07156'),
    ('FR', 'La Seyne-sur-Mer', '07610'),
    ('FR', 'Le Tampon', '07601'),
    ('FR', 'Le Blanc-Mesnil', '07156'),
    ('FR', 'Arles', '07650'),
    ('FR', 'Clamart', '07156'),
    ('FR', 'Saint-Maur-des-Fossés', '07156'),
    ('FR', 'Fontenay-sous-Bois', '07156'),
    ('FR', 'Sartrouville', '07156'),
    ('FR', 'Bastia', '07610'),
    ('FR', 'Bobigny', '07156'),
    ('FR', 'Saint-Nazaire', '07434'),
    ('FR', 'Vannes', '07434'),
    ('FR', 'Sevran', '07156'),
    ('FR', 'Corbeil-Essonnes', '07156'),
    ('FR', 'Saint-Laurent-du-Maroni', '07610'),
    ('FR', 'Franconville', '07156'),
    ('FR', 'Pessac', '07510'),
    ('FR', 'Vaulx-en-Velin', '07481'),
    ('FR', 'Martigues', '07610'),
    ('FR', 'Clichy', '07156'),
    ('FR', 'Vitrolles', '07610'),
    ('FR', 'Massy', '07156'),
    ('FR', 'Vincennes', '07156'),
    ('FR', 'Échirolles', '07434'),
    ('FR', 'Évry-Courcouronnes', '07156'),
    ('FR', 'Drancy', '07156'),
    ('FR', 'Albi', '07434'),
    ('FR', 'Bourg-en-Bresse', '07481'),
    ('FR', 'Niort', '07434'),
    ('FR', 'Gap', '07434'),
    ('FR', 'Angoulême', '07434'),
    ('FR', 'Béziers', '07650'),
    ('FR', 'Alfortville', '07156'),
    ('FR', 'Chartres', '07240'),
    ('FR', 'Talence', '07510'),
    ('FR', 'Bagneux', '07156'),
    ('FR', 'Villeurbanne', '07481'),
    ('FR', 'Maisons-Alfort', '07156'),
    ('FR', 'Chelles', '07156'),
    ('FR', 'Aubagne', '07610'),
    ('FR', 'Chalon-sur-Saône', '07299'),
    ('FR', 'Montluçon', '07434'),
    ('FR', 'Villefranche-sur-Saône', '07481'),
    ('FR', 'Conflans-Sainte-Honorine', '07156'),
    ('FR', 'Montigny-le-Bretonneux', '07156'),
    ('FR', 'Sainte-Geneviève-des-Bois', '07156'),
    ('FR', 'Saint-Chamond', '07497'),
    ('FR', 'La Courneuve', '07156'),
    ('FR', 'Saint-Brieuc', '07434'),
    ('FR', 'Sète', '07650'),
    ('FR', 'Suresnes', '07156'),
    ('FR', 'Cagnes-sur-Mer', '07510'),
    ('FR', 'Choisy-le-Roi', '07156'),
    ('FR', 'Garges-lès-Gonesse', '07156'),
    ('FR', 'Châtillon', '07156'),
    ('FR', 'Villepinte', '07156'),
    ('FR', 'Le Perreux-sur-Marne', '07156'),
    ('FR', 'Cachan', '07156'),
    ('FR', 'Saint-Ouen', '07156'),
    ('FR', 'Gennevilliers', '07156'),
    ('FR', 'Savigny-sur-Orge', '07156'),
    ('FR', 'Saint-Martin-d’Hères', '07434'),
    ('FR', 'Saint-Leu', '07110'),
    ('FR', 'Bagnolet', '07156'),
    ('FR', 'Beauvais', '07168'),
    ('FR', 'Châlons-en-Champagne', '07168'),
    ('FR', 'Villeneuve-Saint-Georges', '07156'),
    ('FR', 'Tremblay-en-France', '07156'),
    ('FR', 'Saint-Cloud', '07156'),
    ('FR', 'Gagny', '07156'),
    ('FR', 'Villeneuve-d’Ascq', '07110'),
    ('FR', 'Puteaux', '07156'),
    ('FR', 'Béziers', '07650'),
    ('FR', 'Livry-Gargan', '07156'),
    ('FR', 'Saint-Joseph', '07601'),
    ('FR', 'Nogent-sur-Marne', '07156'),
    ('FR', 'Concarneau', '07434'),
    ('FR', 'Trappes', '07156'),
    ('FR', 'La Ciotat', '07610'),
    ('FR', 'Montélimar', '07650'),
    ('FR', 'Villefranche-sur-Mer', '07510'),
    ('FR', 'Aubagne', '07610'),
    ('FR', 'Annemasse', '07434'),
    ('FR', 'Les Mureaux', '07156'),
    ('FR', 'Saint-Dié-des-Vosges', '07168'),
    ('FR', 'Nanterre', '07156'),
    ('FR', 'Schiltigheim', '07207'),
    ('FR', 'Montrouge', '07156'),
    ('FR', 'Plaisir', '07156'),
    ('FR', 'Neuilly-sur-Marne', '07156'),
    ('FR', 'Villenave-d’Ornon', '07510'),
    ('FR', 'Thionville', '07168'),
    ('FR', 'Lens', '07168'),
    ('FR', 'Athis-Mons', '07156'),
    ('FR', 'Poissy', '07156'),
    ('FR', 'Agen', '07510'),
    ('FR', 'Haguenau', '07207'),
    ('FR', 'Roanne', '07497'),
    ('FR', 'Aubervilliers', '07156'),
    ('FR', 'Creil', '07156'),
    ('FR', 'Montmorency', '07156'),
    ('FR', 'Viry-Châtillon', '07156'),
    ('FR', 'Villeneuve-la-Garenne', '07156'),
    ('FR', 'Les Lilas', '07156'),
    ('FR', 'Sotteville-lès-Rouen', '07207'),
    ('FR', 'Lamentin', '97200'),
    ('FR', 'Vandœuvre-lès-Nancy', '07168'),
    ('FR', 'Sainte-Marie', '97105'),
    ('FR', 'Vitry-sur-Orne', '07168'),
    ('FR', 'Goussainville', '07156'),
    ('FR', 'Alès', '07650'),
    ('FR', 'Martigues', '07610'),
    ('FR', 'Baie-Mahault', '97105'),
    ('FR', 'Chatou', '07156'),
    ('FR', 'Viry-Châtillon', '07156'),
    ('FR', 'Élancourt', '07156'),
    ('FR', 'Beaune', '07299'),
    ('FR', 'Montfermeil', '07156'),
    ('FR', 'Vigneux-sur-Seine', '07156'),
    ('FR', 'Équeurdreville-Hainneville', '07168'),
    ('FR', 'Vanves', '07156'),
    ('FR', 'Clichy-sous-Bois', '07156'),
    ('FR', 'Saint-Martin', '07601'),
    ('FR', 'Le Creusot', '07299'),
    ('FR', 'Gonesse', '07156'),
    ('FR', 'Limeil-Brévannes', '07156'),
    ('FR', 'Malakoff', '07156'),
    ('FR', 'Lunel', '07650'),
    ('FR', 'Les Abymes', '97105'),
    ('FR', 'Brive-la-Gaillarde', '07460'),
    ('FR', 'Sainte-Suzanne', '07156'),
    ('FR', 'Vernon', '07156'),
    ('FR', 'Villiers-le-Bel', '07156'),
    ('FR', 'Savigny-le-Temple', '07156'),
    ('FR', 'Champigny-sur-Marne', '07156'),
    ('FR', 'Yerres', '07156'),
    ('FR', 'Saint-Ouen-l’Aumône', '07156'),
    ('FR', 'Saint-Martin-dHères', '07434'),
    ('FR', 'Épinal', '07168'),
]

# Initialize an empty list to store data for French cities
dfs = []

# Loop through each station and fetch data for French cities only
for country, city, wmo_code in stations:
    if country == 'FR':
        # Fetch data for the current French city
        station_data = get_data(wmo_code, country, city, wmo_code)
        # Append the data to the list
        dfs.append(station_data)

# Concatenate data for all French cities into a single DataFrame
weather_data = pd.concat(dfs)
#weather_data = weather_data.reset_index().rename(columns={'index': 'date'})

# Set the index of the DataFrame to the 'city' column

# Set the index of the DataFrame to the 'city' column
weather_data.set_index('city', inplace=True)
print(weather_data)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    city_name = request.form['city']
    if city_name in weather_data.index:
        city_weather = weather_data.loc[city_name].to_dict(orient='records')
        return render_template('base.html', city=city_name, weather=city_weather)
    else:
        return render_template('base.html', city=city_name, weather="City not found")

if __name__ == '__main__':
    app.run(debug=True)






################################################""


from flask import Flask, render_template, request
from meteostat import Stations, Daily
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)

class WeatherData:
    def __init__(self):
        self.start_date = datetime(2017, 1, 1)
        self.end_date = datetime.now() - timedelta(days=1)
        self.weather_data = self.fetch_weather_data()

    def fetch_weather_data(self):
        stations = [
            ('FR', 'Paris', '07156'),
            ('FR', 'Marseille', '07610'),
            # Add more stations here
        ]

        dfs = []
        for country, city, wmo_code in stations:
            if country == 'FR':
                data = self.get_data(wmo_code, country, city, wmo_code)
                dfs.append(data)

        weather_data = pd.concat(dfs)
        weather_data = weather_data.reset_index().rename(columns={'index': 'date'})
        weather_data.set_index('city', inplace=True)
        return weather_data

    def get_data(self, station, country, city, wmo_code):
        data = Daily(station, self.start_date, self.end_date).fetch()
        data.insert(0, 'station', f'{country}-{city}-{wmo_code}')
        data['sun_hours'] = round(data['tsun'] / 60, 2)
        data['country'] = country
        data['city'] = city
        data['wmo_station_code'] = wmo_code
        return data

weather_data_handler = WeatherData()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    city_name = request.form['city']
    if city_name in weather_data_handler.weather_data.index:
        city_weather = weather_data_handler.weather_data.loc[city_name].to_dict(orient='records')
        return render_template('base.html', city=city_name, weather=city_weather)
    else:
        return render_template('base.html', city=city_name, weather="City not found")

if __name__ == '__main__':
    app.run(debug=True)
'''

from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import plotly.graph_objs as go

import json
import wbpy

app = Flask(__name__)

# Initialize the API
api = wbpy.IndicatorAPI()

iso_country_codes = {"Morocco": "MA", "France": "FR", "Japan": "JP" , "Algeria" : "DZ" , "Afghanistan": "AF",
    "Albania": "AL", "Andorra": "AD",
    "Angola": "AO",
    "Antigua and Barbuda": "AG",
    "Argentina": "AR",
    "Armenia": "AM",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Bahamas": "BS",
    "Bahrain": "BH",
    "Bangladesh": "BD",
    "Barbados": "BB",
    "Belarus": "BY",
    "Belgium": "BE",
    "Belize": "BZ",
    "Benin": "BJ",
    "Bhutan": "BT",
    "Bolivia": "BO",
    "Bosnia and Herzegovina": "BA",
    "Botswana": "BW",
    "Brazil": "BR",
    "Brunei": "BN",
    "Bulgaria": "BG",
    "Burkina Faso": "BF",
    "Burundi": "BI",
    "Cabo Verde": "CV",
    "Cambodia": "KH",
    "Cameroon": "CM",
    "Canada": "CA",
    "Central African Republic": "CF",
    "Chad": "TD",
    "Chile": "CL",
    "China": "CN",
    "Colombia": "CO","Comoros": "KM",
    "Congo": "CG",
    "Costa Rica": "CR",
    "Croatia": "HR",
    "Cuba": "CU",
    "Cyprus": "CY",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Djibouti": "DJ",
    "Dominica": "DM",
    "Dominican Republic": "DO",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "Equatorial Guinea": "GQ",
    "Eritrea": "ER",
    "Estonia": "EE",
    "Eswatini": "SZ",
    "Ethiopia": "ET",
    "Fiji": "FJ",
    "Finland": "FI",
    "Gabon": "GA",
    "Gambia": "GM",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Greece": "GR",
    "Grenada": "GD",
    "Guatemala": "GT",
    "Guinea": "GN",
    "Guinea-Bissau": "GW",
    "Guyana": "GY",
    "Haiti": "HT",
    "Honduras": "HN",
    "Hungary": "HU",
    "Iceland": "IS",
    "India": "IN",
    "Indonesia": "ID",
    "Iran": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Japan": "JP",
    "Jordan": "JO",
    "Kazakhstan": "KZ",
    "Kenya": "KE",
    "Kiribati": "KI",
    "Kuwait": "KW",
    "Kyrgyzstan": "KG",
    "Laos": "LA",
    "Latvia": "LV",
    "Lebanon": "LB",
    "Lesotho": "LS",
    "Liberia": "LR",
    "Libya": "LY",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Madagascar": "MG",
    "Malawi": "MW",
    "Malaysia": "MY",
    "Maldives": "MV",
    "Mali": "ML",
    "Malta": "MT",
    "Marshall Islands": "MH",
    "Mauritania": "MR",
    "Mauritius": "MU",
    "Mexico": "MX",
    "Micronesia": "FM",
    "Moldova": "MD",
    "Monaco": "MC",
    "Mongolia": "MN",
    "Montenegro": "ME",
    "Mozambique": "MZ",
    "Myanmar": "MM",
    "Namibia": "NA",
    "Nauru": "NR",
    "Nepal": "NP",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Nicaragua": "NI",
    "Niger": "NE",
    "Nigeria": "NG",
    "North Korea": "KP",
    "North Macedonia": "MK",
    "Norway": "NO",
    "Oman": "OM",
    "Pakistan": "PK",
    "Palau": "PW",
    "Panama": "PA",
    "Papua New Guinea": "PG",
    "Paraguay": "PY",
    "Peru": "PE",
    "Philippines": "PH",
    "Poland": "PL",
    "Portugal": "PT",
    "Qatar": "QA",
    "Romania": "RO",
    "Russia": "RU",
    "Rwanda": "RW",
    "Saint Kitts and Nevis": "KN",
    "Saint Lucia": "LC",
    "Saint Vincent and the Grenadines": "VC",
    "Samoa": "WS",
    "San Marino": "SM",
    "Sao Tome and Principe": "ST",
    "Saudi Arabia": "SA",
    "Senegal": "SN",
    "Serbia": "RS",
    "Seychelles": "SC",
    "Sierra Leone": "SL",
    "Singapore": "SG",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Solomon Islands": "SB",
    "Somalia": "SO",
    "South Africa": "ZA",
    "South Korea": "KR",
    "South Sudan": "SS",
    "Spain": "ES",
    "Sri Lanka": "LK",
    "Sudan": "SD",
    "Suriname": "SR",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syria": "SY",
    "Taiwan": "TW",
    "Tajikistan": "TJ",
    "Tanzania": "TZ",
    "Thailand": "TH",
    "Timor-Leste": "TL",
    "Togo": "TG",
    "Tonga": "TO",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Turkey": "TR",
    "Turkmenistan": "TM",
    "Tuvalu": "TV",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "United Kingdom": "GB",
    "United States": "US",
    "Uruguay": "UY",
 
    }
total_population = "SP.POP.TOTL"
total_CO2 = "EN.ATM.CO2E.KT"

'''def country_infos(country_name):
    api_url = f'https://api.api-ninjas.com/v1/country?name={country_name}'
    response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
'''
def get_country_populations(country_codes):
    dataset = api.get_dataset(total_population, iso_country_codes.values(), date="2010:2020")
    country_pop = dataset.as_dict()
    for country in country_pop.keys():
        if country == country_codes:
            return country_pop[country]

def get_predicted_populations():
    dataset = api.get_dataset(total_population, iso_country_codes.values(), date="2010:2020")
    country_pop = dataset.as_dict()

        
def get_country_co2(country_codes):
    dataset = api.get_dataset(total_CO2, iso_country_codes.values(), date="2010:2020")
    country_emission = dataset.as_dict()
    for country in country_emission.keys():
        if country == country_codes:
            return country_emission[country]

from sklearn.linear_model import LinearRegression
import numpy as np

def prepare_data(population_data):
    years = []
    populations = []
    for year, population in population_data.items():
        if population is not None:
            years.append(int(year))
            populations.append(population)
    X = np.array(years).reshape(-1, 1)
    y = np.array(populations)
    return X, y

def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict_populations(model, years):
    X_pred = np.array(years).reshape(-1, 1)
    population_pred = model.predict(X_pred)
    return population_pred

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country_name = request.form['country_name']
        country_code = iso_country_codes.get(country_name)
        if country_code:
    # Get country data
            country_data = get_country_populations(country_code)
            country_data = dict(reversed(country_data.items()))
            country_emission = get_country_co2(country_code)
    
    # Prepare data for modeling
            X, y = prepare_data(country_data)
            X_train, y_train = X, y  # Assuming we're using all data for training
    
    # Train model
            models = train_model(X_train, y_train)
    
    # Define years for prediction
            years_to_predict = [2021, 2022, 2023, 2024, 2025]
    
    # Make predictions
            predictions = predict_populations(models, years_to_predict)

    # Prepare figures
            population_fig = go.Bar(x=list(country_data.keys()), y=list(country_data.values()), name='Population Data', marker=dict(color='rgba(55, 128, 191, 0.7)'))
            emission_fig = go.Bar(x=list(country_emission.keys()), y=list(country_emission.values()), name='CO2 Emission Data', marker=dict(color='rgba(255, 153, 51, 0.7)'))
            predictions_fig = go.Bar(x=years_to_predict, y=predictions, name='Predictions', marker=dict(color='red'))

    # Define layout for population figure
            layout_pop = go.Layout(title='Population Data', barmode='group', xaxis=dict(title='Year'), yaxis=dict(title='Population'))
    
    # Create population figure
            pop_fig = go.Figure(data=[population_fig, predictions_fig], layout=layout_pop)
        

    # Define layout for emission figure
            layout_emi = go.Layout(title='Emission Data', barmode='group', xaxis=dict(title='Year'), yaxis=dict(title='Emission'))
    
    # Create emission figure
            emi_fig = go.Figure(data=[emission_fig], layout=layout_emi)

    # Convert figures to JSON
            graph_pop = pop_fig.to_json()
            graph_emi = emi_fig.to_json()
            #graph_json_str = json.dumps(graph_json)


            return render_template('base.html', country_name=country_name, country_data=country_data, country_emission=country_emission , graph_json_pop=graph_pop , graph_json_emi=graph_emi,predictions=predictions  )
        else:
            return "Country not found!"
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)





