import unittest


class ServiceTest(unittest.TestCase):

    def test_instantiation(self):

        from dna.middleware.models.service import Service
        service = Service()
        assert isinstance(service, Service)


if "__main__" == __name__:
    unittest.main()
