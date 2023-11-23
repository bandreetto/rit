import unittest

from stem.util.log import logging
from src import app


class ProxyRoutesTests(unittest.TestCase):
    proxy_id: str 

    def setUp(self) -> None:
        logging.getLogger().handlers.clear()
        logging.basicConfig(
            format=f"%(asctime)s [%(levelname)s][{self._testMethodName}]: %(message)s",
            level=logging.DEBUG,
        )
        self.app = app.test_client()

    def test_post(self):
        response = self.app.post("/api/proxy")

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data["id"], str)
        self.assertRegex(data["proxy"], r"socks5:\/\/.+")

        self.proxy_id = data["id"]

    def test_delete(self):
        response = self.app.post("/api/proxy")

        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        response = self.app.delete(f"/api/proxy/{data["id"]}")
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        if hasattr(self, 'proxy_id'):
            self.app.delete(f"/api/proxy/{self.proxy_id}")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ProxyRoutesTests)
    unittest.TextTestRunner().run(suite)
