import io
import struct
import unittest
import hashlib
from collect import prior_payloads
from riff_headers import inventory, timecode, fields, unique_text, video_headers, compare


def chunk(kind, data):
    return kind + struct.pack("<I", len(data)) + data + b"\0" * (len(data) % 2)


def riff(data=b"", kind=b"AVI "):
    return chunk(b"RIFF", kind + data)


class HeaderTests(unittest.TestCase):
    def parse(self, data, **limits):
        return inventory(io.BytesIO(data), len(data), **limits)

    def test_prior_lossless_representations(self):
        rows=[]
        for offset, data, key in ((1,b"text\0","utf8"),(2,b"\xff\0","hex")):
            value=data.decode("utf-8") if key=="utf8" else data.hex()
            rows.append({"offset":offset,"payload":{"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),key:value}})
        self.assertEqual(prior_payloads({"riff":{"records":rows}}),{1:b"text\0".hex(),2:"ff00"})
        rows[0]["payload"]["bytes"]+=1
        with self.assertRaisesRegex(ValueError,"reconstruction"):
            prior_payloads({"riff":{"records":rows}})

    def test_valid_info_padding(self):
        d=riff(chunk(b"LIST", b"INFO"+chunk(b"INAM", b"x")))
        r=self.parse(d)
        self.assertEqual(r["records"][-1]["payload_hex"], "78")
        self.assertEqual(r["metadata_payload_bytes_read"], 1)

    def test_skip_movie(self):
        self.assertEqual(self.parse(riff(chunk(b"LIST", b"movibad!")))["metadata_payload_bytes_read"],0)

    def test_skip_indices_and_junk(self):
        for k in (b"JUNK",b"idx1",b"indx",b"ix00"):
            with self.subTest(k=k):
                self.assertEqual(self.parse(riff(chunk(k,b"data")))["metadata_payload_bytes_read"],0)

    def test_skip_misplaced_essence(self):
        for k in (b"00db",b"01dc",b"02wb",b"0Apc"):
            with self.subTest(k=k):
                r=self.parse(riff(chunk(k,b"data")))
                self.assertEqual(r["metadata_payload_bytes_read"],0)
                self.assertIn("essence",r["records"][-1]["skip_reason"])

    def test_depth_boundary(self):
        data=riff(chunk(b"LIST", b"INFO"+chunk(b"INAM",b"a")))
        self.parse(data,max_depth=2)
        with self.assertRaisesRegex(ValueError,"depth limit"):
            self.parse(data,max_depth=1)

    def test_record_boundary(self):
        data=riff(chunk(b"INAM",b"a"))
        self.parse(data,max_records=2)
        with self.assertRaisesRegex(ValueError,"record limit"):
            self.parse(data,max_records=1)

    def test_payload_boundary_and_no_oversized_read(self):
        data=riff(chunk(b"INAM",b"abcd"))
        self.parse(data,max_payload=4)
        class Guarded(io.BytesIO):
            def read(self, n=-1):
                if self.tell()==20:
                    raise AssertionError("oversized payload read")
                return super().read(n)
        with self.assertRaisesRegex(ValueError,"payload limit"):
            inventory(Guarded(data),len(data),max_payload=3)

    def test_multiple_segments(self):
        self.assertEqual(len(self.parse(riff()+riff(kind=b"AVIX"))["records"]),2)

    def test_truncated_header(self):
        with self.assertRaisesRegex(ValueError,"truncated header"):
            self.parse(riff(b"xx"))

    def test_chunk_outside_parent(self):
        with self.assertRaisesRegex(ValueError,"outside parent"):
            self.parse(riff(b"INAM"+struct.pack("<I",100)))

    def test_short_container_and_wrong_type(self):
        for data in (chunk(b"RIFF",b"x"),riff(kind=b"WAVE"),b"NOT RIFF"):
            with self.subTest(data=data),self.assertRaises(ValueError): self.parse(data)

    def test_short_stream_read(self):
        class Short(io.BytesIO):
            def read(self,n=-1): return super().read(max(0,n-1))
        with self.assertRaisesRegex(ValueError,"short read"):
            inventory(Short(riff()),12)

    def test_fields_keep_tails_and_duplicates(self):
        data=riff(chunk(b"LIST",b"Tdat"+chunk(b"rn_O",b"Tape\0\xff")+chunk(b"rn_O",b"Tape\0")))
        fs=fields(self.parse(data)["records"])
        self.assertEqual(len(fs["rn_O"]),2)
        self.assertEqual(fs["rn_O"][0]["tail_hex"],"ff")
        self.assertIsNone(unique_text(fs["rn_O"]))

    def test_video_header(self):
        data=b"vidsdvsd"+bytes(8)+struct.pack("<IIIII",0,1001,30000,0,25)+bytes(20)
        r=self.parse(riff(chunk(b"LIST",b"hdrl"+chunk(b"LIST",b"strl"+chunk(b"strh",data)))))
        self.assertEqual(video_headers(r["records"])[0]["duration_seconds_rational"],"1001/1200")

    def test_timecodes(self):
        self.assertEqual(timecode("00;01;00;02",True),1800)
        self.assertEqual(timecode("00;10;00;00",True),17982)
        self.assertEqual(timecode("01:00:00:00",True),107892)
        self.assertEqual(timecode("00;03;12;26",False),5786)
        self.assertEqual(timecode("00;03;12;26",True),5780)
        self.assertIsNone(timecode("00;01;00;00",True))
        for value in (None,"00;60;00;00","24;00;00;00","00:00;00:01","00;00;00;30","1;2;3;4","００;００;００;００"):
            self.assertIsNone(timecode(value))

    def test_independent_lanes_and_gaps(self):
        def item(clip,tc,alt=None):
            fs={k:[{"prefix_utf8":v}] for k,v in {"rn_O":"T","rn_A":"T","tc_O":tc,"tc_A":alt or tc}.items()}
            return {"clip":clip,"fields":fs,"video_header":{"length":30}}
        items=[item(2,"00;00;02;00"),item(1,"00;00;00;00"),item(3,"00;00;03;00","00;00;04;00")]
        r=compare(items,False,"O")
        self.assertEqual(r["groups"][0]["sorted_clips"],[1,2,3])
        self.assertEqual(r["groups"][0]["adjacent"][0]["conditional_gap_frames"],30)
        self.assertEqual(r["groups"][0]["adjacent"][1]["conditional_gap_frames"],0)
        self.assertEqual(r["unavailable"],[])
        alt=compare(items,False,"A")
        self.assertEqual(alt["groups"][0]["adjacent"][1]["conditional_gap_frames"],30)

    def test_missing_duplicate_ties_and_overlap(self):
        fs={k:[{"prefix_utf8":v}] for k,v in {"rn_O":"T","rn_A":"T","tc_O":"00;00;00;00","tc_A":"00;00;00;00"}.items()}
        items=[{"clip":n,"fields":dict(fs),"video_header":{"length":30}} for n in (1,2,3,4)]
        items[2]["fields"]["tc_O"]=[]
        items[3]["fields"]["rn_O"]=fs["rn_O"]*2
        r=compare(items,False,"O")
        edge=r["groups"][0]["adjacent"][0]
        self.assertTrue(edge["equal_start"])
        self.assertEqual(edge["conditional_gap_frames"],-30)
        self.assertEqual([x["clip"] for x in r["unavailable"]],[3,4])
        self.assertEqual(compare(items,False,"A")["unavailable"],[])
        with self.assertRaisesRegex(ValueError,"unknown"):
            compare(items,False,"X")


if __name__ == "__main__":
    unittest.main(verbosity=2)
