from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def show_data(station, date):
    dfn = pd.read_csv("data/stations.txt", skiprows=17)
    station_name = dfn.loc[dfn['STAID'] == int(station)]['STANAME                                 '].item()

    station = str(station).zfill(6)
    filename = "data/TG_STAID"+station+".txt"

    dft = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    temperature = dft.loc[dft['    DATE'] == date]['   TG'].squeeze() / 10

    return {"station": station,
            "station name": station_name,
            "date": date,
            "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True)
