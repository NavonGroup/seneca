import os, json, functools
from flask import Flask, request, render_template, jsonify
import sys, json
    
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "seneca_front.sqlite"),
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
    
    #drag and drop example
    @app.route("/test", methods=("GET", "POST"))
    def test():
        data = request.get_json()
        print (data)
        with open('data.txt', 'w') as file:
            file.write(json.dumps(data, indent=4))
        return render_template("test.html")
    
    @app.route("/form", methods=("GET", "POST"))
    def form():
        if request.method == 'POST':
            data2 = request.get_json()
            print (data2)
            k =json.dumps(data2, indent=2)
            print (k)
            with open('form.txt', 'w') as file:
                json.dump(data2,file)
        return render_template("form.html")

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app