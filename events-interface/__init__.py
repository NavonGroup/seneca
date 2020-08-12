import os, json, functools
from flask import Flask, request, render_template, jsonify
import sys, pathlib
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('events-interface', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

file_folder = Path("C:/Users/Laura/seneca/events-interface")
    
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "events-interface.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route("/form", methods=("GET", "POST"))
    def form():
        if request.method == 'POST':
            data = request.get_json()
            data_formatted = json.dumps(data, indent=2)
            print(data_formatted)
            with open('form.txt', 'w') as file:
                json.dump(data_formatted, file)
        return render_template("form.html")
    
    

    @app.route("/spreadsheet", methods=("GET", "POST"))
    def spreadsheet():
        with open(file_folder/'config.txt') as config_file:
            config_json = json.load(config_file)
        event_config = {
                        "types": list(config_json.keys()),
                        "example_data": list(config_json.values())
                         }
        event_config["type_parameters"]={}
        for type in config_json:
            event_config["type_parameters"][type]=list(config_json[type].keys())
        event_config["all_parameters"] = []
        for event in event_config["type_parameters"]:
            for parameter in event_config["type_parameters"][event]:
                event_config["all_parameters"].append(parameter)
        event_config["all_parameters"] = list(set(event_config["all_parameters"]))

        if request.method == 'POST':
            dataObj = request.get_json()
            events = dataObj.keys()
            columns = json.loads(dataObj[list(events)[0]]["data"])["header"]
            logic = {}
            for event in events:
                subEventsObj = json.loads(dataObj[event]["data"])["body"]
                eventData ={}
                eventData["seqType"] = dataObj[event]["sequenceType"]
                frmtData = []
                for subEvent in subEventsObj:
                    subEventType = subEvent[2]
                    subColumns = config_json[subEventType].keys()
                    frmtSubEvent = {}
                    # the first two columns do not contain data
                    for key in subColumns:
                        columnIndex = columns.index(key)
                        frmtSubEvent[key] = subEvent[columnIndex]
                    frmtData.append(frmtSubEvent)
                eventData["subEvents"] = frmtData
                logic[event]=eventData
            print (json.dumps(logic, indent=2))
            with open('spreadsheet.json', 'w') as file:
                json.dump(logic,file, indent=2)
        return render_template("spreadsheet.html", config1="about", config=event_config)
    
    @app.route("/spreadsheet/uploaded", methods=("GET", "POST"))
    def spreadsheetU():
        if request.method =='POST':
                print ('ok')
        return render_template("spreadsheet.html")
    
    @app.route("/spreadsheetM", methods=("GET", "POST"))
    def spreadsheetM():
        return render_template("spreadsheet_multiple.html")
    
    @app.route("/editor", methods=("GET", "POST"))
    def editor():
        return render_template("editor.html")

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
