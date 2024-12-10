# 定义一个常量表示无穷大
INF = float('inf')

# Dijkstra算法实现
def dijkstra(graph, start):
    n = len(graph)
    # 存储从源点到各个顶点的最短距离，初始值为无穷大
    dist = [INF] * n
    # 源点到自身的距离为0
    dist[start] = 0
    # 记录每个顶点的前驱顶点，用于构建最短路径
    prev = [None] * n
    # 标记顶点是否已确定最短距离
    visited = [False] * n

    for _ in range(n):
        # 找到当前未确定最短距离的顶点中距离最小的顶点
        u = min((dist[i], i) for i in range(n) if not visited[i])[1]
        visited[u] = True
        for v in range(n):
            if graph[u][v] < INF and not visited[v]:
                new_dist = dist[u] + graph[u][v]
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u

    return dist, prev

# 根据前驱顶点构建最短路径
def build_path(prev, i):
    path = []
    while i is not None:
        path.append(i)
        i = prev[i]
    return path[::-1]

# 测试示例
if __name__ == "__main__":
    # 定义带权有向图的邻接矩阵
    graph = [[0, 0, 4, 2, 3, INF, INF, INF, INF, INF],
             [0, 0, INF, INF, INF, 10, 9, INF, INF, INF],
             [0, INF, 0, INF, INF, 6, 7, 10, INF, INF],
             [0, INF, INF, 0, INF, INF, 3, 8, INF, INF],
             [0, INF, INF, INF, 0, INF, INF, INF, 4, 8],
             [0, INF, INF, INF, INF, 0, INF, INF, 9, 6],
             [0, INF, INF, INF, INF, INF, 0, INF, 5, 4],
             [0, INF, INF, INF, INF, INF, INF, 0, INF, 8],
             [0, INF, INF, INF, INF, INF, INF, INF, 0, 4],
             [0, INF, INF, INF, INF, INF, INF, INF, INF, 0]]

    start_vertex = 0
    distances, predecessors = dijkstra(graph, start_vertex)

    for i in range(1, len(graph)):
        print(f"从顶点 {start_vertex} 到顶点 {i} 的最短距离为: {distances[i]}")
        path = build_path(predecessors, i)
        print(f"最短路径为: {' -> '.join(map(str, path))}")