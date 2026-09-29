import importlib.util
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import parse_material as p


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lexer=p.load_lexer()

    def scan(self,s):
        return p.scan(s.encode('latin-1'),self.lexer)

    def test_all_schemas(self):
        data='MP,DENS,1,7.8E3\nMPDATA,EX,1,1,2.0,3.0\nMPTEMP,1,0,100\nTB,PLASTIC,1,2,3,BISO\nTBTEMP,100\nTBDATA,1,2,3\nET,1,70\n'
        r=self.scan(data)
        self.assertEqual(len(r['rows']),7)
        self.assertEqual(r['selected_statuses'],{'literal_fields':7})

    def test_blank_zero_and_padded_absence(self):
        r=self.scan('MPDATA,EX,1,,0,,0\n')['rows'][0]
        f={x['role']:x for x in r['fields']}
        self.assertEqual(f['start']['kind'],'blank')
        self.assertEqual(f['c1']['lexeme'],'0')
        self.assertEqual(f['c2']['kind'],'blank')
        self.assertEqual(f['c3']['lexeme'],'0')
        self.assertEqual(r['argument_count'],6)

    def test_no_defaults(self):
        r=self.scan('MP,C,,100\n')['rows'][0]
        self.assertEqual(r['fields'][1],{'role':'material','kind':'blank'})

    def test_unknown_expression_quoted_and_privacy(self):
        s="MP,PRIVATE_SENTINEL,1,44\nMP,EX,1,PRIVATE_EXPR+1\nMP,'EX',1,2\nET,1,PRIVATE_ELEMENT\n/COM,PRIVATE_COMMENT\n"
        result=self.scan(s)
        self.assertEqual(result['selected_statuses'],{'unresolved_fields':4})
        encoded=json.dumps(result)
        for needle in ('PRIVATE_SENTINEL','PRIVATE_EXPR','PRIVATE_ELEMENT','PRIVATE_COMMENT',"'EX'"):
            self.assertNotIn(needle,encoded)

    def test_unbl(self):
        result=self.scan('MPDATA,UNBL,2,EX,1,1,3\nMPTEMP,UNBL,2,1,20\n')
        self.assertEqual(result['selected_statuses'],{'unresolved_coded_database':2})
        self.assertTrue(all(not r['fields'] for r in result['rows']))

    def test_extra_fields(self):
        result=self.scan('TBTEMP,20,,,\nTBTEMP,20,,999\n')
        self.assertEqual(result['rows'][0]['trailing_extra_blanks'],2)
        self.assertEqual(result['rows'][1]['status'],'extra_nonblank_arguments')
        self.assertFalse(result['rows'][1]['fields'])

    def test_exponents_and_strict_numeric(self):
        for value in ('1','-.2','+2.','1.2d+3','1E-2','0'):
            self.assertEqual(p.scalar(value,'number')['kind'],'number')
        for value in ('nan','Inf','1/2','1_000','１２','1E','--1','1'*65):
            self.assertEqual(p.scalar(value,'number')['kind'],'unresolved')
        self.assertEqual(p.scalar('+1','integer')['kind'],'unresolved')

    def test_comments_and_dollar_commands(self):
        result=self.scan('MP,EX,1,1 $ MP,C,2,3 ! MP,ENTH,2,5\n')
        self.assertEqual([(r['line'],r['segment']) for r in result['rows']],[(1,1),(1,2)])
        self.assertEqual(result['commands'],{'MP':2})

    def test_quotes_and_unclosed(self):
        result=self.scan("MP,EX,1,'a''!$b'\nMP,EX,1,'missing\n")
        self.assertEqual(result['rows'][0]['status'],'unresolved_fields')
        self.assertEqual(result['rows'][1]['status'],'unclosed_quote')
        self.assertEqual(result['lexical_flags'],{'unclosed_quote_lines':1})

    def test_quoted_comma_preserves_field_positions(self):
        for label in ("'PRIVATE,A'", "'PRIVATE''A,B'", '"PRIVATE,A"', '"PRIVATE""A,B"'):
            row=self.scan(f'MP,{label},1,42\n')['rows'][0]
            fields={f['role']:f for f in row['fields']}
            self.assertEqual(row['argument_count'],3)
            self.assertEqual(row['status'],'unresolved_fields')
            self.assertEqual(fields['label']['kind'],'unresolved')
            self.assertEqual(fields['material']['lexeme'],'1')
            self.assertEqual(fields['c0']['lexeme'],'42')
            self.assertEqual(fields['c1']['kind'],'blank')
            self.assertNotIn('PRIVATE',json.dumps(row))

    def test_direct_unclosed_field(self):
        row=p.parse_row('MP',"MP,'PRIVATE,A,1,42",1,1)
        self.assertEqual(row['status'],'unclosed_quote')
        self.assertFalse(row['fields'])

    def test_cli_errors_are_fixed_and_do_not_run(self):
        for args in (['--PRIVATE_SENTINEL'],['--output'],
                     ['--output','producer-run01.json','--PRIVATE_SENTINEL']):
            stdout,stderr=io.StringIO(),io.StringIO()
            with patch('sys.argv',['parse_material',*args]),patch.object(p,'run') as run,redirect_stdout(stdout),redirect_stderr(stderr):
                self.assertEqual(p.main(),2)
            run.assert_not_called()
            self.assertEqual(json.loads(stdout.getvalue()),{'status':'REFUSED','code':'cli_arguments'})
            self.assertEqual(stderr.getvalue(),'')

    def test_formats(self):
        result=self.scan("*VWRITE,1\nMP,EX,1,2\nMP,C,1,3\n*VREAD,1\n")
        self.assertEqual(len(result['rows']),1)
        self.assertEqual(result['line_kinds']['format_records'],1)
        self.assertEqual(result['lexical_flags'],{'missing_format_eof':1})

    def test_full_token_and_whitespace_form(self):
        result=self.scan('MPPRIVATE,EX,1,2\nMP EX,1,2\n')
        self.assertEqual(len(result['rows']),1)
        self.assertEqual(result['rows'][0]['status'],'unsupported_command_form')
        self.assertNotIn('MPPRIVATE',json.dumps(result))

    def test_et_numeric_only(self):
        result=self.scan('ET,2,70\nET,2,SOLID70\n')
        self.assertEqual(result['rows'][0]['fields'][1]['lexeme'],'70')
        self.assertEqual(result['rows'][1]['status'],'unresolved_fields')
        self.assertNotIn('SOLID70',json.dumps(result))

    def test_empty_reset(self):
        result=self.scan('MPTEMP,,,,,,,,\nMPTEMP\nMP\n')
        self.assertEqual(result['rows'][0]['status'],'literal_fields')
        self.assertTrue(all(f['kind']=='blank' for f in result['rows'][0]['fields']))
        self.assertEqual(result['rows'][1]['status'],'literal_fields')
        self.assertEqual(result['rows'][2]['status'],'missing_arguments')

    def test_segment_empty_slots(self):
        result=self.scan('$ MP,EX,1,2 $$ MP,C,1,3\n')
        self.assertEqual([r['segment'] for r in result['rows']],[2,4])

    def test_nonblank_tb_function_stays_unresolved(self):
        r=self.scan('TB,USER,1,2,3,THERM,,PRIVATE_FUNCTION\n')['rows'][0]
        self.assertEqual(r['status'],'unresolved_fields')
        self.assertNotIn('PRIVATE_FUNCTION',json.dumps(r))

    def test_caps_and_nul(self):
        for data in (b'\0',b'a'*(p.CAP+1),b'a'*p.LINE_CAP):
            with self.assertRaises(p.Refused):
                p.scan(data,self.lexer)
        with patch.object(p,'ROW_CAP',1):
            with self.assertRaises(p.Refused):
                self.scan('MP,EX,1,2\nMP,EX,1,3\n')

    def test_output_guards(self):
        for name in ('../producer-run01.json','raw.json','producer-run01.json/../x',''):
            with self.assertRaises(p.Refused):
                p.output_path(name)
        with tempfile.TemporaryDirectory() as td,patch.object(p,'HERE',Path(td)):
            path=p.output_path('producer-run01.json');path.write_text('preserve')
            with self.assertRaises(p.Refused):
                p.output_path('producer-run01.json')
            self.assertEqual(path.read_text(),'preserve')

    def test_lexer_pin_refusal(self):
        with patch.object(p,'LEXER_SHA','0'*64):
            with self.assertRaises(p.Refused):
                p.load_lexer()

    def fixture(self,td,relative='input.apdl',content=b'MP,EX,1,2\n'):
        base=Path(td); target=base/'input.apdl'; target.write_bytes(content)
        manifest=base/'manifest.csv'
        manifest.write_text('extension,filename,relative_path,size_bytes,sha256\n.apdl,input.apdl,'+relative+','+str(len(content))+','+p.sha(content)+'\n.apdl,excluded2,excluded2,0,none\n.apdl,excluded3,excluded3,0,none\n')
        return SimpleNamespace(BASE=base,MANIFEST=manifest,MANIFEST_SHA=p.sha(manifest.read_bytes())),target

    def test_candidate_pin_and_only_one_body(self):
        with tempfile.TemporaryDirectory() as td:
            lex,target=self.fixture(td)
            with patch.object(p,'SOURCE_SHA',p.sha(target.read_bytes())),patch.object(p,'SOURCE_SIZE',target.stat().st_size),patch.object(p,'NAME_SHA',p.sha(b'input.apdl')):
                actual,manifest,data=p.read_candidate(lex)
                self.assertEqual(actual,target)
                self.assertEqual(data,b'MP,EX,1,2\n')
                target.write_bytes(b'MP,EX,1,3\n')
                with self.assertRaises(p.Refused):
                    p.read_candidate(lex)

    def test_candidate_path_refusal(self):
        with tempfile.TemporaryDirectory() as td:
            lex,target=self.fixture(td,relative='../input.apdl')
            with patch.object(p,'SOURCE_SHA',p.sha(target.read_bytes())),patch.object(p,'SOURCE_SIZE',target.stat().st_size),patch.object(p,'NAME_SHA',p.sha(b'input.apdl')):
                with self.assertRaises(p.Refused) as err:
                    p.read_candidate(lex)
                self.assertEqual(err.exception.code,'candidate_path')

    def test_candidate_and_output_symlink_refusal(self):
        with tempfile.TemporaryDirectory() as td:
            lex,target=self.fixture(td)
            contents=target.read_bytes(); saved=Path(td)/'saved'; target.rename(saved)
            target.symlink_to(saved)
            with patch.object(p,'SOURCE_SHA',p.sha(contents)),patch.object(p,'SOURCE_SIZE',len(contents)),patch.object(p,'NAME_SHA',p.sha(b'input.apdl')):
                with self.assertRaises(p.Refused) as err:
                    p.read_candidate(lex)
                self.assertEqual(err.exception.code,'candidate_file_type')
            with patch.object(p,'HERE',Path(td)):
                out=Path(td)/'producer-run01.json'; out.symlink_to(Path(td)/'absent')
                with self.assertRaises(p.Refused):
                    p.output_path(out.name)

    def test_manifest_pin_refusal(self):
        with tempfile.TemporaryDirectory() as td:
            lex,target=self.fixture(td); lex.MANIFEST_SHA='0'*64
            with self.assertRaises(p.Refused) as err:
                p.read_candidate(lex)
            self.assertEqual(err.exception.code,'manifest_pin')


if __name__=='__main__':
    unittest.main()
