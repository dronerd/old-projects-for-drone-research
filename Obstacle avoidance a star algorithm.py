#This code was created for autonomously creating obstacle avoidance paths for drones, 
#which will be taught by training a random forest
#this research was published at CIEC 2024, leading to 3rd place award in U-18

#the a star algorithm was taking too much time, so lower the size of the map
#the maze is 16 by 21, one space is 10 cm.
#as the obstacles are 10 cm wide and drone center should be 15cm away, total 40cm square.
#which means 5 in width and length
import random
import numpy as np

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():
#one number indicates 10cm.
#thus, as the space would be 140cm横Ｘ200cm縦、maze would be 15x21
#y座標、ｘ座標の順で表示されていることに注意．
#最も下の中心から、最も上の中心に行くようにするべしである。
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


    # when placing obstacles, ひとつだけ重ならなければok
    #drone path planning は、囲むスクエアをもとに計算 3つ？

    a = 0
    objectposition = []
    iteration = 8
    overlap = 0
    while a < iteration:
      x = random.randint(2, 15)  # Adjusted range to avoid edge values 15
      y = random.randint(1, 9)  # Adjusted range to avoid edge values 10
      p = x
      q = y
      e = 0
      f = 0
      for e in range(1):# change here number to change the size of the obstacle. now set to 10cm (1)
         for f in range(1):
           if maze[p][q] == 1:
             overlap = 1
           q += 1
         q = y
         p += 1

      if overlap == 1:
        overlap = 0
        continue

      else:
          p = x
          q = y
          for g in range(3): #change here to change the area drone should not enter, not set to 30cm
            for h in range(3):
              maze[p][q] = 1
              q += 1
            q = y
            p += 1
          a += 1
          objectposition.append ((x+2,y+2))

    start = (20, 7)
    end = (0, 7)

    path = astar(maze, start, end)
    print(objectposition)
    print(path)
    patharray = np.array(path)
    pathgoal=path

    sizeofpath = len(path)

    # calculate angles
    pathgoal.pop(0)  #change the number of iterations here to change how far in this case 2 spaces forward to calculate the angle vector.
    pathgoal.pop(0)
    pathgoal.append((0,7))  #change the number of iterations here to change how far in this case 2 spaces forward to calculate the angle vector.
    pathgoal.append((0,7))
    pathgoalarray = np.array(pathgoal)

    direction = pathgoalarray - patharray

    #direction is array of (x,y)
    #extract y and x
    #divide the y by the x and i get tan

    directiony = direction[:,0]
    directionx = direction[:,1]
    direction_tan_angle = directionx / directiony
    direction_tan_anglelist = direction_tan_angle.tolist()

    #convert the tan to degrees. from -90 to 90, from right to left.

    degrees=[]

    #loop to convert the list to angles
    degrees.append(0)
    for i in range(sizeofpath):
       tangent = direction_tan_anglelist[i]
       if tangent==0:
         degrees.append(0)
       if tangent==-0.5:
         degrees.append(-26)
       if tangent==-1:
         degrees.append(-45)
       if tangent==-2:
         degrees.append(-63)
       if tangent==0.5:
         degrees.append(26)
       if tangent==1:
         degrees.append(45)
       if tangent==2:
         degrees.append(63)

    print(degrees)

      ##change the 0s on the maze to indicate path
    for position in path:
          maze[position[0]][position[1]] = 'X'

##change the 0s on the maze to indicate start and end
    maze[start[0]][start[1]] = 'S'
    maze[end[0]][end[1]] = 'G'
    straightpath = [(20,7) for i in range(sizeofpath)]
    straightpatharray = np.array(straightpath)
    subtracted_array = np.subtract(patharray, straightpatharray)
    deviation = subtracted_array[:,1]
    finaldeviation = list(deviation)
    print(finaldeviation)

    # Print out the maze
    for row in maze:
       print(' '.join(str(cell) for cell in row))


if __name__ == '__main__':
    main()