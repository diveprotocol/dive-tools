from flask import Blueprint, request, jsonify, render_template
from .services import check_dive_protection
from config import Config

bp = Blueprint("dive_api", __name__)

@bp.route("/")
def index():
    """Render the dev tool interface."""
    return render_template("index.html")

@bp.route("/api/check", methods=["GET", "POST"])
def check():
    """Check if a URL is protected by DIVE."""
    if request.method == "POST":
        data = request.get_json()
        url = data.get("url")
    else:
        url = request.args.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    result = check_dive_protection(url, require_dnssec=Config.REQUIRE_DNSSEC)

    if result.error:
        return jsonify({"error": result.error}), 400

    return jsonify({
        "url": result.url,
        "is_protected": result.is_protected,
        "scope": result.scope,
        "policy_domain": result.policy_domain,
        "policy_fqdn": result.policy_fqdn,
        "dnssec_validated": result.dnssec_validated,
        "directives": result.directives,
        "keys": result.keys,
    })

def init_app(app):
    app.register_blueprint(bp)
