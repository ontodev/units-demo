# Units of Measurement Server

This is a small Flask app that demonstrates the [`units-of-measurement`](https://github.com/units-of-measurement/units-of-measurement) package to convert UCUM codes to linked data.

To get started, install the requirements:
```
python3 -m pip install -r requirements.txt
```

Then run the app:
```
export FLASK_APP=run.py
flask run
```

By default, the base IRI for unit outputs is `https://w3id.org/uom/`. If you want to change this, you can do so by setting the `UNIT_BASE_IRI` environment variable before running (`FLASK_APP` still needs to be set as well):
```
export UNIT_BASE_IRI=http://example.com/
flask run
```
