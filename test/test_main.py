import unittest


class MainTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_main(self):
        self.assertEqual(1, 1)

    def tearDown(self):
        pass


def suite():
    main_suite = unittest.TestSuite()
    main_suite.addTest(unittest.makeSuite(MainTest))
    return main_suite

# run all tests
unittest.TextTestRunner().run(suite())
