import matplotlib.pyplot as plt
from io import BytesIO
from collections import defaultdict
from itertools import cycle

line_stiles = (
    '-',
    '--',
    '-.',
    ':'
)
marker_stiles = (
    'o',
    'v',
    '>'
)

def get_graph(graph_data: dict, title: str):
    x = []
    y = defaultdict(list)
    for date, values in graph_data.items():
        date = date.rsplit('.', 1)[0]
        x.append(date.replace(' ', '\n'))
        for k, v in values['result'].items():
            y[k].append(v)
    fig, ax = plt.subplots(1, figsize=(20, 8))

    lines = cycle(line_stiles)
    markers = cycle(marker_stiles)
    for name, values in y.items():
        ax.plot(x, values, next(lines) + next(markers), label=name, alpha=0.7)
    ax.grid()
    ax.legend(loc='upper left')
    ax.set_title(title)
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)
    return imgdata
