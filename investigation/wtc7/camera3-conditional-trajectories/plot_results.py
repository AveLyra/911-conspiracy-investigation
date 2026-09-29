#!/usr/bin/env python3
"""Static scientific figures of all declared nominal-clock windows, no new fits."""
import hashlib
import json
import os
from pathlib import Path
import tempfile

HERE=Path(__file__).resolve().parent


def pin(path):
    b=path.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}


def main():
    out=HERE/'figure01'
    if out.exists(): raise ValueError('output_exists')
    inputs={'fits':HERE/'fit01/fits.json','trajectories':HERE/'fit01/trajectories.json',
            'clock':HERE/'fit01/clocks.json','receipt':HERE/'fit01/receipt.json',
            'producer':Path(__file__)}
    before={k:pin(v) for k,v in inputs.items()}
    receipt=json.loads(inputs['receipt'].read_text())
    for key,name in [('fits','fits.json'),('trajectories','trajectories.json'),('clock','clocks.json')]:
        assert before[key]==receipt['products'][name]
    fits=json.loads(inputs['fits'].read_text())
    trajectories=json.loads(inputs['trajectories'].read_text())
    from fractions import Fraction
    times=[float(Fraction(t)) for t in json.loads(inputs['clock'].read_text())['nominal']]
    with tempfile.TemporaryDirectory(prefix='wtc7-mpl-') as cache:
        os.environ['MPLCONFIGDIR']=cache
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,axes=plt.subplots(3,1,figsize=(10,9),sharex=True,layout='constrained')
        series=[]
        for track,color in zip(trajectories,['#17648c','#986523']):
            geom=next(g for g in track['geometry_scenarios'] if g['angle']=='saved' and g['intervals']==15)
            vals=[v[1] for v in geom['displacement_X_D_assigned_m']]
            axes[0].plot(times,vals,'.-',markersize=3,linewidth=1,color=color,label=track['track'])
            series.append({'panel':0,'track':track['track'],'time':times,'value':vals})
        axes[0].set_ylabel('Assigned downward displacement (m)')
        axes[0].set_title('Saved points: nominal clock, saved angle, assigned 15-interval scale',fontsize=11)
        axes[0].legend(loc='upper left',frameon=False,ncol=2)
        palette=['#b6b6b6','#2488a3','#95599e','#222222']
        for panel,track in enumerate(['track01','track02'],1):
            ax=axes[panel]
            for length,color in zip([5,9,13,21],palette):
                selected=[r for r in fits if r['track']==track and r['clock']=='nominal' and r['count']==length and r['status']=='pass']
                x=[r['fits']['2']['center_seconds'] for r in selected]
                y=[next(g['acceleration_X_D_assigned_m_per_s2'][1] for g in r['geometry_scenarios'] if g['angle']=='saved' and g['intervals']==15) for r in selected]
                ax.plot(x,y,color=color,linewidth=1.2,label=f'{length} points / {(length-1)*.2:g} s')
                series.append({'panel':panel,'track':track,'window_points':length,'time':x,'value':y})
            ax.axhline(9.80665,color='#b44c3f',linestyle='--',linewidth=1,label='9.80665 reference')
            ax.axhline(0,color='#777777',linewidth=.5)
            ax.set_ylabel(f'{track}: window acceleration\n(assigned m/s²)')
            ax.legend(loc='upper left',frameon=False,ncol=3,fontsize=8)
        for ax in axes:
            ax.spines[['top','right']].set_visible(False)
            ax.grid(axis='y',alpha=.18)
            ax.set_xlim(0,14)
        axes[-1].set_xlabel('Nominal saved-analysis seconds; zero is not identified collapse onset')
        fig.suptitle('Conditional trajectories and fitting-window sensitivity',fontsize=14)
        out.mkdir()
        figure=out/'trajectories-and-window-sensitivity.png'
        fig.savefig(figure,dpi=150,metadata={'Software':'matplotlib; static derived scientific figure'})
        plt.close(fig)
        data_path=out/'plotted-series.json'
        data_path.write_text(json.dumps(series,indent=2,sort_keys=True)+'\n')
        after={k:pin(v) for k,v in inputs.items()}
        assert after==before
        result={'status':'pass_generated_not_yet_visually_reviewed','matplotlib':matplotlib.__version__,
                'inputs_before':before,'inputs_after':after,'series_count':len(series),
                'plotted_samples':sum(len(s['time']) for s in series),
                'products':{figure.name:pin(figure),data_path.name:pin(data_path)},
                'limits':'Full-span quadratic omitted from the window plot but retained in fits; no measured error bars or causal inference.'}
        (out/'receipt.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        print(json.dumps({'status':result['status'],'series':len(series),'samples':result['plotted_samples']}))


if __name__=='__main__': main()
