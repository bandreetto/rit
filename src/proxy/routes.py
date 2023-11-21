from flask import Blueprint

proxy_blueprint = Blueprint("proxy", __name__)


@proxy_blueprint.route("/api/proxy", methods=["GET"])
def get_proxy():
    raise NotImplementedError()
