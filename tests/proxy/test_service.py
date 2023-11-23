from time import sleep
import unittest
import requests
from stem.control import os
from stem.util.log import logging

from src.proxy.service import Proxy, create_proxy, kill_proxy
from src.utils import is_port_in_use

ip_regex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"


class ProxyServiceTests(unittest.TestCase):
    proxy: Proxy

    def setUp(self) -> None:
        logging.getLogger().handlers.clear()
        logging.basicConfig(
            format=f"%(asctime)s [%(levelname)s][{self._testMethodName}]: %(message)s",
            level=logging.DEBUG,
        )
        self.proxy = create_proxy()

    def test_create_proxy(self):
        proxy = self.proxy

        self.assertIsInstance(proxy.url, str)

        my_ip = requests.get("http://ifcfg.me").text
        proxy_ip = requests.get(
            "http://ifcfg.me", proxies={"http": proxy.url, "https": proxy.url}
        ).text

        self.assertRegex(my_ip, ip_regex)
        self.assertRegex(proxy_ip, ip_regex)
        self.assertNotEqual(my_ip, proxy_ip)

    def test_proxy_should_have_BR_ip(self):
        proxy = self.proxy
        proxy_ip = requests.get(
            "http://ip-api.com/json",
            proxies={"http": proxy.url, "https": proxy.url},
        ).json()

        self.assertEqual(proxy_ip["countryCode"], "BR")

    def text_destroy_inexistent_proxy(self):
        kill_proxy("some random string")
        pass

    def test_destroy_proxy(self):
        proxy = self.proxy

        ip = requests.get(
            "http://ifcfg.me", proxies={"http": proxy.url, "https": proxy.url}
        ).text
        self.assertRegex(ip, ip_regex)

        kill_proxy(proxy.id.hex)
        self.proxy = None  # type: ignore

        sleep(1)
        self.assertFalse(is_port_in_use(proxy.port))
        self.assertFalse(os.path.exists(proxy.data_dir))

    def tearDown(self) -> None:
        if self.proxy:
            kill_proxy(self.proxy.id.hex)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ProxyServiceTests)
    unittest.TextTestRunner().run(suite)
