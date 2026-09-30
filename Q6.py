import heapq

def main():
    n, e = map(int, input().split())

    modules = []
    graph = {}
    indegree = {}

    for _ in range(n):
        module = input().strip()
        modules.append(module)
        graph[module] = set()
        indegree[module] = 0

    for _ in range(e):
        a, b = input().split()

        if b not in graph[a]:
            graph[a].add(b)
            indegree[b] += 1

    heap = []

    for module in modules:
        if indegree[module] == 0:
            heapq.heappush(heap, module)

    order = []

    while heap:
        module = heapq.heappop(heap)
        order.append(module)

        for dependent in sorted(graph[module]):
            indegree[dependent] -= 1

            if indegree[dependent] == 0:
                heapq.heappush(heap, dependent)

    if len(order) == n:
        print(*order)
    else:
        print("CYCLE")

        state = {module: 0 for module in modules}
        parent = {}
        cycle = []

        def find_cycle(node):
            state[node] = 1

            for neighbor in graph[node]:
                if state[neighbor] == 0:
                    parent[neighbor] = node
                    if find_cycle(neighbor):
                        return True

                elif state[neighbor] == 1:
                    cycle.append(neighbor)

                    current = node
                    while current != neighbor:
                        cycle.append(current)
                        current = parent[current]

                    cycle.append(neighbor)
                    cycle.reverse()
                    return True

            state[node] = 2
            return False

        for module in sorted(modules):
            if state[module] == 0:
                if find_cycle(module):
                    break

        print(*cycle)


if __name__ == "__main__":
    main()
