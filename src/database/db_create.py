from src.database import db
from src import create_app

app = create_app()
app.app_context().push()

db.create_all()