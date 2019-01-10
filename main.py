from flask import Flask,render_template,request,send_file
import pandas
from geopy.geocoders import ArcGIS
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success-table", methods=['POST'])
def success_table():
    global filename
    if request.method == 'POST':
        file = request.files["file"]                                                      # saves file uploaded by user
        try:                                                                                       # checks .csv file
            df=pandas.read_csv(file)
            nom = ArcGIS(timeout=10)
            if 'address' in df.columns:                                                          #checks address in df.column
                df['address'] = df['address']
            elif 'Address' in df.columns:
                df["address"] = df['Address']
            else:
                return render_template("index.html", text ="Please make sure you have an Address column in your csv file .!")

            df["Coordinates"] = df["address"].apply(nom.geocode)
            df["Latitude"] = df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
            df["Longitude"] = df["Coordinates"].apply(lambda x: x.longitude if x != None else None)
            df = df.drop("address", 1)
            df = df.drop("Coordinates", 1)
            filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"+".csv")     # unique filename
            df.to_csv(filename,index=None)

            return render_template("index.html", data_html = df.to_html(),btn="download.html")            # print table
        except Exception:
            return render_template("index.html" , issue = "Please upload .CSV file.!")

@app.route("/success-table/")
def download():
    return send_file(filename,attachment_filename="yourFile.csv",as_attachment=True)

if __name__=='__main__':
    app.run(debug = True)