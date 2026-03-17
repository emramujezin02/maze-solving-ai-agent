from analytics.database import init_db
init_db()

from web.flask_app import app
app.run(debug=True)
