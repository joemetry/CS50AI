import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation.
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines.
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines.
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly.
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, the player has found no mines.
        self.mines_found = set()

    def print(self):
        # Prints a text-based representation of where mines are located.
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
        # Returns True if the given cell contains a mine.
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are within one row and column of a given cell,
        not including the cell itself.
        """
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        # Checks if all mines have been flagged.
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game.
    A sentence consists of a set of board cells and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        # Returns the set of all cells in self.cells known to be mines.
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        # Returns the set of all cells in self.cells known to be safe.
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player.
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width.
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on.
        self.moves_made = set()

        # Keep track of cells known to be safe or mines.
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true.
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

    def neighbors(self, cell):
        """
        Returns the set of all cells that are neighbors of the given cell.
        """
        i, j = cell
        neighbors = set()

        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    neighbors.add((ni, nj))

        return neighbors

    def add_knowledge(self, cell, count):
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        new_sentence = Sentence(self.neighbors(cell), count)
        self.knowledge.append(new_sentence)

        # Prepare to mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
        new_safes = set()
        new_mines = set()
        for sentence in self.knowledge:
            if sentence.known_safes():
                new_safes.update(sentence.known_safes())
            if sentence.known_mines():
                new_mines.update(sentence.known_mines())

        # Mark the cells as safe or mines
        for safe_cell in new_safes:
            self.mark_safe(safe_cell)
        for mine_cell in new_mines:
            self.mark_mine(mine_cell)

        # Add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1.cells.issubset(sentence2.cells) and sentence1 != sentence2:
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(new_cells, new_count)
                    if new_sentence not in self.knowledge:
                        self.knowledge.append(new_sentence)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """    
        all_cells = set(itertools.product(range(self.height), range(self.width)))
        possible_moves = all_cells - self.moves_made - self.mines
        if possible_moves:
            return random.choice(list(possible_moves))
        return None

