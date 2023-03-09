# from app import create_app
#
# app = create_app()
import os
from app import create_app
import faulthandler

faulthandler.enable()
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", 8080)))