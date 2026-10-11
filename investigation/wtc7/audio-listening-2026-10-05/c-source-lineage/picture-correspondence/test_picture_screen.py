"""Synthetic adapter controls; no historical frame reads or scoring."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image

ADAPTER = None
CORE = None


class AdapterControls(unittest.TestCase):
    def setUp(self):
        self.a=ADAPTER; self.core=CORE
        self.rng=np.random.default_rng(7102027)

    def test_canvas_extremes_and_offsets(self):
        image=np.arange(120*180,dtype=np.uint16).reshape(120,180)%256
        for scale,shape,origin in [(.75,(135,90),(47,40)),(1.,(180,120),(25,25)),(1.75,(315,210),(-43,-20))]:
            a,v,t=self.a.canvas(image,scale)
            self.assertEqual((t['raster_width'],t['raster_height']),shape)
            self.assertEqual((t['canvas_x'],t['canvas_y']),origin)
            full=np.asarray(Image.fromarray(image.astype(np.uint8)).resize(shape,Image.Resampling.BILINEAR))
            for y,x in [(0,0),(0,229),(169,0),(169,229),(85,115)]:
                sx,sy=x-origin[0],y-origin[1]; inside=0<=sx<shape[0] and 0<=sy<shape[1]
                self.assertEqual(bool(v[y,x]),inside)
                self.assertEqual(a[y,x],full[sy,sx] if inside else 0)
            self.assertEqual(a.shape,(170,230))

    def test_native_masks_and_invalid_geometry(self):
        arm={'crop':[100,0,1180,720],'static':[[100,0,640,360]],'dynamic':[[640,360,1180,720]]}
        s,d=self.a.masks(arm)
        self.assertEqual(int(s.sum()),90*60); self.assertEqual(int(d.sum()),90*60)
        self.assertFalse((s&d).any())
        bad=copy.deepcopy(arm);bad['dynamic']=bad['static']
        with self.assertRaises(ValueError): self.a.masks(bad)
        bad=copy.deepcopy(arm);bad['static']=[[0,0,640,360]]
        with self.assertRaises(ValueError): self.a.masks(bad)
        with self.assertRaises(ValueError): self.a.geometry([False,0,4,4],(5,5))
        with self.assertRaises(ValueError): self.a.canvas(np.ones((119,180)),1.)

    def test_direct_oracle_and_padding(self):
        im=self.rng.integers(0,255,(120,180)).astype(float)
        target=self.rng.integers(0,255,(120,180)).astype(float); mask=np.ones_like(target,bool)
        for scale in [.75,1.,1.75]:
            a,v,_=self.a.canvas(im,scale); scores,cover=self.core.pearson_surface(a,target,mask,v)
            for y,x in [(0,0),(25,25),(50,50)]:
                good=mask&v[y:y+120,x:x+180];frac=good.sum()/mask.sum()
                self.assertAlmostEqual(cover[y,x],frac,places=10)
                if frac<.85: self.assertTrue(np.isnan(scores[y,x]))
                else:
                    aa=a[y:y+120,x:x+180][good];bb=target[good];aa=aa-aa.mean();bb=bb-bb.mean()
                    direct=np.dot(aa,bb)/np.sqrt(np.dot(aa,aa)*np.dot(bb,bb))
                    self.assertAlmostEqual(scores[y,x],direct,places=10)
            a[~v]=123456 # invalid padding never becomes evidence
            again,_=self.core.pearson_surface(a,target,mask,v)
            np.testing.assert_allclose(again,scores,atol=1e-10,equal_nan=True)

    def test_dynamic_change_and_flat(self):
        im=self.rng.integers(0,255,(120,180)).astype(float)
        s=np.zeros_like(im,bool);s[:60]=True;d=~s
        changed=im.copy();changed[d]=255-im[d]
        best,ss,cc=self.a.register(self.core,im,changed,s,d,[1.])
        self.assertEqual((best[0]['left'],best[0]['top']),(25,25))
        self.assertGreater(best[0]['static_score'],1-1e-10)
        self.assertLess(best[0]['dynamic']['score'],-1+1e-10)
        self.assertEqual(ss.shape,(1,51,51))
        self.assertEqual(self.a.register(self.core,np.zeros_like(im),im,s,d,[1.])[0],[])
        self.assertEqual(self.a.dynamic_score(self.core,im,im,d,np.zeros_like(d))['missing_reason'],'coverage')

    def test_rank_ties_reordering_missing(self):
        rows=[{'source_index':i,'transforms':[{'static_score':.8,'dynamic':{'score':None if i==3 else .7}}]} for i in [3,2,1]]
        one=self.a.rank(rows);two=self.a.rank(rows[::-1]);self.assertEqual(one,two)
        self.assertEqual(one['static']['top_two'],[1,2]);self.assertEqual(one['static']['near_best']['0.005'],[1,2,3])
        self.assertEqual(self.a.rank([{'source_index':1,'transforms':[]}])['shortlist_union'],[])

    def test_map_missing_duplicates_and_pts(self):
        rows=[{'source_index':i,'png':f'{i}.png','source_pts':i,'source_time_base':'1/30','source_seconds_exact':str(i)+'/30'} for i in [1,2]]
        self.assertEqual([r['source_index'] for r in self.a.select_rows(rows,[2,1])],[2,1])
        for rr,ii in [(rows,[3]),(rows+rows,[1])]:
            with self.assertRaises(ValueError): self.a.select_rows(rr,ii)
        bad=copy.deepcopy(rows);bad[0]['source_seconds_exact']='3'
        with self.assertRaises(ValueError): self.a.select_rows(bad,[1])
        bad=copy.deepcopy(rows);bad[0]['png']='../out.png'
        with self.assertRaises(ValueError): self.a.select_rows(bad,[1])
        self.assertEqual((30000*34+1000)//1001,1019)

    def test_changing_image_sequence_and_reordered_references(self):
        # Shared synthetic static scene cannot establish chronological identity.
        base=self.rng.integers(20,230,(120,180)).astype(float)
        static=np.zeros_like(base,bool);static[:50]=True
        dynamic=np.zeros_like(base,bool);dynamic[80:]=True
        images=[]
        for _ in range(3):
            image=base.copy()
            image[dynamic]=self.rng.integers(20,230,int(dynamic.sum()))
            images.append(image)
        recovered=[]; static_leaders=[]; dynamic_matrices=[]
        for reference_order in ([0,1,2],[2,0,1]):
            chosen=[]; leaders=[]; matrix=[]
            for ri in reference_order:
                rows=[]
                for index,image in enumerate(images):
                    transforms,_,_=self.a.register(self.core,image,images[ri],static,dynamic,[1.])
                    self.assertEqual((transforms[0]['left'],transforms[0]['top']),(25,25))
                    self.assertGreater(transforms[0]['static_score'],1-1e-10)
                    rows.append({'source_index':index,'transforms':transforms})
                ranking=self.a.rank(rows)
                self.assertEqual(set(ranking['static']['near_best']['0.005']),{0,1,2})
                scores=[r['transforms'][0]['dynamic']['score'] for r in rows]
                self.assertGreater(scores[ri],1-1e-10)
                self.assertTrue(all(abs(s)<.1 for i,s in enumerate(scores) if i!=ri))
                chosen.append(ranking['dynamic']['ranking'][0]['source_index'])
                leaders.append(ranking['static']['ranking'][0]['source_index']);matrix.append(scores)
            recovered.append(chosen);static_leaders.append(leaders);dynamic_matrices.append(matrix)
            self.assertEqual(chosen,reference_order)
        self.assertEqual(static_leaders[0],static_leaders[1])
        self.assertNotEqual(recovered[0],recovered[1])
        # Retain candidate ordering and all nine dynamic scores per arm in stdout.
        print(json.dumps({'synthetic_sequence':{'reference_orders':[[0,1,2],[2,0,1]],
            'recovered_dynamic_orders':recovered,'static_leaders':static_leaders,
            'dynamic_score_matrices':dynamic_matrices}},sort_keys=True))

    def test_hash_geometry_and_existing_refusal(self):
        with tempfile.TemporaryDirectory(prefix='picture-control-') as d:
            p=Path(d)/'x.png';Image.new('RGB',(9,7),'red').save(p);record=self.a.pin(p)
            self.assertEqual(self.a.checked({'path':str(p),**record}),p)
            with self.assertRaises(ValueError): self.a.checked({'path':str(p),'sha256':'0'*64})
            with self.assertRaises(ValueError): self.a.frame(Path(d)/'map.json',{'png':'x.png',**record},(8,7))
            q=Path(d)/'x.json';self.a.save(q,{'x':1})
            with self.assertRaises(FileExistsError):self.a.save(q,{})
            with self.assertRaises(FileExistsError):Path(d).mkdir(exist_ok=False)

    def test_control_gate_refuses_stale_and_product_change(self):
        with tempfile.TemporaryDirectory(prefix='picture-gate-') as d:
            p=Path(d);frozen={'pins':{'synthetic':'a'}}
            self.a.save(p/'controls.json',{'pass':True,'tests_run':8,'inherited':{'pass':True}})
            rec={'mode':'controls','status':'complete','before':frozen,'after':frozen,'products':{'controls.json':self.a.pin(p/'controls.json')}}
            self.a.save(p/'receipt.json',rec);self.a.gate(p,frozen)
            with self.assertRaises(ValueError):self.a.gate(p,{'other':1})
            # Replacing a synthetic fixture intentionally tests product authentication.
            (p/'controls.json').write_text('{}')
            with self.assertRaises(ValueError):self.a.gate(p,frozen)
