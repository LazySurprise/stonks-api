import unittest
import sys
from io import StringIO

from client import Reddit
from os import environ

class Test(unittest.TestCase):

    def test_1_1_parse_post_failure(self):
        Reddit2 = Reddit(mode='test')
        captured_output = StringIO()
        sys.stdout = captured_output 
        expected_output = 'stonk not found'
      
        post = ['PALANTIRRRR', 'IM RIDING PALANTIR!']
        parsed_stonk = Reddit2.parse_stonk(post)
        captured_output = captured_output.getvalue().rstrip('\n') 

        self.assertFalse(parsed_stonk)
        self.assertEqual(expected_output, captured_output)

    def test_1_2_parse_post_success(self):
        Reddit2 = Reddit(mode='test')
        expected_stonk = 'PLTR'
      
        post = ['PALANTIRRRR', 'IM RIDING PLTR']
        parsed_stonk = Reddit2.parse_stonk(post)

        self.assertTrue(parsed_stonk)
        self.assertEqual(expected_stonk, parsed_stonk)

    def test_2_1_parse_posts_failure(self):
        Reddit2 = Reddit(mode='test')
        captured_output = StringIO()
        sys.stdout = captured_output 
        expected_output = 'stonk not found\nstonk not found\nstonk not found' # TODO: lol hope noone sees this
      
        posts = [
            ['PALANTIRRRR', 'IM RIDING PALANTIR!', '2020-11-28'],
            ['elon is the worst', 'boooo elonnnn', '2020-01-01'],
            ['sdfsdfssdfs', 'sdffsdfsdf sdfsdfs sdfsfsd', '2020-05-23']
        ]
        parsed_stonks = Reddit2.parse_stonks(posts)
        captured_output = captured_output.getvalue().rstrip('\n') 

        self.assertFalse(parsed_stonks)
        self.assertEqual(expected_output, captured_output)
   
    def test_2_2_parse_posts_hybrid(self):
        Reddit2 = Reddit(mode='test')
        captured_output = StringIO()
        sys.stdout = captured_output 
        expected_output = 'stonk not found\nstonk not found' # TODO: lol hope noone sees this
        expected_stonks = [['TSLA', '2020-01-01']]

        posts = [
            ['PALANTIRRRR', 'IM RIDING PALANTIR!', '2020-11-28'],
            ['elon is the worst', 'but I loveeeee TSLA', '2020-01-01'],
            ['sdfsdfssdfs', 'sdffsdfsdf sdfsdfs sdfsfsd', '2020-05-23']
        ]
        parsed_stonks = Reddit2.parse_stonks(posts)
        captured_output = captured_output.getvalue().rstrip('\n') 

        self.assertTrue(parsed_stonks)
        self.assertEqual(expected_stonks, parsed_stonks)
        self.assertEqual(expected_output, captured_output)
        
    def test_2_3_parse_posts_success(self):
        Reddit2 = Reddit(mode='test')
        expected_stonks = [
            ['MSFT', '2020-11-28'],
            ['TSLA', '2020-01-01']
        ]

        posts = [
            ['riding msft', 'BILL GATES Vaccine ! MSFT 4 lifeeee!', '2020-11-28'],
            ['elon is the worst', 'but I loveeeee TSLA', '2020-01-01'],
        ]
        parsed_stonks = Reddit2.parse_stonks(posts)

        self.assertTrue(parsed_stonks)
        self.assertEqual(expected_stonks, parsed_stonks)

    def test_3_1_get_stonks_failure(self):
        def mock_fetch():
            posts = [
                ['PALANTIRRRR', 'IM RIDING PALANTIR!', '2020-11-28'],
                ['elon is the worst', 'boooo elonnnn', '2020-01-01'],
                ['sdfsdfssdfs', 'sdffsdfsdf sdfsdfs sdfsfsd', '2020-05-23']
            ]
            return posts

        Reddit2 = Reddit(mode='test')
        Reddit2.fetch_stonks = mock_fetch
        captured_output = StringIO()
        sys.stdout = captured_output 
        expected_output = 'stonk not found\nstonk not found\nstonk not found' # TODO: lol hope noone sees this

        stonks = Reddit2.get_stonks()
        captured_output = captured_output.getvalue().rstrip('\n') 

        self.assertFalse(stonks)
        self.assertEqual(expected_output, captured_output)
   
    def test_3_2_get_stonks_hybrid(self):
        def mock_fetch():
            posts = [
                ['PALANTIRRRR', 'IM RIDING PALANTIR!', '2020-11-28'],
                ['elon is the worst', 'but I loveeeee TSLA', '2020-01-01'],
                ['sdfsdfssdfs', 'sdffsdfsdf sdfsdfs sdfsfsd', '2020-05-23']
            ]
            return posts

        Reddit2 = Reddit(mode='test')
        Reddit2.fetch_stonks = mock_fetch
        captured_output = StringIO()
        sys.stdout = captured_output 
        expected_output = 'stonk not found\nstonk not found' # TODO: lol hope noone sees this
        expected_stonks = [['TSLA', '2020-01-01']]

        stonks = Reddit2.get_stonks()
        captured_output = captured_output.getvalue().rstrip('\n') 

        self.assertTrue(stonks)
        self.assertEqual(expected_stonks, stonks)
        self.assertEqual(expected_output, captured_output)
        
    def test_3_3_get_stonks_success(self):
        def mock_fetch():
            posts = [
                ['riding msft', 'BILL GATES Vaccine ! MSFT 4 lifeeee!', '2020-11-28'],
                ['elon is the worst', 'but I loveeeee TSLA', '2020-01-01'],
            ]
            return posts

        Reddit2 = Reddit(mode='test')
        Reddit2.fetch_stonks = mock_fetch
        expected_stonks = [
            ['MSFT', '2020-11-28'],
            ['TSLA', '2020-01-01']
        ]

        stonks = Reddit2.get_stonks()

        self.assertTrue(stonks)
        self.assertEqual(expected_stonks, stonks)


if __name__=='__main__':
    unittest.main()
