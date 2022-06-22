import flask_wtf
import flask_wtf.file
import wtforms
import wtforms.validators


class ImageForm(flask_wtf.FlaskForm):
    image_field = flask_wtf.file.FileField(
        "", validators=[flask_wtf.file.FileRequired()],
    )
    submit = wtforms.SubmitField("Submit")
