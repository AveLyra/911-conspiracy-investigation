import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import followup as f


class FollowupTests(unittest.TestCase):
    def test_density_categories(self):
        cases = {'': 'blank', '  ': 'blank', '1': 'numeric_literal', '-.1D+2': 'numeric_literal',
                 'private_name': 'identifier', '1/0': 'numeric_arithmetic',
                 '1/(2**3)': 'numeric_arithmetic', '(1)': 'numeric_arithmetic',
                 '1 + -2': 'numeric_arithmetic', 'private_name/2': 'identifier_arithmetic',
                 '(private_name)': 'identifier_arithmetic', 'x**y': 'identifier_arithmetic',
                 '"private"': 'quote_bearing', "'private": 'quote_bearing',
                 'x' * 257: 'over_cap'}
        for text, expected in cases.items():
            with self.subTest(expected=expected):
                self.assertEqual(f.density_shape(text), expected)

    def test_unsupported(self):
        for text in ['()', '1+', '*1', '(1', '1)', '1(2)', 'func(1)', 'a[1]', '%a%',
                     '1,2', '1<2', '1=2', '1 2', '1x', '1***2', 'π', '１', '1\u00a0+2',
                     'a' * 33, '1' * 65, '(' * 17 + '1' + ')' * 17, '+' * 128 + '1']:
            with self.subTest(length=len(text)):
                self.assertEqual(f.density_shape(text), 'unsupported')

    def test_boundaries(self):
        self.assertEqual(f.density_shape('+' * 127 + '1'), 'numeric_arithmetic')
        self.assertEqual(f.density_shape('(' * 16 + '1' + ')' * 16), 'numeric_arithmetic')
        self.assertEqual(f.density_shape('1' * 64), 'numeric_literal')
        self.assertEqual(f.density_shape('a' * 32), 'identifier')
        self.assertEqual(f.density_shape('1' + ' ' * 254 + '+'), 'unsupported')

    def test_element_recognition(self):
        names = {'SOLID70', 'SHELL181', 'SOLID226'}
        for name in names:
            self.assertEqual(f.element_shape(' ' + name.lower() + ' ', names), {'classification': 'official_name_match', 'name': name})
        for text in ['PRIVATE999', '181', "'SHELL181'", 'SHELL181+1', 'ＳHELL181', 'SHELL 181']:
            self.assertEqual(f.element_shape(text, names), {'classification': 'unresolved'})

    def fixture(self, source, command='MP'):
        prior = f.prior_module()
        lexer = prior.load_lexer()
        segment = lexer.split_line(source)[0][0].strip()
        fields = prior.comma_fields(segment)[0]
        index = 3 if command == 'MP' else 2
        target = {'line': 1, 'segment': 1, 'command': command, 'argument_count': len(fields)-1,
                  'local_or_material_id': '1', 'field_index': index, 'role': 'C0' if command == 'MP' else 'ENAME',
                  'segment_sha256': f.sha(segment.encode('latin1')),
                  'field_sha256': f.sha(fields[index].strip().encode('utf8'))}
        return prior, lexer, target

    def test_fixed_field_and_privacy(self):
        source = 'MP,DENS,1,private_sentinel/2 ! private_comment\nUNRELATED,PRIVATE'
        prior, lexer, target = self.fixture(source.split('\n')[0])
        rows = f.extract(source.encode(), [target], {'SHELL181'}, prior, lexer)
        serialized = json.dumps(rows)
        self.assertNotIn('private', serialized.lower())
        self.assertEqual(rows[0]['classification'], 'identifier_arithmetic')

    def test_quotes_and_dollar(self):
        source = 'MP,DENS,1,"secret,with$delimiter!" $ ET,2,SHELL181 !comment'
        prior, lexer, target = self.fixture(source)
        rows = f.extract(source.encode(), [target], {'SHELL181'}, prior, lexer)
        self.assertEqual(rows[0]['classification'], 'quote_bearing')
        self.assertNotIn('secret', json.dumps(rows))

    def test_field_and_segment_pins(self):
        source = 'ET,1,SHELL181'
        prior, lexer, target = self.fixture(source, 'ET')
        self.assertEqual(f.extract(source.encode(), [target], {'SHELL181'}, prior, lexer)[0]['name'], 'SHELL181')
        for key in ('field_sha256', 'segment_sha256'):
            bad = {**target, key: '0' * 64}
            with self.assertRaises(f.Refused):
                f.extract(source.encode(), [bad], {'SHELL181'}, prior, lexer)

    def test_field_guards(self):
        source = 'MP,DENS,1,1/2'
        prior, lexer, target = self.fixture(source)
        for key, value in [('argument_count', 2), ('local_or_material_id', '2'), ('field_index', 2), ('role', 'ENAME'), ('line', 2)]:
            with self.assertRaises(f.Refused):
                f.extract(source.encode(), [{**target, key: value}], set(), prior, lexer)
        with self.assertRaises(f.Refused):
            f.extract(b'\0', [target], set(), prior, lexer)

    def test_cli_privacy(self):
        result = subprocess.run([sys.executable, '-B', str(Path(f.__file__)), 'PRIVATE_SENTINEL'], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('PRIVATE_SENTINEL', result.stdout + result.stderr)
        self.assertEqual(result.stderr, '')

    def test_unselected_line_cap(self):
        source = 'MP,DENS,1,1/2'
        prior, lexer, target = self.fixture(source)
        with self.assertRaises(f.Refused) as failure:
            f.extract(source.encode() + b'\n' + b'x' * prior.LINE_CAP, [target], set(), prior, lexer)
        self.assertEqual(failure.exception.code, 'line_cap')

    def test_output_and_control_guards(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(f, 'HERE', Path(temporary)):
            with self.assertRaises(f.Refused):
                f.output_path('../private.json')
            path = f.output_path('followup-producer-run01.json')
            path.touch()
            with self.assertRaises(f.Refused):
                f.output_path(path.name)
            with self.assertRaises(f.Refused):
                f.pinned(path.name, '0' * 64)
            link = Path(temporary) / 'link'
            link.symlink_to(path)
            with self.assertRaises(f.Refused):
                f.pinned('link', f.sha(b''))


if __name__ == '__main__':
    unittest.main()
