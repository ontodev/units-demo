from io import BytesIO

from flask import Flask, redirect, render_template, request, send_file, url_for
from rdflib import RDF, OWL
from units.convert import convert, graph_to_html
from units.helpers import get_exponents, get_mappings, get_prefixes, get_si_mappings
from urllib.parse import unquote_plus

app = Flask(__name__)

UNITS_EXPONENTS = get_exponents()
UNITS_MAPPINGS = get_mappings()
UNITS_PREFIXES = get_prefixes()
UNITS_SI_MAPPINGS = get_si_mappings()

EXAMPLES = [
    ("/A/s3/cg3/T3", "A-1.s-3.cg-3.T-3"),
    ("/g", "g-1"),
    ("/m3", "m-3"),
    ("%", "%"),
    ("aBq", "aBq"),
    ("Cel.d-1", "Cel.d-1"),
    ("dL/g", "dL.g-1"),
    ("dlm", "dlm"),
    ("dlx", "dlx"),
    ("Em.s-2", "Em.s-2"),
    ("g.cm-3", "g.cm-3"),
    ("K2", "K2"),
    ("kW/h", "kW.h-1"),
    ("m/s", "m.s-1"),
    ("m.s-2", "m.s-2"),
    ("m/s/d", "m.s-1.d-1"),
    ("mmol.mL-1", "mmol.mL-2"),
    ("mol.L-1", "mol.L-1"),
    ("mol.um", "mol.um"),
    ("ng-1", "ng-1"),
    ("pA", "pA"),
    ("ug.mL-1", "ug.mL-1"),
    ("umol.L-1", "umol.L-1"),
    ("us", "us"),
    ("Wb", "Wb"),
]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ucum_code = request.form.get("ucum_code")
        if not ucum_code:
            return error("A UCUM code is required.")
        ucum_code = unquote_plus(ucum_code)
        try:
            gout = convert(
                [ucum_code],
                UNITS_SI_MAPPINGS,
                UNITS_PREFIXES,
                UNITS_EXPONENTS,
                UNITS_MAPPINGS,
                fail_on_err=True,
            )
        except (RecursionError, ValueError):
            return error(f"'{ucum_code}' is not a valid UCUM code.")
        # The canonical code used in IRI may be different than provided code
        iri = str(list(gout.subjects(RDF.type, OWL.NamedIndividual))[0])
        url_code = unquote_plus(iri.replace("https://w3id.org/units/", ""))
        return redirect(url_for("show_ucum", ucum_code=url_code))
    return render_template("index.html", examples=EXAMPLES)


@app.route("/<ucum_code>")
def show_ucum(ucum_code):
    try:
        gout = convert(
            [ucum_code],
            UNITS_SI_MAPPINGS,
            UNITS_PREFIXES,
            UNITS_EXPONENTS,
            UNITS_MAPPINGS,
            fail_on_err=True,
        )
    except (RecursionError, ValueError):
        return error(f"'{ucum_code}' is not a valid UCUM code.")
    outfmt = request.args.get("format")
    if outfmt:
        # Return a download file
        if outfmt == "ttl":
            mt = "text/turtle"
            outstr = gout.serialize(format=outfmt)
        elif outfmt == "json-ld":
            mt = "application/ld+json"
            # Serialize the graph with context
            jsonld_context = {}
            for ns, base in dict(gout.namespaces()).items():
                jsonld_context[ns] = str(base)
            jsonld_context = {"@context": jsonld_context}
            outstr = gout.serialize(format=outfmt, context=jsonld_context)
            # File extension should just be .json
            outfmt = "json"
        else:
            return error(f"'{outfmt}' is not a valid export format.")
        buffer = BytesIO()
        # Handle backwards compatibility for rdflib 5.x.x (bytes output) and 6.x.x (str output)
        if isinstance(outstr, str):
            buffer.write(outstr.encode("utf-8-sig"))
        else:
            buffer.write(outstr)
        buffer.seek(0)
        return send_file(
            buffer, mimetype=mt, attachment_filename=f"{ucum_code}.{outfmt}", as_attachment=True
        )
    html = graph_to_html(gout)
    return render_template("term.html", html=html)


def error(message):
    html = "<h3>Oops!</h3>"
    html += f'<p>{message} <a href="/">Go back</a>.</p>'
    return render_template("base.html", default=html), 400
