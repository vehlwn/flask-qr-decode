import os
from app import create_app, db

app = create_app(os.environ["FLASK_CONFIG"])


@app.cli.command()
def deploy():
    """Run deployment tasks."""

    db.create_all()
