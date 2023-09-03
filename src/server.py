import os
import threading
from flask import Flask, current_app
from flask import send_from_directory


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "../res"


@app.route("/schedule/<filename>", methods=["GET", "POST"])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config["UPLOAD_FOLDER"])
    return send_from_directory(uploads, filename + ".ics", as_attachment=True)


def start():
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False, ssl_context='adhoc')


SERVER_THREAD = threading.Thread(target=start)
SERVER_THREAD.daemon = True
SERVER_THREAD.start()
