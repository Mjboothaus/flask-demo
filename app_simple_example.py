# https://stackoverflow.com/questions/20207448/flask-wtform-render-selected-with-bootstrap

from flask import Flask, render_template
from flask_wtf import Form
from wtforms import SelectField

app = Flask(__name__)
app.secret_key = 'Testing BS'

choices = [
    ('1', 'Alice'),
    ('2', 'Bob'),
    ('3', 'Carol'),
]


class MyForm(Form):
    name = SelectField('Pick Name', choices=choices)


@app.route('/', methods=['post', 'get'])
def hello_world():
    form = MyForm()
    form.name.data = '2'  # lets set Bob to be active.
    return render_template('simple_example.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
