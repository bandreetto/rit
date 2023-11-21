import unittest
from src import app


class ProxyRoutesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def test_get(self):
        response = self.app.get("/api/proxy")

        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.data["proxy"], r"socks5:\/\/.+")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ProxyRoutesTests)
    unittest.TextTestRunner().run(suite)
