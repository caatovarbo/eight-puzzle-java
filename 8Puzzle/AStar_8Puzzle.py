
from Queue import heapq as hq
from copy import deepcopy

k, N, goal = [None] * 3

class State:
    def __init__(self, sig):
        self.sig = deepcopy(sig)
        for i in xrange(N):
            if self.sig[i] == 0:
                self.pos0 = i
                break
        self.h = self.__heuristic__()
        self.str = self.__toStr__()

    def __toStr__(self):
        return reduce(lambda x, y: x + str(y), self.sig, '')

    def __str__(self):
        return self.str

    def __moveCount__(self, i):
        if self.sig[i] == 0:
            return 0
        return abs((i / k) - (self.sig[i] / k)) + abs((i % k) - (self.sig[i] % k))

    def __heuristic__(self):
        return reduce(lambda x, y: x + self.__moveCount__(y), xrange(N), 0)

    # Manhattan distance
    def heuristic(self):
        return self.h

    def moves(self):
        candidates = []
        copy = deepcopy(self.sig)
        if self.pos0 >= k:
            copy[self.pos0], copy[self.pos0 - k] = copy[self.pos0 - k], copy[self.pos0]
            candidates.append([State(copy), 'U'])
            copy[self.pos0], copy[self.pos0 - k] = copy[self.pos0 - k], copy[self.pos0]
        if self.pos0 < N-k:
            copy[self.pos0], copy[self.pos0 + k] = copy[self.pos0 + k], copy[self.pos0]
            candidates.append([State(copy), 'D'])
            copy[self.pos0], copy[self.pos0 + k] = copy[self.pos0 + k], copy[self.pos0]
        if (self.pos0 % k) > 0:
            copy[self.pos0], copy[self.pos0 - 1] = copy[self.pos0 - 1], copy[self.pos0]
            candidates.append([State(copy), 'L'])
            copy[self.pos0], copy[self.pos0 - 1] = copy[self.pos0 - 1], copy[self.pos0]
        if (self.pos0 % k) < k-1:
            copy[self.pos0], copy[self.pos0 + 1] = copy[self.pos0 + 1], copy[self.pos0]
            candidates.append([State(copy), 'R'])
            copy[self.pos0], copy[self.pos0 + 1] = copy[self.pos0 + 1], copy[self.pos0]
        return candidates

    def isGoal(self):
        return self.sig == goal

def astar(start):
    pq = []
    closed = set()
    hq.heappush(pq, [start.heuristic(), 0, start, []])
    while pq:
        f, g, cur, path = hq.heappop(pq)
        if cur.isGoal():
            return g, path
        closed.add(str(cur))
        for child, move in cur.moves():
            if str(child) not in closed:
                p = deepcopy(path)
                p.append(move)
                hq.heappush(pq, [g+1 + child.heuristic(), g+1, child, p])
    return None

if __name__ == "__main__":
    k = 3;
#    k = int(raw_input())
    N = k * k

#    - Entrada por consola
#    pattern = [int(raw_input()) for i in xrange(N)]

    goal = [i for i in xrange(1, N)]
    pattern = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    goal.append(0)
    count, path = astar(State(pattern))
    moves = {'U':'UP', 'D':'DOWN', 'L':'LEFT', 'R':'RIGHT'}
    if count == 0:
        print "Resuelto :)"
    else:
        print "Movimientos necesarios: ", count
    for move in path:
        print moves[move]
