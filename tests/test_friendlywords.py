import unittest
import random

import friendlywords as fw


class TestFriendlyWords(unittest.TestCase):

    def setUp(self) -> None:
        fw.preload()

    def test_generate_separator(self):
        def _check(n, sep):
            self.assertEqual(len(fw.generate(n, separator=sep).split(sep)), n)

        _check(2, ' ')
        _check(3, '-')
        _check(4, '/')
        _check(5, ', ')

        # empty separator should produce one big str
        self.assertEqual(len(fw.generate(5, separator='').split()), 1)

    def test_generate_as_list(self):
        for n in range(1, 10):
            s = fw.generate(n, as_list=True)
            self.assertIsInstance(s, list)
            self.assertEqual(len(s), n)

    def test_generate_integers(self):
        for n in range(1, 10):
            self.assertEqual(len(fw.generate(n).split()), n)

    def test_generate_words(self):

        def _check(command):
            s = fw.generate(command).split()
            for c, w in zip(command, s):
                self.assertIn(w, fw.WORD_LISTS[c.lower()]['list'])
            self.assertEqual(len(s), len(command))

        _check('c')
        _check('o')
        _check('p')
        _check('t')
        _check('copt')
        _check('C')
        _check('O')
        _check('P')
        _check('T')
        _check('COPT')

    def test_inputs(self):
        with self.assertRaises(ValueError):
            fw.generate(0)
        with self.assertRaises(TypeError):
            fw.generate(3.14)
        with self.assertRaises(TypeError):
            fw.generate(10, separator=1)
        with self.assertRaises(ValueError):
            fw.generate('a')
        with self.assertRaises(ValueError):
            fw.generate('cccoooppptttz')

    def test_reproducibility(self):
        def _check(seed):
            random.seed(seed)
            a = fw.generate(10)
            random.seed(seed)
            b = fw.generate(10)
            self.assertEqual(a, b)

        _check(0)
        _check(42)
        _check(1337)
