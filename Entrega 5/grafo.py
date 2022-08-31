import networkx as nx
import osmnx as ox

ox.config(use_cache=True, log_console=True)

G = ox.graph_from_bbox(
    north= -33.30,
    south= -33.62,
    east= -70.26,
    west= -70.82,
    network_type= 'drive',
    clean_periphery=True,
    custom_filter='["highway"~"motorway|primary|secondary|tertiary|construction"]'
    )

nx.write_gpickle(G, 'santiago_grueso.gpickle')