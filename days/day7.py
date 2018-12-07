import re
from typing import List, Dict

from days import AOCDay, day

BASE_TIME = 60
WORKERS = 5


class Node:
    parents: List['Node'] = []
    children: List['Node'] = []
    name: str = None
    time_left: int = 0
    done: bool = False

    _instances: Dict[str, 'Node'] = {}

    def __init__(self, name: str, parents: List['Node'], children: List['Node']):
        self.name = name
        self.parents = parents
        self.children = children
        self.time_left = BASE_TIME + ord(self.name) - ord('A') + 1
        self.done = False

    def add_child(self, child: 'Node'):
        self.children.append(child)

    def add_parent(self, parent: 'Node'):
        self.parents.append(parent)

    @classmethod
    def get(cls, name: str):
        if name not in cls._instances.keys():
            cls._instances[name] = Node(name, [], [])
        return cls._instances[name]

    @classmethod
    def get_all(cls):
        return cls._instances

    @classmethod
    def reset(cls):
        cls._instances = {}

    @classmethod
    def get_initial(cls):
        return [x for x in cls._instances.values() if not x.parents]

    def __gt__(self, other):
        return self.name > other.name

    def __repr__(self):
        return "({})".format(self.__str__())

    def __str__(self):
        return "{} -> {} -> {}".format(",".join([x.name for x in self.parents]),
                                       self.name,
                                       ",".join([x.name for x in self.children]))


class Worker:
    worker_id: int = 0
    current_task: Node = None
    busy: bool = False

    def __init__(self, worker_id: int):
        self.worker_id = worker_id

    def start_task(self, task: Node):
        if self.current_task is None:
            self.current_task = task
            self.busy = True
        else:
            raise ValueError("Already working on task {}".format(self.current_task))

    def tick(self):
        if self.current_task is not None and not self.current_task.done:
            self.current_task.time_left -= 1
            if self.current_task.time_left == 0:
                self.current_task.done = True
                self.busy = False

    def done(self):
        if not self.busy and self.current_task:
            task = self.current_task
            self.current_task = None
            return task
        else:
            return None

    def __str__(self):
        return self.current_task.name if self.current_task else "."


@day(7)
class DaySeven(AOCDay):
    test_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
    regex = r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.'

    def common(self, input_data):
        Node.reset()
        # input_data = self.test_input.split("\n")
        for inp in input_data:
            m = re.match(self.regex, inp)
            if m:
                parent = m.group(1)
                child = m.group(2)
                Node.get(parent).add_child(Node.get(child))
                Node.get(child).add_parent(Node.get(parent))

        # for name, node in Node.get_all().items():
        #     yield str(node)

    def part1(self, input_data):
        """
        https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
        L ← Empty list that will contain the sorted elements
        S ← Set of all nodes with no incoming edge
        while S is non-empty do
            remove a node n from S
            add n to tail of L
            for each node m with an edge e from n to m do
                remove edge e from the graph
                if m has no other incoming edges then
                    insert m into S
        if graph has edges then
            return error   (graph has at least one cycle)
        else
            return L   (a topologically sorted order)
        """
        result = []
        start_nodes = Node.get_initial()
        while len(start_nodes) != 0:
            node = start_nodes.pop(0)
            result.append(node)
            for m in node.children[:]:
                node.children.remove(m)
                m.parents.remove(node)
                if len(m.parents) == 0:
                    start_nodes.append(m)
                    start_nodes.sort()
        if any(x.parents or x.children for x in Node.get_all().values()):
            raise ValueError("Dependency graph contains cycles")
        else:
            yield "".join([x.name for x in result])

    def part2(self, input_data):
        available_nodes = Node.get_initial()
        done_tasks = []
        workers = [Worker(n+1) for n in range(WORKERS)]
        current_second = 0

        def _get_free_worker():
            if any(w.busy is False for w in workers):
                return [x for x in workers if not x.busy][0]
            else:
                return None

        # yield "{:>5}  {}  {}".format("Sec.", " ".join([str(w.worker_id) for w in workers]), "Done")

        while len(available_nodes) != 0 or any(w.current_task for w in workers):
            # Check for any new tasks that can be added because their dependencies finished
            for w in workers:
                done = w.done()
                if done is not None:
                    done_tasks.append(done)
                    for m in done.children[:]:
                        done.children.remove(m)
                        m.parents.remove(done)
                        if len(m.parents) == 0:
                            available_nodes.append(m)
                            available_nodes.sort()

            # If there is a free worker and there are nodes, start that task.
            w = _get_free_worker()
            while w is not None and len(available_nodes) != 0:
                node = available_nodes.pop(0)
                w.start_task(node)
                w = _get_free_worker()

            # Then, execute a tick to continue the work
            for w in workers:
                w.tick()
            # yield "{:>5}  {}  {}".format(current_second, " ".join([str(w) for w in workers]), "".join([x.name for x in done_tasks]))
            current_second += 1

        yield "Tasks took {} seconds to complete".format(current_second - 1)
