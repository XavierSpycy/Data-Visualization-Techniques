import matplotlib.pyplot as plt
import networkx as nx
import base64
from io import BytesIO

def kamada_kawai(G, scale_factor=3):
    plt.figure(figsize=(7,6))
    pos = nx.kamada_kawai_layout(G)
    deg = nx.degree(G)
    sizes = [scale_factor * deg[n] for n in G.nodes()]
    nx.draw_networkx(G, pos=pos, node_size=sizes, with_labels=False, node_color='lime')
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    plt.close()
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<h2>Kamada-Kawai Layout</h2><img src=\'data:image/png;base64,{}\'>'.format(encoded)
    with open('kamada_kawai.html', 'w') as f:
        f.write(html)