from collections import deque
import itertools


class SmartTwoControl:

    def __init__(self, people):
        self.people = people
        self.start_path = f"0{''.join(sorted(people))}|"
        self.end_path = f"1|{''.join(sorted(people))}"

    def is_valid_edge(self, edge):
        if not edge.count('A') and not edge.count('C') and not edge.count('E'):
            return False
        return True

    def is_valid_node(self, lhs, rhs):
        for side in (lhs, rhs):
            if side.count('B') and side.count('C') and len(set(side)) == 2:
                return False
            if side.count('A') and side.count('D') and len(set(side)) == 2:
                return False
            if side.count('F') and not side.count('E'):
                return False
        return True

    def build_nodes(self):
        nodes = set()
        permutations = set(itertools.permutations(f'|{self.people}'))
        permutations =set([''.join(item) for item in permutations])

        for permutation in permutations:
            lhs = sorted(permutation.split('|')[0])
            rhs = sorted(permutation.split('|')[1])
            label = f"{''.join(lhs)}|{''.join(rhs)}"

            if self.is_valid_node(lhs, rhs):
                nodes.add(f'0{label}')
                nodes.add(f'1{label}')
        return nodes

    def build_edges(self):
        edges = set()
        combinations = set(list(itertools.combinations(self.people, 2)))
        combinations_single = set(list(itertools.combinations(self.people, 1)))
        combinations = combinations.union(combinations_single)

        for combination in combinations:
            if self.is_valid_edge(combination):
                edges.add(combination)
        return edges

    def build_graph(self):
        nodes = self.build_nodes()
        edges = self.build_edges()
        graph = {node: list() for node in nodes}

        for node in nodes:
            lhs = node.split('|')[0][1:]
            rhs = node.split('|')[1]
            position = node[0]

            for edge in edges:
                is_full = False if len(edge) == 1 else True
                is_valid = False

                if position == '0' and is_full and lhs.count(edge[0]) and lhs.count(edge[1]):
                    is_valid = True
                elif position == '0' and not is_full and lhs.count(edge[0]):
                    is_valid = True
                elif position == '1' and is_full and rhs.count(edge[0]) and rhs.count(edge[1]):
                    is_valid = True
                elif position == '1' and not is_full and rhs.count(edge[0]):
                    is_valid = True

                if not is_valid:
                    continue

                right_result, left_result = '', ''

                if is_full and position == '0':
                    left_result = lhs.replace(edge[0], '', 1)
                    left_result = left_result.replace(edge[1], '', 1)
                    right_result = ''.join(sorted(rhs + ''.join(edge)))

                elif is_full and position == '1':
                    right_result = rhs.replace(edge[0], '', 1)
                    right_result = right_result.replace(edge[1], '', 1)
                    left_result = ''.join(sorted(lhs + ''.join(edge)))

                elif not is_full and position == '0':
                    left_result = lhs.replace(edge[0], '', 1)
                    right_result = ''.join(sorted(rhs + ''.join(edge)))

                elif not is_full and position == '1':
                    right_result = rhs.replace(edge[0], '', 1)
                    left_result = ''.join(sorted(lhs + ''.join(edge)))

                new_position = '1' if position == '0' else '0'
                state = f'{new_position}{left_result}|{right_result}'
                graph[node].append(state)

        return graph

    def find_path(self, graph):
        start = self.start_path
        end = self.end_path

        dist = {start: [start]}
        que = deque(dist)
        while len(que):
            at = que.popleft()
            for next in graph.get(at, []):
                if next not in dist:
                    dist[next] = dist[at] + [next]
                    que.append(next)
        return dist.get(end)

    def translate_labels(self, label):
        codes = {
            'A': 'Piloto',
            'B': 'Oficial',
            'C': 'Chefe de Serviço',
            'D': 'Comissário de Bordo',
            'E': 'Policial',
            'F': 'Detento',
        }
        return [codes[code] for code in label]

    def execute_steps(self, steps):

        def substract(a, b):
            low, high = None, None
            if len(a) < len(b):
                low = a
                high = b
            else:
                low = b
                high = a
            for i in range(0, len(low)):
                high = high.replace(low[i], '', 1)
            return high

        for i in range(0, len(steps)+1):
            current_step = steps[i]
            next_step = steps[i+1]

            current_lhs = current_step.split('|')[0][1:]
            current_rhs = current_step.split('|')[1]
            current_pos = current_step[0]

            next_lhs = next_step.split('|')[0][1:]
            next_rhs = next_step.split('|')[1]

            if next_step == self.end_path:
                print(f'Pessoas no avião: {self.translate_labels(next_rhs)}')
                print(f'Finalizou')
                break

            if current_pos == '0':
                print(f'Pessoas no terminal de embarque: {self.translate_labels(current_lhs)}')
                print(f'Embarcando no veiculo: {self.translate_labels(substract(current_lhs, next_lhs))}')
                print(f'Veiculo chegou ao avião')
            else:
                print(f'Pessoas no avião: {self.translate_labels(current_rhs)}')
                print(f'Embarcando no veiculo: {self.translate_labels(substract(current_rhs, next_rhs))}')
                print(f'Veiculo chegou no terminal')


    def run(self):
        graph = self.build_graph()
        path = self.find_path(graph)
        self.execute_steps(path)


if __name__ == '__main__':
    people = 'ABBCDDEF'
    control = SmartTwoControl(people)
    control.run()
