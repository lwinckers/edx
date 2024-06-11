import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Deep copy the domains.
        domains_copy = copy.deepcopy(self.domains)

        # For each variable get the length.
        for variable in domains_copy:
            length = variable.length
            # For each word in domains, check if length is not the same as variable length.
            # If length is not the same, remove word from domains (not from the copy).
            for word in domains_copy[variable]:
                if len(word) != length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Deep copy the domains.
        #domain_copy = copy.deepcopy(self.domains)
        
        # Set revision_made variable to False.
        revision_made = False

        # Retrieve overlapping cells for x and y.
        overlap = self.crossword.overlaps[x, y]

        # For every word in domains (for both x and y), check if there is overlap based on potentially the same letter in overlapping position.
        if overlap:

            xoverlap, yoverlap = overlap
            domains_to_remove = set()

            for xword in self.domains[x]:
                value_matched = False
                
                for yword in self.domains[y]:
                    if xword != yword and xword[xoverlap] == yword[yoverlap]:
                        value_matched = True
                        break                           # No need to check other y if there is already overlap found.

                if not value_matched:
                    domains_to_remove.add(xword) 

            if domains_to_remove:   
                self.domains[x] -= domains_to_remove       # Remove x value/word from domains if no matching value is found with y.
                revision_made = True

        return revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        if arcs is None:
            # If arcs is None, start with an initial queue of all of the arcs in the problem.
            queue = []
            
            for variable in self.crossword.variables:               # For each variable, retrieve each neighbor of that variable.
                for neighbor_variable in self.crossword.neighbors(variable):
                    queue.append((variable, neighbor_variable))     # Add all arcs to queue.
        else:
            queue = list(arcs)

        # If there are variables in the queue, pop the first combination of variables.
        while queue:
            x, y = queue.pop(0)

            if self.revise(x, y):                       # Check if revision made is True, to make them arc consistent.
                if len(self.domains[x]) == 0:           # If domain ends up empty, return False.
                    return False
                
                for neighbor in self.crossword.neighbors(x):    # Append queue with all neighbors based on X, check if neighbor is not already y.
                    if neighbor != y:
                        queue.append((neighbor, x))

        return True                                     # Return True if arc consistency is enforced and no domains are empty.

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            if variable not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for x in assignment:
            word1 = assignment[x]
            if x.length != len(word1):      # If length of word is not length of variable, return False.
                return False

            for y in assignment:
                word2 = assignment[y]
                if x != y:
                    if word1 == word2:      # If two variables have the same word, return False.
                        return False

                    overlap = self.crossword.overlaps[x, y]
                    if overlap:
                        a, b = overlap
                        if word1[a] != word2[b]:    # If there is overlap, then the letter of both words must match. Else return False.
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Get neighbors of var which are not in assignment.
        neighbors = self.crossword.neighbors(var)
        for i in assignment:
            if i in neighbors:
                neighbors.remove(i)

        result = []

        # For every value in te domain of 'var' check for overlap with neighbors.
        for val in self.domains[var]:
            n_ruled_out = 0                 # Number of ruled out to sort on later

            for neighbor_var in neighbors:
                for val2 in self.domains[neighbor_var]:                     # For every value of var's neighbor,
                    overlap = self.crossword.overlaps[var, neighbor_var]    # check overlap between var and its neighbors
                    
                    if overlap:
                        a, b = overlap
                        if val[a] != val2[b]:
                            # If there is no overlap between value of var and value of var's neighbor,
                            # then they are ruled out
                            n_ruled_out += 1
            # Append the value to the result list with number of ruled out values amond neighbors of 'val'.
            result.append([val, n_ruled_out])
        # Sort list of results based on number of ruled out values.
        result.sort(key=lambda x: x[1])

        return [i[0] for i in result]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)

if __name__ == "__main__":
    main()