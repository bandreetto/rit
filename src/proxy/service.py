import logging
from shutil import rmtree
from tempfile import mkdtemp
from typing import NamedTuple
from stem.control import Controller, Signal
from stem.process import launch_tor_with_config

from src.utils import find_free_port


class Proxy(NamedTuple):
    url: str
    port: str
    control_port: str
    data_dir: str


def create_proxy() -> Proxy:
    logging.info("Creating data directory")
    data_dir = mkdtemp()
    logging.info(f"Data directory {data_dir} created for proxy")

    try:
        logging.info("Finding a free ports for the tor process")
        socks_port = find_free_port()
        control_port = find_free_port()
        logging.info(f"Found ports {socks_port} and {control_port}!")

        logging.info("Launching tor")
        launch_tor_with_config(
            config={
                "ControlPort": str(control_port),
                "SOCKSPort": str(socks_port),
                "DataDirectory": data_dir,
            },
            init_msg_handler=logging.info,
            take_ownership=True,
        )
        logging.info("Tor Successfully Launched")

        logging.info(f"Socks port: {socks_port}")
        logging.info(f"Control port: {control_port}")

        return Proxy(
            f"socks5://localhost:{socks_port}", socks_port, control_port, data_dir
        )
    except Exception as e:
        logging.warn(
            "Something wen't wrong on proxy creation, cleaning up data directory"
        )
        rmtree(data_dir)
        logging.info("Data dir successfully removed!")
        raise e


def kill_proxy(proxy: Proxy):
    logging.info(f"Trying to kill proxy allocated on port {proxy.port}")
    logging.info("Killing tor process")
    with Controller.from_port(port=proxy.control_port) as controller:
        controller.authenticate()
        controller.signal(Signal.SHUTDOWN)  # type: ignore
    logging.info("Tor process killed successfully!")

    logging.info(f"Removing proxy data directory {proxy.data_dir}")
    rmtree(proxy.data_dir)
    logging.info(f"Data directory removed {proxy.data_dir} successfully!")
