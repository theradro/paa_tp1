import sys

# Create adjacency list from input file
# Returns adjacency list, number of vertices and number of edge
# Assumes vertices are v = {1,2,3,...,n}
def create_adjacency_list():
    adjacency_list = {}

    for line in sys.stdin.readlines():
        if len(line.split()) == 2:
            n,m = map(int, line.split())
        else:
            u,v,w = map(int, line.split())
            adjacency_list.setdefault(u, {})[v] = w
            # Run if graph is undirected
            adjacency_list.setdefault(v, {})[u] = w
    
    return adjacency_list, n, m

# Creates Weights matrix (W) from adjacency list and number of vertices
# Also creates Predecessor Matrix (PI)
# Assumes vertices are v = {1,2,3,...,n} 
def create_w_matrix(adjacency_list, n):
    W = []
    PI = []
    for i in range(n):
        row = []
        pi_row = []
        if (i+1) in list(adjacency_list):
            for j in range(n):
                if i == j:
                    row.append(0)
                    pi_row.append(0)
                else:
                    if (j+1) in list(adjacency_list[i+1]):
                        row.append(adjacency_list[i+1][j+1])
                        pi_row.append(i+1)
                    else:
                        row.append(9999)
                        pi_row.append(0)
        else:
            for j in range(n):
                if i == j:
                    row.append(0)
                    pi_row.append(0)
                else:
                    row.append(9999)
                    pi_row.append(0)  
        W.append(row)
        PI.append(pi_row)
    return W, PI

# Floyd-Warshall algorithm for all pairs shortest paths
# Returns shortest distances matrix (D(n))
# Returns predecessors matrix (Pre(n))
# Assumes vertices are v = {1,2,3,...,n}
def floyd_warshall(W, PI):
    n = len(W)
    D = []
    PRE = []
    D.append(W)
    PRE.append(PI)
    for k in range(1,n+1):
        D_k = []
        PRE_k = []
        for i in range(n):
            row = []
            pre_row = []
            for j in range(n):
                d = min(D[k-1][i][j], D[k-1][i][k-1] + D[k-1][k-1][j])
                pre = 0
                if D[k-1][i][j] <= D[k-1][i][k-1] + D[k-1][k-1][j]:
                    pre = PRE[k-1][i][j]
                else:
                    pre = PRE[k-1][k-1][j]
                row.append(d)
                pre_row.append(pre)
            D_k.append(row)
            PRE_k.append(pre_row)
        D.append(D_k)
        PRE.append(PRE_k)
    return(D[n],PRE[n])

# Finds the shortest path with maximum distance
# Returns vertices (u,v) separately and the maximum distance dmax
# Assumes vertices are v = {1,2,3,...,n}
def find_biggest_path(D):
    di = 0
    dmax = 0
    for i, row in enumerate(D):
        for j, colum in enumerate(row):
            dmax = max(di,D[i][j])
            if dmax != di:
                u = i+1
                v = j+1
                di = dmax
    return u, v, dmax

# Obtains the list of vertices that compose the path from vertex i to j given a predecessor matrix PRE
# Assumes vertices are v = {1,2,3,...,n}
def find_path(PRE, i, j):
    path = []
    path.append(j)
    while PRE[i-1][j-1] != i:
        j = PRE[i-1][j-1]
        path.append(j)
    path.append(i)
    path.reverse()
    return path

# Writes in a file: -the distance of the biggest path (dmax);
#                   -the starting vertex (u) and end vertex (v) of the biggest path;
#                   -the number of vertices in the path;
#                   -the vertices that compose the path
# Assumes vertices are v = {1,2,3,...,n}
def write_to_file(dmax, u, v, path):
    sys.stdout.write(str(dmax) + '\n')
    sys.stdout.write(str(u)+ " " +str(v) + '\n')
    sys.stdout.write(str(len(path)) + '\n')
    path_string = ""
    for vertex in path:
        path_string += str(vertex) + " "
    sys.stdout.write(path_string + '\n')

def main():
    adjacency_list, n , m = create_adjacency_list()

    W, PI = create_w_matrix(adjacency_list, n)

    D,PRE = floyd_warshall(W,PI)

    u,v,dmax = find_biggest_path(D)
            
    path = find_path(PRE, u, v)

    write_to_file(dmax, u, v, path)

if __name__ == "__main__":
    main()