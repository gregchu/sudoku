# approach
given the plethora of solution approaches and the limited time, 
i chose to establish a baseline and start with the most brute force approach

backtracking and recursion
that was ~26 sec

then applied hueristics to  speed it up

view like a decision tree

Pseudocode

candidates_per_coord = {} # key is coord, val is list of potential values
for each coord, element in grid:
    if coord is empty:
        find all potential_vals for coord
        add to vals_per_coord

if vals_per_coord is empty:
    done #base case
find coord with least # of potential vals
for each val in candidates:
    if is_valid(val):
        remove_val_from_group(coord, val)

