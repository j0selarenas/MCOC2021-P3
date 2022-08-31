import networkx as nx
import numpy as np

zonas_avo = [146,683,666,682,677,287,307,288,291,289,290,304,266,684,599,153,590]

def zone(p1, p2, lista):
    if p1 in zonas_avo:
        if p1 not in lista:
            lista.append(p1)
        if p2 not in lista:
            lista.append(p2)
           
def zoneOD(p1, p2, lista):
    if p1 in zonas_avo:
        if [p1,p2] not in lista:
            lista.append([p1,p2])
        if [p2,p1] not in lista:
            lista.append([p2,p1])
           
OD, zonas, zonas_mayor_flujo, od, viajes = {}, [], [], [], 0
for line in open('mod.csv'):
    sl = line.split(',')
    o, d, demanda = int(sl[0]), int(sl[1]), np.double(sl[2])
    if demanda > 100:
        zone(o, d, zonas), zone(d, o, zonas)
        viajes += demanda
    if demanda > 1000:
        zone(o, d, zonas_mayor_flujo), zone(d, o, zonas_mayor_flujo)
        zoneOD(o, d, od), zoneOD(d, o, od)
    OD[(o,d)] = demanda
    
for zona in zonas_avo:
    if zona not in zonas:
        zonas.append(zona)
    if zona not in zonas_mayor_flujo:
        zonas_mayor_flujo.append(zona)
        
print(f'Hay un total de {len(zonas)} que cumplen con una demanda mayor a 100, estas zonas son:\n{zonas}\n')
print(f'Hay un total de {int(viajes)} viajes por hora para las zonas seleccionadas\n')
print(f'Hay un total de {len(zonas_mayor_flujo)} que cumplen con una demanda mayor a 1000, estas zonas son:\n{zonas_mayor_flujo}\n')
print(f'Hay un total de {len(od)} pares OD, y estas son: {od}')
nx.write_gpickle(zonas, 'zonas.gpickle')
nx.write_gpickle(zonas_mayor_flujo, 'zonas_mayor_flujo.gpickle')