from datetime import datetime
import flask
import zlib
import os
import sys

from . import main
from .. import barcode_scanner
from ..models import DecodedResultCache, BarcodeData
from .forms import ImageForm


_OUTPUT_IMAGE_FORMAT = "PNG"
_OUTPUT_MIME_TYPE = "image/png"
_CRC32_VALUE = int(os.environ["FLASK_HASH_INITIAL_VALUE"])


@main.route("/", methods=["GET", "POST"])
def index():
    form = ImageForm()
    if form.validate_on_submit():
        f = form.image.data
        image_bytes = f.read()
        input_image_hash = zlib.crc32(image_bytes, _CRC32_VALUE)
        cached_decoded_result = DecodedResultCache.objects(
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
                )
            cached_decoded_result = DecodedResultCache(
                input_image_hash=input_image_hash
            )
            cached_decoded_result.add_result_datum(result)
        else:
            cached_decoded_result.timestamp = datetime.utcnow()
        cached_decoded_result.save()
        return flask.render_template(
            "scan-results.html",
            cached_decoded_result=cached_decoded_result,
        )
    return flask.render_template("main-form.html", form=form)


@main.route("/mini_image/<int:id>")
def mini_image(id: int):
    cached_decoded_result = list(
        DecodedResultCache.objects.aggregate(
            [
                {"$match": {"barcode_datum.id": id}},
                {
                    "$project": {
                        "barcode_datum": {
                            "$filter": {
                                "input": "$barcode_datum",
                                "as": "barcode_data",
                                "cond": {"$eq": ["$$barcode_data.id", id]},
                            }
                        }
                    }
                },
            ]
        )
    )[0]
    barcode_data = cached_decoded_result["barcode_datum"][0]
    return flask.Response(
        barcode_data["mini_image"],
        mimetype=_OUTPUT_MIME_TYPE,
    )
