"""Tests for the Docstring class."""

from unittest import TestCase

from darglint.docstring import Docstring
from darglint.lex import lex
from darglint.parse import parse
from darglint.peaker import Peaker


class DocstringMethodTest(TestCase):
    """Tests for the Docstring class."""

    def test_global_noqa_no_body(self):
        """Ensure an empty noqa body means ignore everything."""
        root = parse(Peaker(lex('\n'.join([
            'A short explanation.',
            '',
            '    # noqa',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertTrue(docstring.ignore_all)

    def test_global_noqa_star_body(self):
        """Ensure noqa with * means ignore everything."""
        root = parse(Peaker(lex('\n'.join([
            'A short explanation.',
            '',
            '    # noqa: *',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertTrue(docstring.ignore_all)

    def test_get_short_description(self):
        """Ensure we can get the short description."""
        root = parse(Peaker(lex('Nothing but a short description.'), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.short_description,
            'Nothing but a short description.'
        )

    def test_get_long_description(self):
        """Make sure we can get the long description."""
        root = parse(Peaker(lex('\n'.join([
            'Ignore short.',
            '',
            'Long description should be contiguous.',
            '',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.long_description,
            '\nLong description should be contiguous.\n'
        )

    def test_get_arguments_description(self):
        """Make sure we can get the arguments description."""
        root = parse(Peaker(lex('\n'.join([
            'Something.',
            '',
            'Args:',
            '    x: An integer.',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.arguments_description,
            'Args:\n    x: An integer.\n'
        )

    def test_get_argument_types(self):
        """Make sure we can get a dictionary of arguments to types."""
        root = parse(Peaker(lex('\n'.join([
            'Something.',
            '',
            'Args:',
            '    x (int): The first.',
            '    y (List[int], optional): The second.',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        argtypes = docstring.get_argument_types()
        self.assertEqual(
            argtypes['x'],
            'int',
        )
        self.assertEqual(
            argtypes['y'],
            'List[int], optional',
        )

    def test_get_return_section(self):
        """Make sure we can get the returns description."""
        root = parse(Peaker(lex('\n'.join([
            'Ferment corn.',
            '',
            'Returns:',
            '    Bourbon.',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.returns_description,
            'Returns:\n    Bourbon.\n',
        )

    def test_get_return_type(self):
        """Make sure we can get the return type described."""
        root = parse(Peaker(lex('\n'.join([
            'Ferment potato.',
            '',
            'Returns:',
            '    Alcohol: Vodka.',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.get_return_type(),
            'Alcohol',
        )

    def test_get_yields_description(self):
        """Make sure we can get the yields description."""
        root = parse(Peaker(lex('\n'.join([
            'To pedestrians.',
            '',
            'Yields:',
            '    To pedestrians.',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.yields_description,
            'Yields:\n    To pedestrians.\n',
        )

    def test_get_yields_type(self):
        """Make sure we can get the yields type."""
        root = parse(Peaker(lex('\n'.join([
            'Get slavic cats.',
            '',
            'Yields:',
            '    Cat: The slavic ones.',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.get_yield_type(),
            'Cat',
        )

    def test_get_raises_description(self):
        """Make sure we can get the raises description."""
        root = parse(Peaker(lex('\n'.join([
            'Check if there\'s a problem.',
            '',
            'Raises:',
            '    ProblemException: if there is a problem.',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.raises_description,
            'Raises:\n    ProblemException: if there is a problem.\n'
        )

    def test_get_exception_types(self):
        """Make sure we can get the types of exceptions raised."""
        root = parse(Peaker(lex('\n'.join([
            'Problematic.',
            '',
            'Raises:',
            '    IndexError: Frequently.',
            '    DoesNotExist: Always.',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.get_exception_types(),
            ['IndexError', 'DoesNotExist']
        )

    def test_get_noqas(self):
        """Make sure we can get all of the noqas in the docstring."""
        root = parse(Peaker(lex('\n'.join([
            'Full of noqas.',
            '',
            '# noqa: I200',
            '# noqa: I201 y',
            '',
            'Args:',
            '    x: Something. # noqa: I201',
            '\n',
        ])), lookahead=3))
        docstring = Docstring(root)
        self.assertEqual(
            docstring.get_noqas(),
            {
                'I200': [],
                'I201': ['x', 'y'],
            },
        )
