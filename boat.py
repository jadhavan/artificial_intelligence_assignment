#!/usr/bin/env python

class Problem(object):

    def __init__(self):
        self.initial = {'missionaries_left':3,'cannibals_left':3,'boat_pos': 'left','missionaries_right':0,'cannibals_right':0}
        self.goal = {'missionaries_left':0,'cannibals_left':0,'boat_pos': 'right','missionaries_right':3,'cannibals_right':3}

    def actions(self, state):
        #print "Finding the possible actions for the given state..."
        #possible actions [no of Missionaries, no of Cannibals]
        actions = [[2,0],[0,2],[1,0],[0,1],[1,1]];
        for i in actions:
            # to check the if the move is possible, that is,
            # the actions that makes the cannibal outnumber Missionaries are not taken into consideration
            if state["boat_pos"] == "left":
                if ((state["missionaries_right"] + i[0]) > 0 and ( ( state["missionaries_right"] + i[0])<(state["cannibals_right"] + i[1]))) | ( (state["missionaries_left"] - i[0]) < (state["cannibals_left"] - i[1]) and ((state["missionaries_left"] - i[0]) > 0)) | ((state["missionaries_left"] - i[0]) < 0) | ((state["cannibals_left"] - i[1]) < 0 ):
                    continue;
            elif state["boat_pos"] == "right":
                if ((state["missionaries_left"] + i[0]) > 0 and ( ( state["missionaries_left"] + i[0])<(state["cannibals_left"] + i[1]))) | ( (state["missionaries_right"] - i[0]) < (state["cannibals_right"] - i[1]) and ((state["missionaries_right"] - i[0]) > 0)) |  ((state["missionaries_right"] - i[0]) < 0) | ((state["cannibals_right"] - i[1]) < 0):
                    continue;
            yield i

    def result(self, state, action):
        # returns new state from the current state due to the given action
        result = {'missionaries_left':3,'cannibals_left':3,'boat_pos': 'left','missionaries_right':0,'cannibals_right':0};
        if state["boat_pos"] == "left":
            result["missionaries_left"] = state["missionaries_left"] -action[0];
            result["cannibals_left"] = state["cannibals_left"] -action[1];
            result["missionaries_right"] = state["missionaries_right"] +action[0];
            result["cannibals_right"] = state["cannibals_right"] +action[1];
            result["boat_pos"] = "right"
        elif state["boat_pos"] == "right":
            result["missionaries_left"] = state["missionaries_left"] +action[0];
            result["cannibals_left"] = state["cannibals_left"] +action[1];
            result["missionaries_right"] = state["missionaries_right"] -action[0];
            result["cannibals_right"] = state["cannibals_right"] -action[1];
            result["boat_pos"] = "left"
        return result

    def goal_test(self, state):
        #returns true if goal reached
        #print "Testing if the given node is a goal node..."
        if cmp(self.goal,state) == 0:
            return True
        return False


class Node:
    def __init__(self,state,parent = None,action = None):
        self.state = state;
        self.parent = parent;
        self.action = action;
        # depth and path cost are considered to be same
        # as the path cost is 1
        self.depth = 0;
        if self.parent:
            self.depth = parent.depth +1;

    def __repr__(self):
        return "Node%d  M = %s C= %s      %s     M= %s  C = %s\n" % (self.depth+1,self.state["missionaries_left"],self.state["cannibals_left"],
        self.state['boat_pos'],self.state['missionaries_right'],self.state["cannibals_right"])

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        #"List the nodes reachable in one step from this node."
        #for action in problem.actions(self.state):
        #    return self.child_node(problem, action)
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        #print Node(next, self, action).state
        return Node(next, self, action)

    def solution(self):
        #"Return the sequence of actions to go from the root to this node."
        return [node.action for node in self.path()[1:]]

    def path(self):
        #"Return a list of nodes forming the path from the root to this node."
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

if __name__ == "__main__" :
    # tree search
    #implement fifo queue BFS
    frontier =[];
    explored = [];
    problem = Problem()
    frontier.append(Node(problem.initial))
    while frontier:
        frontier_states =[];
        node = frontier.pop()
        explored.append(node.state)
        #print node.state
        if problem.goal_test(node.state):
            print "Path to goal\n\n"
            print "            LEFT    BOAT POSITION    RIGHT\n"
            print node.path()
            break;
        for f_state in frontier:
            frontier_states.append( f_state.state);
        for newnode in node.expand(problem):
            if newnode.state not in explored and newnode.state not in frontier_states:
                frontier.append(newnode)

        #print "Frontier\n",frontier_states
        #print "Explored\n",explored
