from flask import Flask, render_template
import pandas as pd 

data = pd.read_csv("data_small\stations.txt",skiprows=17)[['STAID','STANAME                                 ']]
data = data.to_html()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html",data = data)


@app.route("/api/v1/<station>/<date>")
def about(station,date):
    date = str(date)
    date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
    station = str(station).zfill(6)
    
    df = pd.read_csv(f"data_small\TG_STAID{station}.txt",skiprows = 20,parse_dates=["    DATE"])
    
    temperature = df[df["    DATE"] == date]['   TG'].squeeze()
    
    #print("TEMPPPP", len(temperature))
    return {
        "station":station,
        "date":date,
        "temperature": str(temperature/10.0)
        
    }
    
@app.route("/api/v1/<station>")
def all_data(station):
    station = str(station).zfill(6)
    df = pd.read_csv(f"data_small\TG_STAID{station}.txt",skiprows = 20,parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result

@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station,year):
    station = str(station).zfill(6)
    df = pd.read_csv(f"data_small\TG_STAID{station}.txt",skiprows = 20)
    df["    DATE"] = df["    DATE"].astype(str)
    df = df[["    DATE",'   TG']]
    df['   TG'] = df['   TG'] / 10.0
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result
    
#f __name__ == "main":
app.run(debug=True)