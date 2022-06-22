import datetime
import sys

from . import db
from . import barcode_scanner

_HASH_COLUMN = db.Numeric(10)


class BarcodeData(db.Model):
    __tablename__ = "barcode_data"
    id = db.Column(db.Integer, primary_key=True)
    code_type = db.Column(db.Text)
    str_data = db.Column(db.Text)
    mini_image = db.Column(db.LargeBinary)
    input_image_hash = db.Column(
        _HASH_COLUMN,
        db.ForeignKey("decoded_result_cache.input_image_hash", ondelete="CASCADE"),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DecodedResultCache(db.Model):
    __tablename__ = "decoded_result_cache"
    input_image_hash = db.Column(
        _HASH_COLUMN,
        primary_key=True,
    )
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    barcode_datum = db.relationship(
        "BarcodeData",
        backref="decoded_result",
        cascade="all, delete, delete-orphan",
        passive_deletes=True,
    )

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


@db.event.listens_for(DecodedResultCache, "before_insert")
def clean_cache(_mapper, _connection, _target):
    now = datetime.datetime.utcnow()
    expire_period = datetime.timedelta(hours=1)
    too_old = now - expire_period
    db.session.query(DecodedResultCache).filter(
        DecodedResultCache.timestamp <= too_old
    ).delete()
