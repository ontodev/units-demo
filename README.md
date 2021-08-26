# OBO Units Demo

This is a small Flask app that demonstrates the [`ontodev-units`](https://github.com/ontodev/units) package to convert UCUM codes to linked data.

To get started, install the requirements:
```
python3 -m pip install -r requirements.txt
```

Then run the app:
```
export FLASK_APP=run.py
flask run
```

By default, the base IRI for unit outputs is `https://w3id.org/units/`. If you want to change this, you can do so by setting the `UNIT_BASE_IRI` environment variable before running (`FLASK_APP` still needs to be set as well):
```
export UNIT_BASE_IRI=http://example.com/
flask run
```