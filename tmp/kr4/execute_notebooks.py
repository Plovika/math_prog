"""Execute each notebook code cell in isolation and save real Jupyter outputs."""
from pathlib import Path
import base64
import contextlib
import io
import json
import os
import traceback
os.environ['MPLBACKEND']='Agg'
os.environ['MPLCONFIGDIR']=str(Path(__file__).parent/'mplconfig')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[2]
summaries=[]
for n in range(1,18):
    path=root/'kr4'/f'kr4_task{n}.ipynb'
    nb=json.loads(path.read_text(encoding='utf-8'))
    cell=nb['cells'][1]
    outputs=[]
    stream=io.StringIO()
    def flush_text():
        value=stream.getvalue()
        if value:
            outputs.append({'output_type':'stream','name':'stdout','text':value.splitlines(True)})
            stream.seek(0);stream.truncate(0)
    def show():
        flush_text()
        for figure_number in plt.get_fignums():
            fig=plt.figure(figure_number)
            image=io.BytesIO()
            fig.savefig(image,format='png',dpi=110)
            outputs.append({'output_type':'display_data','metadata':{},'data':{
                'image/png':base64.b64encode(image.getvalue()).decode(),
                'text/plain':['<Figure with probability simulation>']}})
        plt.close('all')
    plt.show=show
    try:
        with contextlib.redirect_stdout(stream):
            exec(compile(''.join(cell['source']),str(path),'exec'),{'__name__':'__main__'})
        flush_text()
        cell['execution_count']=1
        cell['outputs']=outputs
        path.write_text(json.dumps(nb,ensure_ascii=False,indent=1),encoding='utf-8')
        texts=''.join(''.join(x['text']) for x in outputs if x['output_type']=='stream')
        summaries.append(f'===== 4.{n} =====\n'+texts)
        print(f'4.{n}: OK; figures={sum(x["output_type"]=="display_data" for x in outputs)}',flush=True)
    except Exception:
        traceback.print_exc()
        raise
(root/'tmp'/'kr4'/'execution_results.txt').write_text('\n'.join(summaries),encoding='utf-8')
