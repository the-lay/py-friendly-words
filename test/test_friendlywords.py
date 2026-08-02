import os
import random
import subprocess
import sys
import unittest

import friendlywords as fw


class TestFriendlyWords(unittest.TestCase):
    def test_version(self):
        self.assertIsInstance(fw.__version__, str)
        self.assertTrue(fw.__version__)

    def test_word_lists_loaded_on_import(self):
        code = (
            "import friendlywords as fw; import sys; "
            "sys.exit(0 if all(fw.WORD_LISTS[c]['list'] for c in fw.WORD_LISTS) else 1)"
        )
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        result = subprocess.run([sys.executable, "-c", code], cwd=repo_root)
        self.assertEqual(result.returncode, 0, "word lists should be loaded at import, without preload()")

    def test_preload_is_deprecated_noop(self):
        with self.assertWarns(DeprecationWarning):
            fw.preload()

    def test_generate_uses_list_contents(self):
        original = fw.WORD_LISTS["t"]["list"]
        self.addCleanup(lambda: fw.WORD_LISTS["t"].update(list=original, n=len(original)))
        fw.WORD_LISTS["t"]["list"] = ["solo"]
        for _ in range(20):
            self.assertEqual(fw.generate("t"), "solo")

    def test_generate_empty_string_raises(self):
        with self.assertRaises(ValueError):
            fw.generate("")

    def test_generate_with_rng_is_reproducible(self):
        a = fw.generate(10, rng=random.Random(42))
        b = fw.generate(10, rng=random.Random(42))
        self.assertEqual(a, b)

    def test_generate_with_rng_keeps_global_state_untouched(self):
        random.seed(7)
        expected = random.random()
        random.seed(7)
        fw.generate(5, rng=random.Random(0))
        self.assertEqual(random.random(), expected)

    def test_generate_separator(self):
        def _check(n: int, sep: str) -> None:
            self.assertEqual(len(fw.generate(n, separator=sep).split(sep)), n)

        _check(2, " ")
        _check(3, "-")
        _check(4, "/")
        _check(5, ", ")

        # empty separator should produce one big str
        self.assertEqual(len(fw.generate(5, separator="").split()), 1)

    def test_generate_as_list(self):
        for n in range(1, 10):
            s = fw.generate(n, as_list=True)
            self.assertIsInstance(s, list)
            self.assertEqual(len(s), n)

    def test_generate_integers(self):
        for n in range(1, 10):
            self.assertEqual(len(fw.generate(n).split()), n)

    def test_generate_words(self):
        def _check(command: str) -> None:
            s = fw.generate(command).split()
            for c, w in zip(command, s):
                self.assertIn(w, fw.WORD_LISTS[c.lower()]["list"])
            self.assertEqual(len(s), len(command))

        _check("c")
        _check("o")
        _check("p")
        _check("t")
        _check("copt")
        _check("C")
        _check("O")
        _check("P")
        _check("T")
        _check("COPT")

    def test_inputs(self):
        with self.assertRaises(ValueError):
            fw.generate(0)
        with self.assertRaises(TypeError):
            fw.generate(3.14)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            fw.generate(10, separator=1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            fw.generate("a")
        with self.assertRaises(ValueError):
            fw.generate("cccoooppptttz")

    def test_reproducibility(self):
        def _check(seed: int) -> None:
            random.seed(seed)
            a = fw.generate(10)
            random.seed(seed)
            b = fw.generate(10)
            self.assertEqual(a, b)

        _check(0)
        _check(42)
        _check(1337)
