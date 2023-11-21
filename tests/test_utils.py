from socket import AF_INET, SOCK_STREAM, socket
from unittest import TestCase, TestLoader, TextTestRunner

from src.utils import find_free_port, is_port_in_use


class UtilsTest(TestCase):
    def test_find_free_port(self):
        port = find_free_port()
        self.assertFalse(is_port_in_use(port))

        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind(("localhost", port))
            s.listen()
            self.assertTrue(is_port_in_use(port))


if __name__ == "__main__":
    suite = TestLoader().loadTestsFromTestCase(UtilsTest)
    TextTestRunner().run(suite)
