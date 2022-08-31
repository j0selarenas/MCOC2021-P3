import networkx as nx
import matplotlib.pyplot as plt

def tiempo_recorrido(posicion1, posicion2, vel):
    distancia = ((posicion1[0]-posicion2[0])**2+(posicion1[1]-posicion2[1])**2)**0.5
    return(distancia/vel)

def colorPath(G, path):
    colores, edgelist, width = [], [], []
    for ni, nf in G.edges:
        if ni in path and nf in path:
            colores.append('r')
            width.append(3)
        else:
            colores.append('#7C7C7C')
            width.append(1.5)
        edgelist.append((ni,nf))
    return([colores, edgelist,width])

def graficar(G, pos, colores, fig, edgelist, width=None, tiempoRecorrido=None):
    plt.figure()
    ax = plt.axes()
    
    plt.ylabel('Y (km)')
    plt.xlabel('X (km)')
    if tiempoRecorrido != None:
        plt.title(f'Tiempo de recorrido = {int(60*tiempoRecorrido)} min {int(round((60*tiempoRecorrido-int(60*tiempoRecorrido))*60,0))} s')
    
    ax.set_xlim([-0.5,10.5])
    ax.set_ylim([-0.5,10.5])
    ax.set_xticks([0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.])
    ax.set_yticks([0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.])
    ax.set_xticklabels(['0.0','1.0','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0'])
    ax.set_yticklabels(['0.0','1.0','2.0','3.0','4.0','5.0','6.0','7.0','8.0','9.0','10.0'])
    
    nx.draw_networkx_nodes(G, pos=pos)
    nx.draw_networkx_labels(G, pos=pos)
    if width == None:
        nx.draw_networkx_edges(G, pos, edgelist=edgelist, edge_color=colores, width=2.5)
    else:
        nx.draw_networkx_edges(G, pos, edgelist=edgelist, edge_color=colores, width=width)
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    ax.set_axisbelow(True)
    plt.grid('on') 
    plt.savefig(fig,bbox_inches='tight')
    plt.show()

def main():
    #Iniciar grafo
    G = nx.Graph()
    
    #Velocidades en km/hr
    vel_gris, vel_verde, vel_cafe  = 120, 60, 40
    
    #Colores
    gris, verde, cafe  = '#7C7C7C', '#00701A', '#6C4E09'

    #Generando nodos con sus respectivas posiciones
    posiciones = [[1,2],[4,3],[1,6],[7,3],[10,1],[0,10],[4,0],[5,8],[9,7],[8,10]]
    for i in range(len(posiciones)):
        G.add_node(i, pos=posiciones[i])
    
    #Obteniendo un diccionario de los nodos con sus posiciones
    pos = nx.get_node_attributes(G, 'pos') 
    
    #Generando los arcos del grafo
    G.add_edge(0, 1, tiempo=tiempo_recorrido(pos[0], pos[1], vel_cafe), color=cafe)
    G.add_edge(0, 2, tiempo=tiempo_recorrido(pos[0], pos[2], vel_gris), color=gris)
    G.add_edge(0, 6, tiempo=tiempo_recorrido(pos[0], pos[6], vel_gris), color=gris)
    
    G.add_edge(1, 2, tiempo=tiempo_recorrido(pos[1], pos[2], vel_cafe), color=cafe)
    G.add_edge(1, 3, tiempo=tiempo_recorrido(pos[1], pos[3], vel_verde), color=verde)
    G.add_edge(1, 7, tiempo=tiempo_recorrido(pos[1], pos[7], vel_cafe), color=cafe)
    
    G.add_edge(2, 5, tiempo=tiempo_recorrido(pos[2], pos[5], vel_cafe), color=cafe)
    
    G.add_edge(3, 4, tiempo=tiempo_recorrido(pos[3], pos[4], vel_verde), color=verde)
    G.add_edge(3, 6, tiempo=tiempo_recorrido(pos[3], pos[6], vel_cafe), color=cafe)
    G.add_edge(3, 7, tiempo=tiempo_recorrido(pos[3], pos[7], vel_verde), color=verde)
    G.add_edge(3, 8, tiempo=tiempo_recorrido(pos[3], pos[8], vel_cafe), color=cafe)
    
    G.add_edge(4, 6, tiempo=tiempo_recorrido(pos[4], pos[6], vel_gris), color=gris)
    G.add_edge(4, 8, tiempo=tiempo_recorrido(pos[4], pos[8], vel_gris), color=gris)
    
    G.add_edge(5, 7, tiempo=tiempo_recorrido(pos[5], pos[7], vel_gris), color=gris)
    
    G.add_edge(7, 9, tiempo=tiempo_recorrido(pos[7], pos[9], vel_verde), color=verde)
    
    G.add_edge(8, 9, tiempo=tiempo_recorrido(pos[8], pos[9], vel_verde), color=verde)
    
    #Obtener colores de cada arco:
    coloresArcos = nx.get_edge_attributes(G, 'color')
    
    #Obtener datos para trayecto:
    colores, edgelist = [], []
    for i in coloresArcos:
        edgelist.append(i)
        colores.append(coloresArcos[i])
    #Graficar ciudades y caminos:
    graficar(G, pos, colores, 'fig1.png', edgelist)
    
    #Encontrar la trayectoria más rápida para cada trayecto:
    paths   = [nx.dijkstra_path(G, source=0, target=9, weight='tiempo'),
               nx.dijkstra_path(G, source=4, target=5, weight='tiempo'),
               nx.dijkstra_path(G, source=0, target=4, weight='tiempo')]  

    fig = ['fig2.png','fig3.png','fig4.png']
    for i in range(len(paths)):
        #Obtener tiempo de recorrido:
        tiempoRecorrido = 0
        for j in range(len(paths[i])-1):
            parada_i = paths[i][j]
            parada_f = paths[i][j+1]
            tiempoRecorrido_i = G.edges[parada_i, parada_f]['tiempo']
            tiempoRecorrido += tiempoRecorrido_i
        #Obtener datos para trayecto:
        colores, edgelist, width = colorPath(G, paths[i])
        #Graficar:
        graficar(G, pos, colores, fig[i], edgelist, width, tiempoRecorrido)
    
if __name__ == '__main__':
    main()