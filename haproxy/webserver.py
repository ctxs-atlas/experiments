

from flask import Flask

from listener_blueprint import listener_controller
from server_blueprint import server_controller
from monitor_blueprint import monitor_controller


app = Flask(__name__)

# Register all the REST Controllers
app.register_blueprint(listener_controller)
app.register_blueprint(server_controller)
app.register_blueprint(monitor_controller)


if __name__ == "__main__":
    app.run(debug=True)
