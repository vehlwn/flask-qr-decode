import PIL.Image
import PIL.ImageDraw
from pyzbar import pyzbar
import typing
import io


class DecodedBarcodeData:
    def __init__(self, code_type: str, str_data: str, mini_image: bytes):
        self.code_type = code_type
        self.str_data = str_data
        self.mini_image = mini_image


class Result:
    def __init__(self, barcodes: typing.List[DecodedBarcodeData]):
        self.barcodes = barcodes


def _lerp(x0, x1, y0, y1, x):
    return y0 * (x - x1) / (x0 - x1) + y1 * (x - x0) / (x1 - x0)


def decode(image_bytes: bytes, output_format: str = "PNG") -> Result:
    input_stream = io.BytesIO(image_bytes)
    image = PIL.Image.open(input_stream).convert("RGB")
    barcodes: typing.List[DecodedBarcodeData] = []
    LINE_WIDTH = 2
    MINI_SIZE = 150
    old_width = image.width
    old_height = image.height
    for code in pyzbar.decode(image):
        rect = code.rect
        mini_image = image.copy()
        mini_image.thumbnail((MINI_SIZE, MINI_SIZE))
        mini_width = mini_image.width
        mini_height = mini_image.height
        draw = PIL.ImageDraw.Draw(mini_image)
        draw.rectangle(
            (
                (
                    _lerp(0, old_width, 0, mini_width, rect.left),
                    _lerp(0, old_height, 0, mini_height, rect.top),
                ),
                (
                    _lerp(0, old_width, 0, mini_width, rect.left + rect.width),
                    _lerp(0, old_height, 0, mini_height, rect.top + rect.height),
                ),
            ),
            outline="#ff0000",
            width=LINE_WIDTH,
        )
        points = [
            (
                _lerp(0, old_width, 0, mini_width, point[0]),
                _lerp(0, old_height, 0, mini_height, point[1]),
            )
            for point in code.polygon
        ]
        print("points =", points)
        points.append(points[0])
        points.append(points[1])
        draw.line(points, fill="#0000ff", width=LINE_WIDTH, joint="curve")
        output_stream = io.BytesIO()
        mini_image.save(output_stream, format=output_format)
        barcodes.append(
            DecodedBarcodeData(
                code.type, code.data.decode("utf-8"), output_stream.getvalue()
            )
        )
    return Result(barcodes)
