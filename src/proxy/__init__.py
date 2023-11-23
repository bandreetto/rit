from flask import Blueprint

from src.proxy.service import create_proxy

proxy_blueprint = Blueprint("proxy", __name__)


@proxy_blueprint.route("/api/proxy", methods=["GET"])
def get_proxy():
    proxy = create_proxy()
    return {"proxy": proxy.url}
