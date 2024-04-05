import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # You are only sure about the cells being mines if the count for the sentence equals the number of cells (and count is > 0).
        # Otherwise you are not sure. I.e. {A,B} = 1 either one of the two is a mine. If {A,B} = 2 you know both are mines.
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the count for a certain set of cells equals 0, then all those cells do not contain a mine.
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If cell is in set of cells, but is known to be a mine, then remove from set of cells.
        # Decrease counter for number of mines in set of cells. Because you took out a cell that is known to be a mine.
        for cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If cell is in set of cells, but is known to be safe, then remove from set of cells.
        # However, do not decrease counter for number of mines in set of cells.
        for cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # The function should mark the cell as one of the moves made in the game.
        self.moves_made.add(cell)
        # The function should mark the cell as a safe cell, updating any sentences that contain the cell as well.
        self.mark_safe(cell)

        # The function should add a new sentence to the AI’s knowledge base, 
        # based on the value of cell and count, to indicate that count of the cell’s neighbors are mines. 
        # Be sure to only include cells whose state is still undetermined in the sentence.
    
    def return_surrounding_cells(self, cell):   
        i, j = cell
        surrounding_cells = set()

        # Iterate over the neighboring cells.
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                # Exclude the cell itself.
                if (x, y) != (i, j):
                    # Check if the cell is within the board boundaries.
                    if 0 <= x < self.height and 0 <= y < self.width:
                        surrounding_cells.add((x, y))

        return surrounding_cells


        # If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so.

        # If, based on any of the sentences in self.knowledge, new sentences can be inferred (using the subset method described in the Background), 
        # then those sentences should be added to the knowledge base as well.
        
        # Note that any time that you make any change to your AI’s knowledge, it may be possible to draw new inferences that weren’t possible before. 
        # Be sure that those new inferences are added to the knowledge base if it is possible to do so.

        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # make_safe_move should return a move (i, j) that is known to be safe.
        # The move returned must be known to be safe, and not a move already made.
        # If no safe move can be guaranteed, the function should return None.
        # The function should not modify self.moves_made, self.mines, self.safes, or self.knowledge.
        self.safe_move = set()

        for cells in self.safes:
            if cells != self.moves_made and cells != self.mines:
                self.safe_move.add(cells)

        if self.safe_move:
            return random.choice(list(self.safe_move))
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # make_random_move should return a random move (i, j).

        # This function will be called if a safe move is not possible: if the AI doesn’t know where to move, it will choose to move randomly instead.
        # The move must not be a move that has already been made.
        # The move must not be a move that is known to be a mine.
        # If no such moves are possible, the function should return None.
        self.random_move = set()

        self.spaces_left = (self.height * self.width) - (len(self.moves_made) + len(self.mines))
        if self.spaces_left == 0:
            return None

        if not self.safes and self.spaces_left > 0:
            for i in range(0, self.height):
                for j in range(0, self.width):
                    if (i ,j) not in self.moves_made and (i, j) not in self.mines:
                        self.random_move.add((i, j))

        return random.choice(list(self.random_move))
