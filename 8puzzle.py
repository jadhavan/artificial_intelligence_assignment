#!/usr/bin/env python
# -*- coding: utf-8 -*-
from heapq import heappush, heappop
from random import shuffle
import time

class Solver:
  def __init__(self, initial_state=None):
    self.initial_state = State(initial_state)
    self.goal = range(0, 9)
    #self.goal.append(0);

  def _rebuildPath(self, end):
    path = [end]
    state = end.parent
    while state.parent:
      path.append(state)
      state = state.parent
    return path

  def solve(self):
    frontier = PriorityQueue()
    frontier.add(self.initial_state)
    explored = set()
    moves = 0
    print 'Initial State'
    print frontier.peek(), '\n\n'

    while frontier:
      #print frontier[0].score()
      current = frontier.poll()
      if current.values == self.goal:
        print 'Result'
        path = self._rebuildPath(current)
        for state in reversed(path):
          print state
        print 'solved %d Movements' % len(path)
        break
      moves += 1
      for state in current.possible_moves(moves):
        if state not in explored:
          frontier.add(state)
      explored.add(current)



class State:
  def __init__(self, values, moves=0, parent=None):
    self.values = values
    self.moves = moves
    self.parent = parent
    self.goal = range(0, 9)
    #self.goal.append(0);

  def possible_moves(self, moves):
    # obtainig the possible actions
    i = self.values.index(0)
    if i in [3, 4, 5, 6, 7, 8]:
      new_board = self.values[:]
      new_board[i], new_board[i - 3] = new_board[i - 3], new_board[i]
      yield State(new_board, moves, self)
    if i in [1, 2, 4, 5, 7, 8]:
      new_board = self.values[:]
      new_board[i], new_board[i - 1] = new_board[i - 1], new_board[i]
      yield State(new_board, moves, self)
    if i in [0, 1, 3, 4, 6, 7]:
      new_board = self.values[:]
      new_board[i], new_board[i + 1] = new_board[i + 1], new_board[i]
      yield State(new_board, moves, self)
    if i in [0, 1, 2, 3, 4, 5]:
      new_board = self.values[:]
      new_board[i], new_board[i + 3] = new_board[i + 3], new_board[i]
      yield State(new_board, moves, self)

  def score(self):
    return self._h() + self._g()

  def _h(self):
      #index to coordinates
      coordinates = {0:[0,0],1:[0,1],2:[0,2],3:[1,0],4:[1,1],5:[1,2],6:[2,0],7:[2,1],8:[2,2]}
      manhattan_distance = 1;
      for i in self.values:
          pos_state=coordinates[self.values.index(i)]
          pos_goal=coordinates[self.goal.index(i)]
          manhattan_distance += (abs(pos_goal[0]-pos_state[0]) + abs(pos_goal[1]-pos_state[1]))
      return manhattan_distance;

  def _g(self):
    return self.moves

  def __cmp__(self, other):
    return self.values == other.values

  def __eq__(self, other):
    return self.__cmp__(other)

  def __hash__(self):
    return hash(str(self.values))

  def __lt__(self, other):
    return self.score() < other.score()

  def __str__(self):
    print
    return '\n'.join([str(self.values[:3]),
        str(self.values[3:6]),
        str(self.values[6:9])]).replace('[', '').replace(']', '').replace(',', '').replace('0', ' ')

class PriorityQueue:
  def __init__(self):
    self.pq = []

  def add(self, item):
    heappush(self.pq, item)

  def poll(self):
    return heappop(self.pq)

  def peek(self):
    return self.pq[0]

  def remove(self, item):
    print "in remove"
    value = self.pq.remove(item)
    heapify(self.pq)
    return value is not None

  def __len__(self):
    return len(self.pq)

def inversion(puzzle):
    noInversion = 0;
    for z in puzzle:
        j = puzzle.index(z)+1
        for i in range(j,9):
            if puzzle[i] == 0:
                continue
            if puzzle[i] < z:
                noInversion+=1
        j+=1
    print "# of Inversions : ",noInversion
    return noInversion

if __name__ == '__main__':

    puzzle = range(9)
    shuffle(puzzle)
    while inversion(puzzle)%2 !=0:
        print "Generated state cannot reach the goal state"
        print "Generating new state"
        shuffle(puzzle)
    print puzzle
    start = time.time()
    solver = Solver(puzzle)
    solver.solve()
    end = time.time()
    print 'Time Taken %2.f Seconds' % float(end - start)
