import os
import argparse

from app import create_app

app = create_app(os.getenv("FLASK_CONFIG") or "default")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="HTTP server to decode barcodes in images"
    )
    parser.add_argument(
        "--host", help="host where to bind web server", type=str, default="0.0.0.0",
    )
    parser.add_argument(
        "--port", help="port where to bind web server", type=int, default=2988,
    )
    args = parser.parse_args()
    app.run(
        host=args.host, port=args.port, debug=True, threaded=True, use_reloader=False
    )
