from datetime import datetime

from . import barcode_scanner
from . import db


class BarcodeData(db.EmbeddedDocument):
    id = db.SequenceField()
    code_type = db.StringField(required=True)
    str_data = db.StringField(required=True)
    mini_image = db.BinaryField(required=True)


class DecodedResultCache(db.Document):
    input_image_hash = db.IntField(
        primary_key=True,
        min_value=0,
        max_value=2 ** 32 - 1,
    )
    timestamp = db.DateTimeField(required=True, default=datetime.utcnow)
    barcode_datum = db.ListField(db.EmbeddedDocumentField(BarcodeData))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_result_datum(self, result: barcode_scanner.Result):
        for barcode in result.barcodes:
            self.barcode_datum.append(
                BarcodeData(
                    code_type=barcode.code_type,
                    str_data=barcode.str_data,
                    mini_image=barcode.mini_image,
                )
            )
