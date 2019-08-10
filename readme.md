# Usage

```
sh docker_build.sh
python solver.py sudoku.txt
```
Expected output: `sudoku.log`

# Approaches

In the large space of potential approaches for Sudoku solvers, I started with the simplest, non-exhaustive approach, and measured the performance. Then, by applying a single Sudoku-specific heuristic to this approach, I was able to reach a satisfactory level of performance.

Brute-force wasn't an option as a first approach since the complexity is `O(n^m)`, where `n` is the number of possible values per cell (9) and `m` is the number of unsolved cells.

## 1. Depth first search with backtracking

### **Algorithm:**
1. Find the first unsolved cell (in raster-scan order)  
    a. If we cannot find an unsolved cell, the board is solved (base case)
2. For each possible value (1-9)  
    a. If value is valid (does not break Sudoku rules), assign that cell with value, and return (recurse) to step 1.  
3. If no values in step 2) are valid, undo the value assignment, backtrack up the tree and try a new value for the previous node

### **Pseudocode:**
```
func solve(board):
    pos = find_unsolved_cell(board)
    if no pos exists:
        return True
    
    for each value:
        if is_valid(board, pos, value):
            board[pos] = value
            if solve(board):
                return True
        undo(board[pos])
    return False
```

### **Results**
This solved the 50 sudoku boards in ~25 seconds on an 2015 Intel Core i7.

## 2. DFS with backtracking + heuristic

All DFS can be interpreted as traversal through an N-ary tree. In our case, the first unsolved cell is the root node, and each possible value can be represented as a child node. 

### **Hueristic:**

In approach 1), we arbitrarily chose to solve the unsolved cells in raster-scan order. If we precompute the set of *possible* values for each unsolved cell that follows Sudoku rules, we can choose to continuously solve unsolved cells with the least # of possible values.

This heuristic significantly constrains the search space. For example, if we choose an unsolved cell with 6 possible values, there are 6 child nodes for DFS to initiate traversal, whereas if we choose an unsolved cell with 2 possible values, there are only 2 different DFS paths available. This is also known as the branching factor of the tree.

### **Algorithm:**

0. For each unsolved cell, compute the set of possible values and store this in a `map`. By precomputing candidates, we can track unsolved cells not by the unsolved value at the start but by if it exists in the `map`.

Then, the algorithm is the same as in Approach 1 except for a couple details (bolded):

1. Find the first unsolved cell **(with the least # of possible values that were precomputed in step 0.)**  
    a. If we cannot find an unsolved cell, the board is solved (base case)
2. For each value **(from the precomputed list)**  
    a. If value is valid (does not break Sudoku rules  **and does not cause peers to have no possible values left\***), assign that cell with that value, and return (recurse) to step 1.  
3. If no values in step 3) are valid, backtrack up the decision tree and try a new value for the previous node **and put back possible values into `map`**

\* 2.a. "and does not cause peers to have no possible values left": 

When we select a value for a cell, we can update the list of possible values for all its [peers](http://sudopedia.enjoysudoku.com/Peer.html). If for any peer, the list of possible values is updated to None, we've made an error and must backtrack.

### **Pseudocode:**
```
values = precompute_possible_values(board)              <-

func solve(board, values):
    pos = find_unsolved_cell(board)                     <-
    if no pos exists:
        return True
    
    for each value:
        if is_valid(board, pos, value):                 <-
            board[pos] = value
            if solve(board):
                return True

        undo(board[pos])                            <-
    return False        
```

I've added `<-` at the end of each line that is a modification to Approach 1. The overall structure of the algorithm remains the same, but there are modifications of how these methods are implemented.

### **Results**

Hardware: 2015 Intel Core i7

Min, max, average, std


### **Assumptions**
* input file format of `sudoku.txt`



given the plethora of solution approaches and the limited time, 
i chose to establish a baseline and start with the most brute force approach

backtracking and recursion
that was ~26 sec

then applied hueristics to  speed it up

view like a decision tree

Pseudocode

candidates_per_coord = {} # key is coord, val is list of potential values
for each cell in grid:
    if cell is unsolved:
        find all candidates for cell
        add to candidates_per_coord

solve_sudoku(board)

_solve_with_candidates(board, candidates_per_coord)
    if candidates_per_coord is empty:
        return True #base case
    find coord with least # of potential vals
    for each candidate in candidates:
        if is_valid_candidate(candidate): #checks peers
            if (_solve_with_candidates(board, candidates_per_coord))
                return True ??
        put_back_candidate_in_peers
    return False    

is_valid_candidate(coord, candidate,)
    check_self
    check_peers

check_self()
    go through all peers and make sure no conflicts

check_peers()
    go through all peers, see if candidate


            for each peer in peers:
                if candidates_per_coord[peer_coord] is empty:
                    mistake made, put back val in peer
                else:
                    remove_val_from_group(coord, val)
            if any peers now have no candidates, we've made a mistake
            if 


