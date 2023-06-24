import webbrowser
import os
import http.server
import socketserver
import threading
import networkx as nx
from preprocess import load_individual_dataset, load_high_dimensional_dataset, load_dynamic_dataset, load_tree_graph, load_network_graph
from interact import parallel_coordinates, sunburst
from d3 import stream_graph, small_multiples, tree_radial
from netx import kamada_kawai

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

individual_data = load_individual_dataset("dataset.csv", "individual_dataset.csv")
high_dimensional_data = load_high_dimensional_dataset(individual_data)
critic_count = load_dynamic_dataset(individual_data, "critic_score.csv")
tree_graph = load_tree_graph(individual_data)
G = load_network_graph(individual_data)

kamada_kawai(G)
stream_graph()
small_multiples()
tree_radial()
parallel_coordinates(high_dimensional_data)
sunburst(individual_data)

with open("VisualAnalyticsSystem.html", "w") as f:
    f.write("""
    <!DOCTYPE html>
    <html>
    <body>

    <h2 style="text-align:center;">Interactive VA System</h2>

    <iframe src="streamgraph.html" width="100%" height="700"></iframe>
    <iframe src="kamada_kawai.html" width="49%" height="500"></iframe>
    <iframe src="sunburst.html" width="49%" height="500"></iframe>
    <iframe src="parallel_coordinates.html" width="98%" height="400"></iframe>
    <iframe src="small_multiples.html" width="98%" height="1200"></iframe>
    <iframe src="tree_radial.html" width="98%" height="1200"></iframe>
    </body>
    </html>
    """)

full_filename = os.path.abspath("VisualAnalyticsSystem.html")
thread = threading.Thread(target=start_server)
thread.start()
webbrowser.open(f'http://localhost:{PORT}/VisualAnalyticsSystem.html')
