import numpy as np
# grid=[[0,0,0,4,0,9,8,0,2],[5,7,0,3,8,0,0,0,4],[0,0,0,0,0,2,5,0,0,],[3,2,8,0,1,7,0,6,0],[0,5,7,9,3,0,0,0,0],[9,0,0,0,2,0,7,3,0],[7,8,0,1,0,0,0,0,0],[6,0,5,2,0,8,0,0,7],[0,9,4,0,7,3,0,5,0]]
# grid=[[0,0,4,0,0,0,0,5,7],[0,0,0,0,0,0,3,9,0],[0,0,0,1,0,6,0,0,0],[1,0,5,9,0,0,0,0,0],[9,4,0,2,0,0,0,0,1],[0,0,0,0,0,3,0,0,0],[2,6,0,0,0,8,0,0,0],[0,8,0,0,0,0,7,0,0],[0,0,0,5,0,0,0,2,0]]

# array=[0,0,0,0,7,0,0,1,0,1,0,0,0,2,9,7,0,0,3,0,0,5,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,8,0,7,4,5,0,0,0,7,0,0,0,0,0,2,8,0,0,0,0,0,8,0,6,0,0,6,9,4,0,0,0,0,0,0,0,0,0,0,1,0,0,4,0]

# taking list input and making it a grid
def gridder(array):
    if array=='':
        array=input("give the array")
    else:
        grid=[]
        for i in range(len(array)-1):
            if i%9==0:
                grid.append(array[i:i+9])
        grid=np.matrix(grid)
    print("Given initial puzzle:")
    print(grid)
    return(grid)

def possible(x,y,n,grid):
    # Elements in coloumn
    for i in range(9):
        if grid[x,i]==n:
            return False
    # Elements in row
    for j in range(9):
        if grid[j,y]==n:
            return False
    # Elements in square
    x0=(x//3)*3
    y0=(y//3)*3
    for i in range (3):
        for j in range (3):
            if grid [x0+i,y0+j]==n:
                return False
    return True

def solve(grid):
    for x in range(9):
        for y in range(9):
            if grid[x,y]==0:
                for n in range(1,10):
                    if possible(x,y,n,grid):
                        grid[x,y]=n
                        solve(grid)
                        grid[x,y]=0
                return
    print('')
    print("Solved puzzle")
    print(grid)

# solve(gridder([0,0,0,0,7,0,0,1,0,1,0,0,0,2,9,7,0,0,3,0,0,5,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,8,0,7,4,5,0,0,0,7,0,0,0,0,0,2,8,0,0,0,0,0,8,0,6,0,0,6,9,4,0,0,0,0,0,0,0,0,0,0,1,0,0,4,0]))
