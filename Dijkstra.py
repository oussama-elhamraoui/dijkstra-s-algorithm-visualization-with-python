import sys
import networkx as nx
import matplotlib.pyplot as plt
from heapq import heappush

def dijkstra(graph, src, dest, G, pos):
    inf = sys.maxsize  
    # On utilise `sys.maxsize` comme une valeur infinie pour initialiser les coûts. Cela garantit qu'aucun nœud n'a initialement de coût inférieur, sauf pour la source.

    node_data = {node: {'cost': inf, 'pred': []} for node in graph}  
    #  Initialisation d'un dictionnaire pour stocker les informations de chaque nœud.  
    # - Chaque nœud est associé à :  
    #   - `cost`: Le coût minimum pour atteindre ce nœud depuis la source. Initialement, c'est "infini".  
    #   - `pred`: Une liste des nœuds précédents permettant de reconstruire le chemin le plus court.  

    node_data[src]['cost'] = 0  
    # Pour le nœud source (`src`), le coût pour y accéder est défini à 0, car il s'agit du point de départ.  

    visited = set()  
    # Ensemble des nœuds déjà visités. Permet d'éviter de revisiter des nœuds et d'améliorer l'efficacité de l'algorithme.  

    temp = src  
    # Variable temporaire qui représente le nœud en cours de traitement. On commence par le nœud source (`src`).  

    shortest_path_edges = []  
    # Liste qui stockera les arêtes composant le chemin le plus court une fois l'algorithme terminé.  


    # Fonction de mise à jour de la visualisation
    def update_visualization(current_node=None, shortest_path_edges=[]):  
        plt.clf()  
        # Efface la figure actuelle pour préparer une nouvelle mise à jour de la visualisation.  

        colors = ['green' if node in visited else 'lightblue' for node in G.nodes()]  
        # Définit les couleurs des nœuds :  
        # - Vert pour les nœuds déjà visités.  
        # - Bleu clair pour les nœuds non visités.  

        nx.draw(G, pos, node_color=colors, with_labels=True, node_size=800, font_size=10)  
        # Dessine le graphe avec les nœuds colorés, leurs étiquettes, et une taille définie.  

        # Dessine le chemin en rouge
        nx.draw_networkx_edges(G, pos, edgelist=shortest_path_edges, edge_color='red', width=2)  
        # Met en évidence les arêtes qui font partie du chemin le plus court en les dessinant en rouge.  

        # Met en surbrillance le nœud actuel en jaune
        if current_node:  
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='yellow')  
            # Colore le nœud en cours de traitement en jaune pour le différencier des autres.  

        edge_labels = nx.get_edge_attributes(G, 'weight')  
        # Récupère les poids des arêtes pour les afficher.  

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  
        # Dessine les étiquettes des poids des arêtes sur le graphe.  

        # Met à jour le graphique
        plt.pause(0.5)  # Ajoute un délai pour visualiser les étapes une par une.  

    while temp != dest:  
        # Boucle principale de l'algorithme : continue jusqu'à ce que le nœud actuel soit la destination.  

        if temp not in visited:  
            # Vérifie si le nœud actuel n'a pas encore été visité.  

            visited.add(temp)  
            # Ajoute le nœud actuel à l'ensemble des nœuds visités pour éviter de le revisiter.  

            min_heap = []  
            # Initialise un tas binaire (min-heap) pour stocker les voisins et leurs coûts, 
            # permettant de trouver efficacement le nœud avec le coût minimal.  

            # Met à jour les coûts pour les voisins du nœud actuel
            for neighbor in graph[temp]:  
                if neighbor not in visited:  
                    # Vérifie si le voisin n'a pas encore été visité.  

                    cost = node_data[temp]['cost'] + graph[temp][neighbor]  
                    # Calcule le coût total pour atteindre ce voisin via le nœud actuel.  

                    if cost < node_data[neighbor]['cost']:  
                        # Si le nouveau coût est inférieur au coût précédemment enregistré pour ce voisin :  
                        node_data[neighbor]['cost'] = cost  
                        # Met à jour le coût minimal pour atteindre ce voisin.  

                        node_data[neighbor]['pred'] = node_data[temp]['pred'] + [temp]  
                        # Met à jour le chemin prédécesseur pour inclure le nœud actuel.  

                    heappush(min_heap, (node_data[neighbor]['cost'], neighbor))  
                    # Ajoute ce voisin et son coût dans le tas pour un traitement futur.  

            # Passe au nœud suivant avec le coût le plus bas parmi les non-visités
            temp = min_heap[0][1] if min_heap else None  
            # Si le tas est vide, cela signifie qu'il n'y a plus de chemin disponible.  

            if temp is None:  
                # Si aucun nœud n'est disponible, la recherche s'arrête.  
                break  

            # Met à jour la visualisation à chaque étape pour montrer les changements en temps réel.  
            update_visualization(current_node=temp, shortest_path_edges=shortest_path_edges)  
        else:  
            break  # Si le nœud est déjà visité, on quitte la boucle.  

    # Génère le chemin le plus court une fois la destination atteinte ou la recherche terminée.
    if node_data[dest]['cost'] != inf:  
        # Vérifie si un chemin valide vers la destination existe.  

        path = node_data[dest]['pred'] + [dest]  
        # Reconstruit le chemin à partir des prédécesseurs stockés dans `node_data`.  

        for i in range(len(path) - 1):  
            shortest_path_edges.append((path[i], path[i + 1]))  
            # Ajoute les arêtes du chemin dans la liste pour les visualiser.  

        print("Shortest Distance:", node_data[dest]['cost'])  
        # Affiche la distance totale minimale pour atteindre la destination.  

        print("Shortest Path:", " -> ".join(path))  
        # Affiche le chemin complet sous forme lisible.  

        update_visualization(shortest_path_edges=shortest_path_edges)  
        # Met à jour la visualisation avec le chemin final en rouge.  
    else:  
        print(f"No path from {src} to {dest}")  
        # Affiche un message si aucun chemin n'est trouvé.  


# Fonction principale pour configurer le graphe et lancer la visualisation  
def main():
    graph = {
        'A': {'B': 2, 'C': 4},
        'B': {'A': 2, 'C': 3, 'D': 8},
        'C': {'A': 4, 'B': 3, 'E': 5, 'D': 2},
        'D': {'B': 8, 'C': 2, 'E': 11, 'F': 22},
        'E': {'C': 5, 'D': 11, 'F': 1},
        'F': {'D': 22, 'E': 1}
    }

    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=800, font_size=10)
    plt.show(block=False)

    source = 'A'
    destination = 'F'
    dijkstra(graph, source, destination, G, pos)
    plt.show()

if __name__ == "__main__":
    main()
