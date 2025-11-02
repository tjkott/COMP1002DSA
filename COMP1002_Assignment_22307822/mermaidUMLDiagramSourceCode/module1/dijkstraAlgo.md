```mermaid
graph TD
    Start["Start dijkstraAlgorithm(start, end)"] --> Init["Reset all vertex distances to ∞<br>Set start_vertex distance = 0"];
    Init --> CreateList["Create 'unvisited' list of all vertices"];
    CreateList --> Loop{"While 'unvisited' list is not empty"};
    Loop -- Yes --> FindMin["Find vertex 'u' in 'unvisited'<br>with the smallest distance"];
    FindMin --> CheckPath{"Is 'u' None or is u.distance == ∞?"};
    CheckPath -- "Yes (No path)" --> EndLoop["End Loop"];
    CheckPath -- No --> RemoveU["Remove 'u' from 'unvisited' list"];
    RemoveU --> ForNeighbors{"For each neighbor 'v' of 'u'"};
    ForNeighbors -- loop --> CalculateDist["Calculate new_dist = u.distance + weight(u, v)"];
    CalculateDist --> CheckDist{"if new_dist < v.distance"};
    CheckDist -- Yes --> Update["Update v.distance = new_dist<br>Update v.predecessor = u"];
    Update --> ForNeighbors;
    CheckDist -- No --> ForNeighbors;
    ForNeighbors -- done --> Loop;
    Loop -- "No (List empty)" --> EndLoop;
    EndLoop --> Reconstruct{"Path exists to end_vertex?<br>(end_vertex.distance != ∞)"};
    Reconstruct -- Yes --> BuildPath["Build path by following predecessors from end_vertex"];
    Reconstruct -- No --> NoPath["Set 'No Path Found' message"];
    BuildPath --> Finish[End];
    NoPath --> Finish[End];
