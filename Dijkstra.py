import sys
import networkx as nx
import matplotlib.pyplot as plt
from heapq import heappush

def dijkstra(graph, src, dest, G, pos):
    inf = sys.maxsize
    node_data = {node: {'cost': inf, 'pred': []} for node in graph}
    node_data[src]['cost'] = 0
    visited = set()
    temp = src
    shortest_path_edges = []

    # Visualization update function
    def update_visualization(current_node=None, shortest_path_edges=[]):
        plt.clf()
        colors = ['green' if node in visited else 'lightblue' for node in G.nodes()]
        nx.draw(G, pos, node_color=colors, with_labels=True, node_size=800, font_size=10)
        
        # Draw the path in green
        nx.draw_networkx_edges(G, pos, edgelist=shortest_path_edges, edge_color='red', width=2)
        
        # Highlight the current node in yellow
        if current_node:
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='yellow')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        # Update plot
        plt.pause(0.5)  # Delay to visualize step-by-step

    while temp != dest:
        if temp not in visited:
            visited.add(temp)
            min_heap = []

            # Update costs for neighbors of the current node
            for neighbor in graph[temp]:
                if neighbor not in visited:
                    cost = node_data[temp]['cost'] + graph[temp][neighbor]
                    if cost < node_data[neighbor]['cost']:
                        node_data[neighbor]['cost'] = cost
                        node_data[neighbor]['pred'] = node_data[temp]['pred'] + [temp]
                    heappush(min_heap, (node_data[neighbor]['cost'], neighbor))
            
            # Proceed to the next closest unvisited node
            temp = min_heap[0][1] if min_heap else None
            if temp is None:
                break
            
            # Update visualization
            update_visualization(current_node=temp, shortest_path_edges=shortest_path_edges)
        else:
            break

    # Generate the shortest path
    if node_data[dest]['cost'] != inf:
        path = node_data[dest]['pred'] + [dest]
        for i in range(len(path) - 1):
            shortest_path_edges.append((path[i], path[i + 1]))
        print("Shortest Distance:", node_data[dest]['cost'])
        print("Shortest Path:", " -> ".join(path))
        update_visualization(shortest_path_edges=shortest_path_edges)
    else:
        print(f"No path from {src} to {dest}")

# Main function to set up the graph and run visualization
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
