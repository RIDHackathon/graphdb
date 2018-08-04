from flask import Flask, jsonify
app = Flask(__name__)

graph = {
    'bob' : ['carol', 'john', 'jill'],
    'carol': ['joe', 'mike'],
    'jill': ['owen'],
    'john': ['lucy', 'moe']
}

weights = {
    ('carol', 'joe'): 7,
    ('carol', 'mike'): 4,
    ('bob', 'carol'): 10,
    ('bob', 'jill'): 7,
    ('bob', 'john'): 5,
    ('jill', 'owen'): 3,
    ('john', 'lucy'): 4,
    ('john', 'moe'): 8
}

def find_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
                if newpath: return newpath
        return None

def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

def get_weight_scores(graph, nm1, nm2):
    ind_weights = []
    measures = {}
    conn = find_shortest_path(graph, nm1, nm2)
    for i in range(len(conn)):
        for j in range(len(conn)):
            if conn[i]!=conn[j]:
                ind_weights.append((conn[i],conn[j]))
    for w in ind_weights:
        if w in weights.keys():
            measures[w] = weights[w]
    return measures

@app.route('/getpath/<string>')
def path(string):
	names = string.split('-')
	output = find_shortest_path(graph, names[0], names[1])
	scores = get_weight_scores(graph, names[0], names[1])
	return "->".join(output)

@app.route('/getweight/<string>')
def weightscores(string):
	names = string.split('-')
	scores = get_weight_scores(graph, names[0], names[1])
	return str(scores)

if __name__ == '__main__':
    app.run(debug=True)
