import heapq
import copy

def print_succ(state):
    state = twoD(state)
    suc = sorted(succ(state))
    # print all successors of state and hueristic value
    for s in suc:
        ss = str(s).replace('[', '').replace(']', '')
        print("[{0}] h={1}".format(ss, h(s)))

def findZero(state):
    # get coordinates of zero in the board
    r = 0
    for row in state:
        c = 0
        for column in row:
            if column == 0:
                return [r, c]
            c += 1
        r += 1
    return None

def succ(state):
    # check if not goal state
    if state != [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
        # get all possible moves from given state
        zero = findZero(state)
        successors = []
        # Down 
        if zero[0] != 0:
            down = copy.deepcopy(state)
            swap = down[zero[0] - 1][zero[1]]
            down[zero[0]][zero[1]] = swap
            down[zero[0] - 1][zero[1]] = 0
            successors.append(down)
        # Up
        if zero[0] != 2:
            up = copy.deepcopy(state)
            swap = up[zero[0] + 1][zero[1]]
            up[zero[0]][zero[1]] = swap
            up[zero[0] + 1][zero[1]] = 0
            successors.append(up)
        # Left
        if zero[1] != 0:
            left = copy.deepcopy(state)
            swap = left[zero[0]][zero[1] - 1]
            left[zero[0]][zero[1]] = swap
            left[zero[0]][zero[1] - 1] = 0
            successors.append(left)
        # Right
        if zero[1] != 2:
            right = copy.deepcopy(state)
            swap = right[zero[0]][zero[1] + 1]
            right[zero[0]][zero[1]] = swap
            right[zero[0]][zero[1] + 1] = 0
            successors.append(right)
    
        return successors
    else:
        return None

def solve(state):
    state = twoD(state)
    # initialize priority queues and goal state
    closed = []
    open = []
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    # add initial state into unvisited priority queue
    heuristic = h(state)
    heapq.heappush(open, (heuristic + 0, state, (0, heuristic, -1)))

    p = None
    while True:
        # if there are no more states, search failed
        if len(open) == 0:
            return None
        
        # pop out unvisited state to check if it is the goal state
        p = heapq.heappop(open)
        closed.append(p)
        
        # check if goal
        if p[1] == goal:
            # create list of shortest path 
            best = []
            path = 0
            while path != -1:
                best.insert(0, p)
                path = p[2][2]
                p = closed[path]
            
            # format and print output
            i = 0
            for b in best:
                board = str(b[1]).replace('[', '').replace(']', '')
                print('[{0}] h={1} moves: {2}'.format(board, h(b[1]), i))
                i += 1
            return best
        
        # next states
        successors = succ(p[1])
        
        for s in successors:
            heuristic = h(s) # successor's heuristic value
            parent = closed.index(p) # parent state index located in closed list
            distance = g(closed, parent) # distance from starting state
            f = distance + heuristic # f(n)
            tupl = (distance, heuristic, parent)
            info = (f, s, tupl)

            # check if new state by going through open and closed
            found = False
            
            # check if successor is already in a list
            for o in open:
                if s == o[1]:
                    found = True
            
            for c in closed:
                if s == c[1]:
                    found = True
            
            if not found:
                heapq.heappush(open, info)
            else:
                # search through open queued states and check if successors is present
                for o in open:
                    if s == o[1]:
                        # if distance is better, update state
                        if distance < o[2][0]:
                            open.remove(o)
                            #heapq.heappush(open, (f, o[1], o[2]))
                            heapq.heappush(open, info)

                # search through closed (visited) states
                for c in closed:
                    if s == c[1]:
                        found = True
                        # if the distance is shorter (better) push to priority queue
                        if distance < c[2][0]:
                            heapq.heappush(open, info)

def manhattan(num, current):
    # position number needs to be to get goal state
    dest = {
        1 : [0,0],
        2 : [0,1],
        3 : [0,2],
        4 : [1,0],
        5 : [1,1],
        6 : [1,2],
        7 : [2,0],
        8 : [2,1]
    }
    if num == 0:
        return None
    else:
        goal = dest[num]
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def h(state):
    total = 0 # return var
    row = 0 # track rows

    # go through board and get sum of all manhattan values
    for three in state:
        column = 0 # track columns
        for spot in three:
                if spot != 0:
                    total += manhattan(spot, [row, column])
                column += 1
        row += 1
    
    return total

def g(pointer, index):
    return pointer[index][2][0] + 1

def twoD(state):
    return [[state[0], state[1], state[2]], [state[3], state[4], state[5]], [state[6], state[7], state[8]]]
