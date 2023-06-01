from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ConfigForm(FlaskForm):
    config_file = FileField(
        "Upload a new config file",
        validators=[FileRequired(), FileAllowed(["json"], "JSON Files only")],
    )
