import json
import networkx as nx

thresholds = {}
with open("data/thresholds.txt") as f:
    for line in f:
        name, th = line.split()
        thresholds[name] = int(th)


def find_cover_max_degree(g):
    """
        Max-degree heuristics
    """

    dgs = g.degree()
    cover = set()

    for u, v in g.edges():
        if u not in cover and v not in cover:
            if dgs(u) > dgs(v):
                cover.add(u)
            else:
                cover.add(v)

    return sorted([int(c) for c in cover])


failed = 0
result = {}
for name, th in thresholds.items():
    with open(f"data/{name}") as f:
        f.readline()
        g = nx.read_edgelist(f, comments="c")

    cover = find_cover_max_degree(g)

    if len(cover) <= th:
        print(name, "pass")
        result[name] = cover
    else:
        failed += 1
        print(f"{name} fail size={len(g.nodes())} cover={len(cover)} th={th}")


print("Passed:", len(result), "Failed:", failed)
with open("result.json", "w") as f:
    json.dump(result, f, indent=2)
