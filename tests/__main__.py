import unittest

suite = unittest.TestLoader().discover("tests")
result = unittest.TextTestRunner(verbosity=2).run(suite)
