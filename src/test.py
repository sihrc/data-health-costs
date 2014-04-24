import unittest
import get_features as gf


class Test(unittest.TestCase):
    def setUp(self):
        self.datafiles = [\
                        # "H147",\
                        # "H144D",\
                        # "H149",\
                        # "H143", \
                        # "H145",\
                        # "H146", \
                        # "H142", \
                        ]

    def test_read_tables(self):
        for datafile in self.datafiles:
            self.assertTrue(gf.read_tables(datafile))

if __name__ == "__main__":
    unittest.main()