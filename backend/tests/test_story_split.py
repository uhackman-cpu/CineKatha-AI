import unittest
from cinekatha import split_scenes

class SplitScenesTests(unittest.TestCase):
    def test_splits_paragraphs(self):
        scenes = split_scenes('पहला दृश्य।\n\nदूसरा दृश्य।')
        self.assertEqual(len(scenes), 2)

    def test_empty_story_rejected(self):
        with self.assertRaises(ValueError):
            split_scenes('   ')

if __name__ == '__main__':
    unittest.main()
