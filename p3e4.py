import networkx as nx
from networkx.algorithms import dijkstra_path
import matplotlib.pyplot as plt

def graficar(G, path):
    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_edge_attributes(G, 'label')
    flujo = nx.get_edge_attributes(G, 'flujo')
    costo = nx.get_edge_attributes(G, 'costo')
    
    plt.figure(1)
    ax = plt.subplot(111)
    nx.draw(G, pos=pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title(f'GRAFO')
    plt.savefig('grafo',bbox_inches='tight')
    
    plt.figure(2)
    ax = plt.subplot(111)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=flujo)
    plt.title(f'FLUJO')
    plt.savefig('flujo',bbox_inches='tight')
    
    plt.figure(3)
    ax = plt.subplot(111)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=costo)
    plt.title(f'COSTO\nAndate por {path}')
    plt.savefig('costo',bbox_inches='tight')

    plt.show()

def main():
    f1 = lambda f: 10.+f/120. # arcos r, v, z
    f2 = lambda f: 14.+f/80.  # arcos s, u, w, y
    f3 = lambda f: 10.+f/240. # arcos t, x

    OD = {('A', 'C'): 1100.,
          ('A', 'D'): 1110.,
          ('A', 'E'): 1020.,
          ('B', 'C'): 1140.,
          ('B', 'D'): 1160.,
          ('C', 'E'): 1170.,
          ('C', 'G'): 1180.,
          ('D', 'C'): 0350.,
          ('D', 'E'): 1190.,
          ('D', 'G'): 1200.}
    OD_target = OD.copy()

    G = nx.DiGraph()

    G.add_node('A', pos=[-2,1])
    G.add_node('B', pos=[-2,0])
    G.add_node('C', pos=[0, 0])
    G.add_node('D', pos=[0,-1])
    G.add_node('E', pos=[2, 1])
    G.add_node('G', pos=[2, 0])

    G.add_edge('A', 'B', fcosto=f1, flujo=0., costo=10., label='r: 10 + f/120')
    G.add_edge('A', 'C', fcosto=f2, flujo=0., costo=14., label='s: 14 + 3f/240')
    G.add_edge('B', 'C', fcosto=f3, flujo=0., costo=10., label='t: 10 + f/240')
    G.add_edge('B', 'D', fcosto=f2, flujo=0., costo=14., label='u: 14 + 3f/240')
    G.add_edge('C', 'E', fcosto=f2, flujo=0., costo=14., label='w: 14 + 3f/240')
    G.add_edge('C', 'G', fcosto=f3, flujo=0., costo=10., label='x: 10 + f/240')
    G.add_edge('D', 'C', fcosto=f1, flujo=0., costo=10., label='v: 10 + f/120')
    G.add_edge('D', 'G', fcosto=f2, flujo=0., costo=14., label='y: 14 + 3f/240')
    G.add_edge('G', 'E', fcosto=f1, flujo=0., costo=10., label='z: 10 + f/120')
    
    incrementos = [0.1]*9 + [0.01]*9 + [0.001]*9 + [0.0001]*9 + [0.00001]*9 + [0.000001]*9 + [0.0000001]*9 + [0.00000001]*10
    for incremento in incrementos:
        for key in OD:
            origen, destino = key[0], key[1]
            demanda_actual, demanda_objetivo = OD[key], OD_target[key]
            if demanda_actual > 0.:
                path = dijkstra_path(G,origen,destino,weight='costo')
                Nparadas = len(path)
                for i in range(Nparadas-1):
                    o, d = path[i], path[i+1]
                    G.edges[o,d]['flujo'] += incremento*demanda_objetivo
                    G.edges[o,d]['costo'] = G.edges[o,d]['fcosto'](G.edges[o,d]['flujo'])
                OD[key] -= incremento*demanda_objetivo
                
    for key, value in G.edges.items():
        G.edges[key]['flujo'] = round(G.edges[key]['flujo'],4)
        G.edges[key]['costo'] = round(G.edges[key]['costo'],4)
    
    graficar(G, path)

if __name__ == '__main__':
    main()