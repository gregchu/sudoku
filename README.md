# approach
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


