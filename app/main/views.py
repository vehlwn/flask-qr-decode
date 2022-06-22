import flask
import random
import zlib

from . import main
from .forms import ImageForm
from .. import barcode_scanner
from ..models import DecodedResultCache, BarcodeData
from .. import db


_OUTPUT_IMAGE_FORMAT = "PNG"
_OUTPUT_MIME_TYPE = "image/png"
_CRC32_VALUE = random.randint(0, 2 ** 32 - 1)


@main.route("/", methods=["GET", "POST"])
def index():
    form = ImageForm()
    if form.validate_on_submit():
        f = form.image.data
        image_bytes = f.read()
        input_image_hash = zlib.crc32(image_bytes, _CRC32_VALUE)
        cached_decoded_result = DecodedResultCache.query.filter_by(
            input_image_hash=input_image_hash
        ).first()
        if cached_decoded_result is None:
            try:
                result = barcode_scanner.decode(image_bytes, _OUTPUT_IMAGE_FORMAT)
            except Exception as ex:
                flask.abort(500, str(ex))
            if len(result.barcodes) == 0:
                return flask.render_template(
                    "no-barcodes-found.html",
                    form=form,
                )
            cached_decoded_result = DecodedResultCache(
                input_image_hash=input_image_hash
            )
            cached_decoded_result.add_result_datum(result)
            db.session.add(cached_decoded_result)
            db.session.commit()
        else:
            if len(cached_decoded_result.barcode_datum) == 0:
                return flask.render_template(
                    "no-barcodes-found.html",
                    form=form,
                )
        return flask.render_template(
            "scan-results.html",
            form=form,
            cached_decoded_result=cached_decoded_result,
        )
    return flask.render_template("main-form.html", form=form)


@main.route("/mini_image/<int:id>")
def mini_image(id: int):
    barcode_data = BarcodeData.query.filter_by(id=id).first_or_404()
    return flask.Response(
        barcode_data.mini_image,
        mimetype=_OUTPUT_MIME_TYPE,
    )
