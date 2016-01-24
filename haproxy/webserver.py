

from flask import Flask

from server_blueprint import server_controller
from monitor_blueprint import monitor_controller

app = Flask(__name__)
app.register_blueprint(monitor_controller)
app.register_blueprint(server_controller)

if __name__ == "__main__":
    app.run(debug=True)
