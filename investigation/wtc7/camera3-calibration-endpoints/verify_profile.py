"""Independent fixed-strip/lag audit using integer/Fraction/Decimal arithmetic.

No producer import, source decode, plotting, historical feature interpretation
or physical-unit fit. Correlation tolerance fixed before reading result values.
"""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
from PIL import Image, __version__ as pillow_version

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
DECLARATION_SHA = '6eaea06dcc96e3d429f1ab845ffe02ffea21329c6845e156ea58c1339760de71'
PRODUCER_SHA = 'b28ace99e0c532937ddfcf247f6724ad9eea8d4533f035fd20b4b43bf4c65ca5'
RESULT_SHA = '6cf5b643c0705f6ca95f2ddf2fb8e61e2eee891afeba806762f15c2b877c645e'
PRIOR_SHA = '8ae034a788f93a8c8c80704c4fe4b675105065be2a28567e9c4c21cf47a83219'
LAGS = tuple(range(8,19))
TOLERANCE = Decimal('1e-12')
TIE = Decimal('1e-12')
VARIANCE_CUTOFF = Q(1,10**20)


def require(value,label):
    if not value:
        raise AssertionError(label)


def identity(path):
    with path.open('rb') as stream:
        return {'bytes':path.stat().st_size,'sha256':hashlib.file_digest(stream,'sha256').hexdigest()}


def read(path):
    def bad(value):raise ValueError('nonfinite JSON value')
    return json.loads(path.read_text(),parse_constant=bad)


def dec(value):
    return Decimal(value.numerator)/Decimal(value.denominator)


def centered(values):
    mean=sum(values)/len(values)
    return [value-mean for value in values]


def independent_correlations(values,detrend):
    values=[Q(value) for value in values]
    if detrend:
        xc=centered([Q(i) for i in range(len(values))])
        yc=centered(values)
        slope=sum(x*y for x,y in zip(xc,yc))/sum(x*x for x in xc)
        values=[y-slope*x for x,y in zip(xc,yc)]
    rows=[]
    with localcontext() as context:
        context.prec=60
        for lag in LAGS:
            a,b=centered(values[:-lag]),centered(values[lag:])
            aa,bb=sum(x*x for x in a),sum(x*x for x in b)
            covariance=sum(x*y for x,y in zip(a,b))
            value=None if min(aa,bb)<=VARIANCE_CUTOFF else dec(covariance)/dec(aa*bb).sqrt()
            rows.append({'lag_pixels':lag,'pairs':len(a),'correlation':value,
                'first_norm':dec(aa).sqrt(),'second_norm':dec(bb).sqrt()})
        valid=[r['correlation'] for r in rows if r['correlation'] is not None]
        best=max(valid) if valid else None
        maxima=[] if best is None else [r['lag_pixels'] for r in rows if r['correlation'] is not None and best-r['correlation']<=TIE]
    return {'linear_detrend':detrend,'correlations':rows,'maximizing_lags':maxima}


def compare_correlations(actual,expected,label):
    require(set(actual)=={'linear_detrend','correlations','maximizing_lags'},label+' exact result fields')
    require(type(actual['linear_detrend']) is bool and actual['linear_detrend']==expected['linear_detrend'],label+' method')
    require(len(actual['correlations'])==11,label+' eleven complete lag rows')
    differences=[]
    for got,wanted in zip(actual['correlations'],expected['correlations']):
        require(set(got)=={'lag_pixels','pairs','correlation'},label+' exact lag fields')
        require(type(got['lag_pixels']) is int and type(got['pairs']) is int and
            (got['lag_pixels'],got['pairs'])==(wanted['lag_pixels'],wanted['pairs']),label+' exact lag/pair count')
        if wanted['correlation'] is None:
            require(got['correlation'] is None,label+' undefined norm preserved')
            difference=None
        else:
            require(type(got['correlation']) is float and math.isfinite(got['correlation']),label+' finite float correlation')
            difference=abs(Decimal.from_float(got['correlation'])-wanted['correlation'])
            require(difference<=TOLERANCE,label+' independent correlation outside fixed tolerance')
        differences.append(dict(wanted,absolute_difference=difference))
    require(actual['maximizing_lags']==expected['maximizing_lags'],label+' exact maximizing lags/ties')
    return {'label':label,'linear_detrend':expected['linear_detrend'],
        'maximizing_lags':expected['maximizing_lags'],'correlations':differences}


def check_controls(actual):
    cases=[]
    for period in (12,13,14):
        values=[Q.from_float(math.cos(2*math.pi*i/period)) for i in range(183)]
        for detrend in (False,True):
            cases.append(('cosine',period,values,detrend))
    cases.extend([('constant_raw',None,[Q(1)]*183,False),
        ('constant_detrended',None,[Q(1)]*183,True),
        ('affine_ramp_detrended',None,[Q(2*i+10) for i in range(183)],True)])
    require(len(actual)==len(cases)==9,'nine exact synthetic control cases')
    records=[]
    for got,(kind,period,values,detrend) in zip(actual,cases):
        fields={'kind','result'}|({'period'} if period else set())
        require(set(got)==fields and got['kind']==kind and (period is None or got['period']==period),'control kind/period fields')
        expected=independent_correlations(values,detrend)
        require(expected['maximizing_lags']==([period] if period else []),'independent known-period or undefined control outcome')
        records.append(compare_correlations(got['result'],expected,f'control/{kind}/{period}/{detrend}'))
    return records


def verify():
    required={'PROFILE-DECLARATION.md':DECLARATION_SHA,'profile_rows.py':PRODUCER_SHA,
        'profile01.json':RESULT_SHA,'run01/receipt.json':PRIOR_SHA}
    require(all(identity(HERE/name)['sha256']==digest for name,digest in required.items()),'fixed declaration/producer/result/source-view identities')
    data=read(HERE/'profile01.json');prior=read(HERE/'run01/receipt.json')
    require(data['script_sha256']==PRODUCER_SHA and data['status']=='pass_image_repetition_diagnostic','producer result identity/status')
    require(data['box']==[402,202,412,385] and data['lags']==list(LAGS),'declared strip and lag grid')
    pin_names={'PROTOCOL.md','PROFILE-DECLARATION.md','prepare.py','run01/receipt.json','root-observations.md','independent-observations.md'}
    require(set(data['pins'])==pin_names,'exact recorded dependency names')
    require(all(identity(HERE/name)['sha256']==digest for name,digest in data['pins'].items()),'current declared dependency bytes')
    paths=[HERE/name for name in set(required)|pin_names]+[Path(__file__),Path(sys.executable)]
    paths.extend(Path(row['native']['path']) for row in prior['selected'])
    before={str(path):identity(path) for path in paths}
    controls=check_controls(data['controls'])
    require([row['index'] for row in prior['selected']]==[138,141,168] and [row['index'] for row in data['results']]==[138,141,168],'exact ordered three-frame coverage')
    records=[]
    for recorded,source in zip(data['results'],prior['selected']):
        path=Path(source['native']['path'])
        require(identity(path)['sha256']==recorded['native_sha256']==source['native']['sha256'],'native image byte lineage')
        with Image.open(path) as image:
            require((image.format,image.mode,image.size)==('PNG','L',(720,480)),'native PNG geometry/mode')
            pixels=image.tobytes()
        require(hashlib.sha256(pixels).hexdigest()==source['pixel_sha256'],'selected native grayscale hash')
        sums=[sum(pixels[y*720+402:y*720+412]) for y in range(202,385)]
        means=[Q(value,10) for value in sums]
        require(recorded['row_integer_sums']==sums and len(sums)==183,'all 183 exact ten-column integer row sums')
        require(all(type(value) is int for value in recorded['row_integer_sums']),'integer sums retain integer type')
        require(recorded['row_means']==[float(value) for value in means] and all(type(value) is float for value in recorded['row_means']),'all 183 correctly rounded arithmetic means')
        cases=[(name,lo,hi,detrend) for name,lo,hi in [('full',0,183),('upper',0,91),('lower',91,183)] for detrend in (False,True)]
        require(len(recorded['windows'])==6,'six method/window pairs per frame')
        windows=[]
        for got,(name,lo,hi,detrend) in zip(recorded['windows'],cases):
            require(set(got)=={'name','y_start','y_stop','result'} and
                (got['name'],got['y_start'],got['y_stop'])==(name,202+lo,202+hi),'exact declared window membership')
            expected=independent_correlations(means[lo:hi],detrend)
            windows.append(compare_correlations(got['result'],expected,f'frame/{recorded["index"]}/{name}/{detrend}'))
        records.append({'index':recorded['index'],'native_sha256':recorded['native_sha256'],
            'integer_sums_verified':183,'means_verified':183,'windows':windows})
    require(all(identity(Path(path))==value for path,value in before.items()),'consumed native/declaration/code/result/observation pins unchanged after review')
    historical=[lag for record in records for window in record['windows'] for lag in window['correlations']]
    synthetic=[lag for control in controls for lag in control['correlations']]
    require(len(historical)==198 and len(synthetic)==99,'198 historical and99 synthetic correlation cells')
    numeric=[row for row in historical+synthetic if row['absolute_difference'] is not None]
    valid_norms=[norm for row in historical for norm in (row['first_norm'],row['second_norm']) if row['correlation'] is not None]
    return {'input_pins':before,'controls':controls,'profiles':records,
        'coverage':{'native_images':3,'integer_sums':549,'row_means':549,'historical_correlation_cells':198,'historical_method_window_results':18,'synthetic_control_cases':9,'synthetic_correlation_cells':99},
        'max_absolute_correlation_difference':max(row['absolute_difference'] for row in numeric),
        'minimum_historical_admitted_overlap_norm':min(valid_norms),
        'correlation_absolute_tolerance':TOLERANCE,'maxima_tie_tolerance':TIE,
        'norm_cutoff':'1e-10 intensity units, checked through exact variance cutoff1e-20',
        'scope':'Pixel-profile arithmetic only; no independent floor count, physical scale, exposure time, acceleration or cause.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True)
    args=parser.parse_args();output=HERE/args.out
    require(output.parent==HERE and output.name.startswith('independent-profile') and output.suffix=='.json' and not output.exists(),'new scoped review receipt')
    result={'verifier':identity(Path(__file__)),'command':sys.argv,'python':platform.python_version(),'pillow':pillow_version,
        'independent_method':'Integer byte-row sums; exact Fraction closed-form OLS and centered covariance/variance;60-digit Decimal normalization; independent math.cos controls; no producer import.'}
    try:
        result['verification']=verify()
        require(identity(Path(__file__))==result['verifier'],'reviewer source unchanged')
        result['status']='pass'
    except Exception as error:
        result.update(status='fail',error_type=type(error).__name__,error=str(error))
    with output.open('x') as stream:
        json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False,default=lambda value:str(value) if isinstance(value,Decimal) else value)
        stream.write('\n')
    print(json.dumps({key:result[key] for key in ('status','error_type','error') if key in result}))
    return 0 if result['status']=='pass' else 1


if __name__=='__main__':raise SystemExit(main())
