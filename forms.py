from wtforms import Form, BooleanField, StringField, SelectField, SubmitField

class AddPlay(Form):
    """form for splunk automation"""
    play_name = StringField("PlayName")
    playbook_status = SelectField(
        "Region",
        choices=[
            ("EU-DE-1", "EU-DE-1"),
            ("EU-NL-1", "EU-NL-1")
            ])
    playbook_test = SelectField(
        "Size",
        choices=[
            ("medium", "medium"),
            ("large", "large")])
    checkbox = BooleanField("Checkbox")
    submit = SubmitField('Build')
