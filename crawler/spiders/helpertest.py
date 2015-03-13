__author__ = 'Kandito Agung'

import unittest
import helper
from datetime import datetime

class MyTestCase(unittest.TestCase):
    def test_kompas_date_0(self):
        self.assertEqual(None, None)


    def test_kompas_date_1(self):
        date = datetime.strptime("2015-03-13 21:59:00.000", "%Y-%m-%d %H:%M:%S.%f")
        self.assertEqual(helper.kompas_date("Jumat, 13 Maret 2015 | 21:59 WIB "), date)

    def test_kompas_date_2(self):
        date = datetime.strptime("2015-03-14 00:19:00.000", "%Y-%m-%d %H:%M:%S.%f")
        self.assertEqual(helper.kompas_date("Sabtu, 14 Maret 2015 | 00:19 WIB "), date)

    def test_kompas_date_3(self):
        date = datetime.strptime("2015-03-12 19:49:00.000", "%Y-%m-%d %H:%M:%S.%f")
        self.assertEqual(helper.kompas_date("Kamis, 12 Maret 2015 | 19:49 WIB "), date)

if __name__ == '__main__':
    unittest.main()
