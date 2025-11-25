# LevMED

This program calculates the Minimum Edit Distance (also known as Levenshtein distance) between two input strings. It dynamically computes the distance using a table, provides a detailed step-by-step breakdown of each cell's calculation, and visualizes the final distance matrix with a shaded traceback path and operation arrows. The program supports configurable costs for insertion, deletion, and substitution operations.

## Features
-   **Dynamic Programming Table:** Computes and displays the full dynamic programming table.
-   **Detailed Calculation Steps:** For each cell in the table, it shows the by  calculation, including the contributing neighboring cells and their associated costs.
-   **Configurable Costs:** Choose between standard Levenshtein costs, a custom set of costs, or an alternative set of costs (Sub=2, Ins/Del=1).
-   **Visual Traceback:** Highlights the optimal path through the distance matrix with shaded cells.
-   **Operation Arrows:** Displays arrows within each cell to indicate the optimal preceding operation (Substitution/Match, Deletion, Insertion).
-   **Unicode Support:** Optimized for display in terminals, including Windows.

## Installation

1.  **Python:** Ensure you have Python (3.6 or newer recommended) installed on your system.
2.  **Colorama:** This program uses the `colorama` library for colored terminal output. Install it using pip:
    ```bash
    pip install colorama
    ```

## How to Run

1.  Clone this repo.
    ```bash
    git clone https://github.com/BLShaw/LevMED
    cd LevMED
4.  Run the script using Python:
    ```bash
    python main.py
    ```
5.  Follow the on-screen prompts to choose your desired cost configuration and enter the source and target words.

## Cost Options

When you run the program, you will be presented with the following cost configuration options:

1.  **Standard Levenshtein (Match=0, Sub=1, Ins=1, Del=1)**
    *   This is the most common definition of Levenshtein distance, where all edit operations (substitution, insertion, deletion) cost 1.
2.  **Alternative (Match=0, Sub=2, Ins=1, Del=1)**
    *   This option applies a substitution cost of 2, while insertion and deletion costs remain at 1.
3.  **Custom**
    *   Allows you to define your own integer costs for match, substitution, insertion, and deletion.

## Example Usage

Here's an example of how to use the program to compute the distance between "kitten" and "sitting" using **Standard Levenshtein** costs:

```
$ main.py

Minimum Edit Distance Calculator (Levenshtein)

Select Cost Configuration:
1. Standard Levenshtein (Match=0, Sub=1, Ins=1, Del=1)
2. Alternative (Match=0, Sub=2, Ins=1, Del=1)
3. Custom
Enter choice (1, 2, or 3): 2

Using Costs -> Match: 0, Sub: 2, Ins: 1, Del: 1

Enter Source Word: kitten
Enter Target Word: sitting

# ... (Detailed step-by-step calculations will be printed here) ...

Result:

The distance between two strings kitten and sitting is 3.

Final Table:
      #     s     i     t     t     i     n     g   
  #      0   ←1   ←2   ←3   ←4   ←5   ←6   ←7   ←8   
  k     ↑1   ↖1   ←2   ←3   ←4   ←5   ←6   ←7   ←8   
  i     ↑2   ↑2   ↖1   ←2   ←3   ←4   ←5   ←6   ←7   
  t     ↑3   ↑3   ↑2   ↖1   ←2   ←3   ←4   ←5   ←6   
  t     ↑4   ↑4   ↑3   ↑2   ↖1   ←2   ←3   ←4   ←5   
  e     ↑5   ↑5   ↑4   ↑3   ↑2   ↖2   ←3   ←4   ←5   
  n     ↑6   ↑6   ↑5   ↑4   ↑3   ↑3   ↖2   ←3   ←4   

```
*(Note: The full calculation steps and colored output will be visible in your terminal when you run the script.)*
