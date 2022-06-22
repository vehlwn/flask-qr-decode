import os
from app import create_app, db

app = create_app(os.getenv("FLASK_CONFIG") or "docker")


@app.cli.command()
def deploy():
    """Run deployment tasks."""

    db.create_all()
