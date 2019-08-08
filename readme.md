# Usage

```
docker compose
python solver.py sudoku.txt
```
Expected output: `sudoku.log`

# Approaches

In the large space of potential approaches for Sudoku solvers, I started with the simplest, non-exhaustive approach, and measured the performance. Then, by applying a single heuristic to this approach, I was able to reach a satisfactory level of performance.

Brute-force wasn't an option as a first approach since the complexity is `O(n^m)`, where `n` is the number of potential values per cell (9) and `m` is the number of unsolved cells.

## 1. Depth first search with backtracking

### **Algorithm:**
1. Find the first unsolved cell (in raster-scan order)  
    a. If we cannot find an unsolved cell, the board is solved (base case)
2. For each candidate (1-9)  
    a. If candidate is valid (does not break Sudoku rules), assign that cell with candidate, and return (recurse) to step 1.  
3. If no candidates in step 2) are valid, backtrack up the decision tree and try a new candidate for the previous node

### **Pseudocode:**
```
func solve(board):
    coordinate = find_first_unsolved_cell(board)
    if no coordinate exists:
        return True
    
    for each candidate:
        if is_valid(candidate):
            board[coordinate] = candidate_value
            if solve(board):
                return True
            board[coordinate] = UNSOVLVED_VALUE
    return False
```

### **Results**
This solved the 50 sudoku boards in ~25 seconds on an 2015 Intel Core i7.

## 2. DFS with backtracking + heuristic

If we depict this depth first search traversal of a Sudoku board as an N-ary decision tree, the first unsolved cell is the root node, and each candidate can be represented as a child node. In approach 1), we arbitrarily chose to solve the unsolved cells in raster-scan order. 

### **Hueristic:**

If we precompute **VALID\*** candidates for each unsolved cell, instead of choosing unsolved cells in raster-scan order, we can choose to solve unsolved cells in order of increasing # of valid candidates.

This heuristic significantly constrains the search space. For example, if we choose an unsolved cell with 5 candidates, there are 5 different DFS paths available, whereas if we choose an unsolved cell with 2 candidates, there are only 2 different DFS paths available.

### **Algorithm:**

0. For each unsolved cell, compute the set of valid\* candidates and store this in a `dict`

Then, the algorithm is the same as in Approach 1 except for a couple details (bolded):

1. Find the first unsolved cell **(with the least # of valid candidates that were precomputed in step 0.)**  
    a. If we cannot find an unsolved cell, the board is solved (base case)
2. For each candidate **(from the precomputed list of valid candidates)**  
    a. If candidate is valid (does not break Sudoku rules  **and does not cause peers to have no valid candidates\****), assign that cell with candidate, and return (recurse) to step 1.  
3. If no candidates in step 3) are valid, backtrack up the decision tree and try a new candidate for the previous node **and put back valid candidates into `dict`**

Footnotes/elaboration:

\* How we define a **valid** candidate:

A valid candidate is a subset of all candidates (1-9) that does not break the rules of Sudoku (no other # in the row, column, or box)

\** 2.a. "and does not cause peers to have no valid candidates": 

When we select a candidate for a cell, we can update the list of valid candidates for all its [peers](http://sudopedia.enjoysudoku.com/Peer.html). If for any peer, the list of valid candidates is updated to None, we've made an error and must backtrack.


### **Pseudocode:**
```
valid_candidates = precompute_valid_candidates(board)   <-

func solve(board, valid_candidates):
    coordinate = find_first_unsolved_cell(board)
    if no coordinate exists:
        return True
    
    for each candidate for that coordinate:
        remove coordinate from valid_candidates         <-
        remove candidate from peers                     <-
        if is_valid_removal(candidate):                 <-
            board[coordinate] = candidate_value
            if solve(board):
                return True

            board[coordinate] = UNSOVLVED_VALUE
            put back coordinate into valid_candidates   <-
            put back candidate into peers               <-
    return False        
```

I've added `<-` at the end of each line that is a modification to Approach 1.

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


