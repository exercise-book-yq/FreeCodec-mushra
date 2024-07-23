from email.mime import base
from jinja2 import FileSystemLoader, Environment
from flask import Flask, render_template
import os
import random
import json

from glob import glob

def get_rows():
    ret=[]
    tgts = glob(f'data/target/*/*.wav')
    random.shuffle(tgts)
    # print(tgts)
    for i, tgt in enumerate(tgts):
        basename = os.path.basename(tgt)[:-4]
        gtype = tgt.split('/')[-2]
        wavs1 = glob(f'data/speex/{gtype}/{basename}.wav')
        wavs2 = glob(f'data/dac-500bps/{gtype}/{basename}.wav')
        wavs3 = glob(f'data/dac-1000bps/{gtype}/{basename}.wav')
        wavs4 = glob(f'data/ours/{gtype}/{basename}.wav')
        wavs5 = glob(f'data/ours-spk_vq/{gtype}/{basename}.wav')
        wavs6 = glob(f'data/ticodec-500bps/{gtype}/{basename}.wav')
        wavs7 = glob(f'data/ticodec-1000bps/{gtype}/{basename}.wav')
       
        ref = glob(f'data/target/{gtype}/{basename}.wav')
        # wavs = wavs1 + wavs2 + wavs3 + wavs4 + wavs5 + wavs6 + wavs7 + wavs8 + wavs9 + ref + wavs10 + wavs11 + wavs12 + wavs13 + wavs14
        wavs =  wavs1  + wavs2 + wavs3 + wavs4 + wavs5 + ref  + wavs6 +  wavs7
        random.shuffle(wavs)
        for j in range(len(wavs)):
            ret.append((f'{i+1}', f'{j+1}', wavs[j], ref[0]))
    # print(ret)
    return ret


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./")
    env = Environment(loader=loader)
    template = env.get_template("base.html.jinja2")

    rows = get_rows()
    rows = json.dumps(rows)

    html = template.render(
        rows=rows,
    )

    print(rows)
    
    with open("mushra.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()