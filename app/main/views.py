import flask
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import cachetools
import datetime

from . import main
from .forms import ImageForm
from .. import barcode_scanner
from .. import mutex


_OUTPUT_IMAGE_FORMAT = "PNG"
_OUTPUT_MIME_TYPE = "image/png"
cached_scanning_results = mutex.Mutex(
    cachetools.TTLCache(maxsize=100, ttl=datetime.timedelta(hours=1).total_seconds())
)


@main.route("/", methods=["GET", "POST"])
def index():
    form = ImageForm()
    if form.validate_on_submit():
        f = form.image_field.data
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        image_bytes = f.read()
        digest.update(image_bytes)
        image_hash_str = digest.finalize().hex()
        with cached_scanning_results.lock() as cache:
            if image_hash_str in cache.get():
                result = cache.get()[image_hash_str]
                print(f"{image_hash_str} found in cache")
            else:
                print(f"{image_hash_str} not found in cache, decode started")
                result = barcode_scanner.decode(image_bytes, _OUTPUT_IMAGE_FORMAT)
                cache.get()[image_hash_str] = result
        return flask.render_template(
            "index.html",
            form=form,
            image_hash=image_hash_str,
            barcodes=result.barcodes,
        )
    return flask.render_template("index.html", form=form)


@main.route("/scanned_image/<image_hash>/<int:barcode_index>")
def scanned_image(image_hash, barcode_index):
    with cached_scanning_results.lock() as cache:
        if image_hash in cache.get():
            result = cache.get()[image_hash]
            if 0 <= barcode_index < len(result.barcodes):
                return flask.Response(
                    result.barcodes[barcode_index].mini_image,
                    mimetype=_OUTPUT_MIME_TYPE,
                )
    flask.abort(404)
