"""Qualification-only correction controls on synthetic inventory objects."""
import copy
from pathlib import Path
import tempfile
import unittest
import extend_v2 as v


def fixture():
    return {'version':1, 'status':'conditional_force56_extension_not_accepted_measurement',
            'inventory':{'pairs':[{'pair':p,'identity_and_topology_limits':'prior '+p,'keep':[False,None,1]}
                                  for p in ('F4','F5','F6')]}, 'readings':[{'rows':['unaltered']}],
            'originals':{'reader':'force56_peer'}}


class Controls(unittest.TestCase):
    def test_only_two_qualifications_appended(self):
        prior=fixture(); saved=copy.deepcopy(prior); result=v.amended(prior)
        self.assertEqual(prior,saved)
        self.assertEqual(result['inventory']['pairs'][0],prior['inventory']['pairs'][0])
        for item in result['inventory']['pairs']:
            if item['pair'] in v.APPEND:
                item['identity_and_topology_limits']=item['identity_and_topology_limits'][:-len(' '+v.APPEND[item['pair']])]
        self.assertTrue(v.helpers().exact(result,prior))

    def test_wrong_version_and_status_rejected(self):
        for field,value in [('version',True),('version',2),('status','accepted')]:
            data=fixture();data[field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):v.amended(data)

    def test_missing_duplicate_and_preapplied_qualifications_rejected(self):
        for mode in ('missing','duplicate','preapplied'):
            data=fixture()
            if mode=='missing':data['inventory']['pairs'].pop()
            elif mode=='duplicate':data['inventory']['pairs'].append(copy.deepcopy(data['inventory']['pairs'][1]))
            else:data['inventory']['pairs'][1]['identity_and_topology_limits']+=' '+v.APPEND['F5']
            with self.subTest(mode=mode),self.assertRaises(ValueError):v.amended(data)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='force56-v2-') as folder:
            path=Path(folder)/'out';e=v.helpers();e.save(path,b'prior')
            with self.assertRaises(FileExistsError):e.save(path,b'altered')
            self.assertEqual(path.read_bytes(),b'prior')


if __name__=='__main__':unittest.main()
