import os
import unittest
from bs4 import BeautifulSoup

from scrapping_indeed import Indeed

class Test(unittest.TestCase):

    def test__init__(self):

        testClass = Indeed()
        
        """ testClass.readJson("journeys?from=stop_area:OCE:SA:87686006&to=stop_area:OCE:SA:87722025") 
        #self.assertTrue(os.path.exists('./my_stop_areas.csv')) """
        
        #self.assertTrue(isinstance(testClass.results, bs4.element.Tag))
        self.assertTrue(testClass.results != '')
        self.assertTrue(len(testClass.a_links)> 1)
        
        #self.assertTrue(os.path.exists('./stop_areas_maria.json'))

    """ def test_getJson(self):
            testClass = Sncf()
            self.assertEqual(type(testClass.getJson()),dict)
    
        def test_combien_arrets(self):
            testClass = Sncf()
            self.assertEqual(type(testClass.combien_arrets("journeys?from=stop_area:OCE:SA:87686006&to=stop_area:OCE:SA:87722025")),int) 
    """

if __name__  == '__main__':
    unittest.main(verbosity =2)