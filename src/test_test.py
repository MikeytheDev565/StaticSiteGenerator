import unittest
from main import extract_title




class TestExtractTitle(unittest.TestCase):
    def test_Extracttitle(self):
        md = "# Hello World!!"
        self.assertEqual("Hello World!!", extract_title(md))



if __name__ == "__main__":
    unittest.main()