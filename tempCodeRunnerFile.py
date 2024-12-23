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