"""Synthetic checks; no historical inputs are read here."""
import json
import unittest

from lookup import disposition, matches, properties, selected_fields, unique


def prop(key, value):
    return {'id': key, 'data': [{'value': {'str': value}}]}


def record(folder=None):
    row = {'properties': [prop('mes:key', 'NYC-WTC_000123456'),
                          prop('title', 'NYC-WTC_000123456.pdf'),
                          prop('source', 'WTC 7'), prop('box_name', 'Example')]}
    if folder is not None:
        row['properties'].append(prop('folder_name', folder))
    return row


class LookupTests(unittest.TestCase):
    def test_sheet_forms(self):
        for value in ('S-1', 'S-S-1', 'SKS-S-1', 'SKS-S-2', 's _ s _ 1', 'S–1'):
            with self.subTest(value=value):
                self.assertTrue(any(h['category'] == 'sheet' for h in matches({'folder': value})))

    def test_compound_is_only_token_lead(self):
        for value in ('A-S-1', 'S-1.1', 'S-1-1'):
            with self.subTest(value=value):
                self.assertEqual(disposition('WTC 7', matches({'folder': value})), 'sheet-token lead')

    def test_alphanumeric_boundaries(self):
        for value in ('XS1', 'S-12', 'S1A', 'SKS-S-20', 'S-TS-7'):
            with self.subTest(value=value):
                self.assertFalse(any(h['category'] == 'sheet' for h in matches({'folder': value})))

    def test_first_floor(self):
        for value in ('First Floor', '1st Fl.', 'first-floor'):
            with self.subTest(value=value):
                self.assertTrue(any(h['category'] == 'first_floor' for h in matches({'folder': value})))

    def test_wrong_floor(self):
        self.assertEqual(matches({'folder': '21st floor'}), [])

    def test_subject_context(self):
        self.assertEqual(disposition('WTC 7', matches({'folder': 'First floor beam plan'})), 'subject lead')

    def test_context_only(self):
        self.assertEqual(disposition('WTC 7', matches({'folder': 'Structural services 23rd floor'})), 'context lead')

    def test_off_source(self):
        self.assertEqual(disposition('OTHER', matches({'folder': 'S-1'})), 'off-source')

    def test_field_isolation(self):
        fields = selected_fields({'title': 'NYC-WTC_000123456.pdf', 'query': 'S-1', 'agency': 'first floor'})
        self.assertEqual(matches(fields), [])

    def test_missing_distinct_from_literal(self):
        self.assertNotIn('folder_name', properties(record()))
        self.assertEqual(properties(record('None'))['folder_name'], 'None')

    def test_duplicate_json(self):
        with self.assertRaises(ValueError):
            json.loads('{"a":1,"a":2}', object_pairs_hook=unique)

    def test_duplicate_property(self):
        row = record('A')
        row['properties'].append(prop('folder_name', 'B'))
        with self.assertRaises(ValueError):
            properties(row)

    def test_multivalue(self):
        row = record('A')
        row['properties'][-1]['data'] *= 2
        with self.assertRaises(ValueError):
            properties(row)

    def test_missing_required(self):
        row = record()
        row['properties'] = row['properties'][1:]
        with self.assertRaises(ValueError):
            properties(row)

    def test_key_title_mismatch(self):
        row = record()
        row['properties'][1] = prop('title', 'Other.pdf')
        with self.assertRaises(ValueError):
            properties(row)

    def test_occurrences_not_documents(self):
        hits = matches({'folder': 'S-1 S-1'})
        self.assertEqual(len(hits), 2)
        self.assertEqual(disposition('WTC 7', hits), 'sheet-token lead')


if __name__ == '__main__':
    unittest.main()
