from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)


dfn = pd.read_csv("data/stations.txt", skiprows=17, nrows=92)
stations = dfn[["STAID", "STANAME                                 ", "CN", "HGHT"]].to_html()


@app.route("/")
def home():
    return render_template("home.html", data=stations)


@app.route("/api/v1/s/<station>")
def all_station_data(station):
    station = str(station).zfill(6)
    filename = "data/TG_STAID" + station + ".txt"

    dft = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    dft['   TG'] = dft['   TG']/10

    return dft.to_dict(orient="record")


@app.route("/api/v1/y/<station>/<year>")
def year_data(station, year):
    station = str(station).zfill(6)
    filename = "data/TG_STAID" + station + ".txt"

    dft = pd.read_csv(filename, skiprows=20)
    dft['    DATE'] = dft['    DATE'].astype(str)
    result = dft[dft['    DATE'].str.startswith(str(year))].to_dict(orient="record")

    return result


@app.route("/api/v1/d/<station>/<date>")
def date_data(station, date):
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
