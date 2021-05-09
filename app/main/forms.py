import PIL.Image
import flask_wtf
import flask_wtf.file
import io
import wtforms


def _pil_image_check(form, field):
    f = field.data
    image_bytes = f.read()
    f.seek(0)
    input_stream = io.BytesIO(image_bytes)
    try:
        PIL.Image.open(input_stream).convert("RGB")
    except Exception as ex:
        raise wtforms.ValidationError(str(ex))


class ImageForm(flask_wtf.FlaskForm):
    image = flask_wtf.file.FileField(
        "Image file",
        validators=[flask_wtf.file.FileRequired(), _pil_image_check],
    )
    submit = wtforms.SubmitField("Submit")
