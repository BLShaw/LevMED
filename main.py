import sys

# Set stdout to UTF-8 for Windows Unicode support
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

#import colorama
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("Error: 'colorama' library is required.")
    print("Please run: pip install colorama")
    sys.exit(1)

def get_arrow(i, j, parents):
    # parents is a list of 'DIAG', 'UP', 'LEFT'
    arrows = []
    if 'DIAG' in parents: arrows.append("↖")
    if 'UP' in parents: arrows.append("↑")
    if 'LEFT' in parents: arrows.append("←")
    return "".join(arrows)

def main():
    print(f"{Fore.CYAN}Minimum Edit Distance Calculator (Levenshtein){Style.RESET_ALL}")
    
    # Cost Configuration
    print("\nSelect Cost Configuration:")
    print("1. Standard Levenshtein (Match=0, Sub=1, Ins=1, Del=1)")
    print("2. Alternative (Match=0, Sub=2, Ins=1, Del=1)")
    print("3. Custom")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    match_cost = 0
    sub_cost = 1
    ins_cost = 1
    del_cost = 1
    
    if choice == '2':
        sub_cost = 2
    elif choice == '3':
        try:
            match_cost = int(input("Enter Match Cost (default 0): ") or 0)
            sub_cost = int(input("Enter Substitution Cost (default 2): ") or 2)
            ins_cost = int(input("Enter Insertion Cost (default 1): ") or 1)
            del_cost = int(input("Enter Deletion Cost (default 1): ") or 1)
        except ValueError:
            print("Invalid input. Using defaults (Sub=2, Ins=1, Del=1).")
            match_cost = 0; sub_cost = 2; ins_cost = 1; del_cost = 1
    else:
        # Default to Standard (1)
        pass

    print(f"\nUsing Costs -> Match: {match_cost}, Sub: {sub_cost}, Ins: {ins_cost}, Del: {del_cost}\n")

    source_input = input("Enter Source Word: ").strip()
    target_input = input("Enter Target Word: ").strip()

    #"Source" is rows, "Target" is columns.
    source = "#" + source_input
    target = "#" + target_input
    
    n = len(source)
    m = len(target)
    
    # Initialize matrices
    dist = [[0] * m for _ in range(n)]
    # To store the parent direction for arrows and traceback
    directions = [[[] for _ in range(m)] for _ in range(n)]
    
    # Base cases
    # Row 0 (Target creation via Insertions)
    for j in range(m):
        dist[0][j] = j * ins_cost
        if j > 0:
            directions[0][j] = ['LEFT']
            
    # Col 0 (Source deletion)
    for i in range(n):
        dist[i][0] = i * del_cost
        if i > 0:
            directions[i][0] = ['UP']
            
    # Calculations
    print("\n" + "="*40 + "\n")
    
    for i in range(1, n):
        for j in range(1, m):
            # Determine match
            char_source = source[i]
            char_target = target[j]
            is_match = (char_source == char_target)
            
            # Calculate costs for each move
            # Diagonal (Match or Sub)
            base_diag = dist[i-1][j-1]
            cost_diag = base_diag + (match_cost if is_match else sub_cost)
            
            # Up (Deletion)
            base_up = dist[i-1][j]
            cost_up = base_up + del_cost
            
            # Left (Insertion)
            base_left = dist[i][j-1]
            cost_left = base_left + ins_cost
            
            # Find Min
            current_cost = min(cost_diag, cost_up, cost_left)
            dist[i][j] = current_cost
            
            # Determine parents
            possible_parents = []
            if cost_diag == current_cost: possible_parents.append('DIAG')
            if cost_up == current_cost: possible_parents.append('UP')
            if cost_left == current_cost: possible_parents.append('LEFT')
            
            directions[i][j] = possible_parents
            
            # Explanation strings
            op_cost_diag = match_cost if is_match else sub_cost
            
            # Generate Output Text matching the template style but adapting to custom costs
            print(f"{Fore.YELLOW}Sub-problem:{Style.RESET_ALL} {source[:i+1]} ➔ {target[:j+1]}.")
            print(f"Intersecting cell: A[{i}, {j}]")
            print(f"Same intersecting characters? {'YES' if is_match else 'NO'}.")
            
            # Display format: Min(A[..] + c, ...)
            print(f"Cost(A[{i}, {j}])       = Min(")
            print(f"                               A[{i-1}, {j-1}] + {op_cost_diag},  (Diag)")
            print(f"                               A[{i-1}, {j}] + {del_cost},  (Up)")
            print(f"                               A[{i}, {j-1}] + {ins_cost}   (Left)")
            print(f"                             )")
            
            # Values
            print(f"                             = Min(")
            print(f"                               {base_diag} + {op_cost_diag},")
            print(f"                               {base_up} + {del_cost},")
            print(f"                               {base_left} + {ins_cost}")
            print(f"                             )")
            print(f"                             = {current_cost}\n")

    # Traceback
    path_cells = set()
    curr_i, curr_j = n - 1, m - 1
    path_cells.add((curr_i, curr_j))
    
    while curr_i > 0 or curr_j > 0:
        parents = directions[curr_i][curr_j]
        
        if 'DIAG' in parents:
            curr_i -= 1
            curr_j -= 1
        elif 'UP' in parents:
            curr_i -= 1
        elif 'LEFT' in parents:
            curr_j -= 1
        else:
            break
        path_cells.add((curr_i, curr_j))

    # Result
    print(f"Result:\n")
    print(f"The distance between two strings {source_input} and {target_input} is {dist[n-1][m-1]}.\n")
    
    # Visual Table
    print(f"{Fore.MAGENTA}Final Table:{Style.RESET_ALL}")
    
    # Header Row
    row_str = "      " 
    for j in range(m):
        char = target[j]
        row_str += f"  {char}   "
    print(row_str)
    
    for i in range(n):
        char = source[i]
        row_str = f"  {char}   "
        
        for j in range(m):
            val = dist[i][j]
            arrow_s = ""
            if not (i == 0 and j == 0):
                p = directions[i][j]
                if 'DIAG' in p: arrow_s = "↖"
                elif 'UP' in p: arrow_s = "↑"
                elif 'LEFT' in p: arrow_s = "←"
            
            cell_str = f"{arrow_s}{val}" 
            cell_str = f"{cell_str:>4} " 
            
            if (i, j) in path_cells:
                cell_str = Back.LIGHTBLACK_EX + Fore.WHITE + cell_str + Style.RESET_ALL
            else:
                cell_str = Fore.CYAN + cell_str + Style.RESET_ALL
                
            row_str += cell_str
            
        print(row_str)

if __name__ == "__main__":
    main()
