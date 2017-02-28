assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
diagonal_1 = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']         #local constriants for diagonal position
diagonal_2 = ['I1','H2','G3','F4','E5','D6','C7','B8','A9']         #local constriants for diagonal position 

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_1_units = dict((s, None) for s in diagonal_1)              #initial the diagonal position 1 as a dict
diagonal_2_units = dict((s, None) for s in diagonal_2)              #initial the diagonal position 2 as a dict

unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unitlist:
        naked_twins = []
        for box in unit:                        
            if (len(values[box]) == 2):     # local constraints for length ==2
                for pair in unit:
                    if values[box] == values[pair] and box != pair:     #local constraints for pair box have same value but different position
                        naked_twins.append(box)
        for naked_twin in naked_twins:
            for box in unit: 
                if box not in naked_twins:
                    #print(box)
                    values[box] = values[box].replace(values[naked_twin][0],'')     #replace the first character of the nake_twins string
                    #print (naked_twin[0])
                    #print (values[box])
                    values[box] = values[box].replace(values[naked_twin][1],'')    #replace the second character of the nake_twins string 
                    #print (naked_twin[1])
                    #print (values[box])
    return values
   
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))
    pass

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
        if box in diagonal_1_units:
            for diagonal_1_unit in diagonal_1_units:
                if diagonal_1_unit == box:                          #box will not be replaced for twice.
                    continue
                else:
                    values[diagonal_1_unit] = values[diagonal_1_unit].replace(digit,'')  #eliminate and update box 
        if box in diagonal_2_units:
            for diagonal_2_unit in diagonal_2_units:
                if diagonal_2_unit == box:
                    continue
                else:
                    values[diagonal_2_unit] = values[diagonal_2_unit].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    for digit in '123456789':
        dplaces = [box for box in diagonal_1_units.keys() if digit in values[box]]  #choose box from diagonal postion 1
        if len(dplaces) == 1:
            values[dplaces[0]] = digit                                              #do only_choice to peered box in diagonal position 1
    for digit in '123456789':
        dplaces = [box for box in diagonal_2_units.keys() if digit in values[box]]  #choose box from diagonal postion 1
        if len(dplaces) == 1:
            values[dplaces[0]] = digit                                              #do only_choice to peered box in diagonal position 2
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
    #    display(values)
    #    print('begin')
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    #    values = naked_twins(v`alues)
    #    print('naked_twins&&&&&&&&&&')
    # Choose one of the unfilled squares with the fewest possibilities
    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in boxes): 
        return values     
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    n,s = min((len(values[s]),s) for s in boxes if len(values[s])>1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
  #  display(solve(diag_sudoku_grid))
  #  solve(dia_sudoku_grid)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
