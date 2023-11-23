from flask import Blueprint

from src.proxy.service import create_proxy, kill_proxy

proxy_blueprint = Blueprint("proxy", __name__)


@proxy_blueprint.route("/api/proxy", methods=["POST"])
def get_proxy():
    proxy = create_proxy()
    return {"id": proxy.id.hex, "proxy": proxy.url}, 201


@proxy_blueprint.route("/api/proxy/<id>", methods=["DELETE"])
def delete_proxy(id: str):
    kill_proxy(id)
    return f"Proxy {id} deleted"
