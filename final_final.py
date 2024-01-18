import random

def generate_individual(partial_puzzle):

    puzzle = [row[:] for row in partial_puzzle]
    empty_cells = [(i, j) for i in range(9) for j in range(9) if puzzle[i][j] == 0]
    random.shuffle(empty_cells)

    numbers = list(range(1, 10))
    for (i, j) in empty_cells:
        valid_numbers = [num for num in numbers if is_valid_move(puzzle, i, j, num)]
        if valid_numbers:
            puzzle[i][j] = random.choice(valid_numbers)

    return puzzle

def is_valid_move(puzzle, row, col, num):

    for i in range(9):
        if puzzle[row][i] == num or puzzle[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if puzzle[start_row + i][start_col + j] == num:
                return False

    return True

def genetic_algorithm(partial_puzzle, population_size, generations):
  
    population = [generate_individual(partial_puzzle) for _ in range(population_size)]

    for generation in range(generations):
        population = sorted(population, key=lambda x: fitness(x, partial_puzzle))
        best_fitness = fitness(population[0], partial_puzzle)
        print(f"Jenerasyon, sudoku çözümü {generation + 1}, Uygunluk {best_fitness}")
        if best_fitness == 0:
            break

        new_population = []

        for _ in range(population_size // 2):
            parent1 = random.choice(population[: population_size // 2])
            parent2 = random.choice(population[: population_size // 2])
            child1 = crossover(parent1, parent2, partial_puzzle)
            child2 = crossover(parent1, parent2, partial_puzzle)
            new_population.extend([mutate(child1, partial_puzzle), mutate(child2, partial_puzzle)])

        population = new_population

    best_solution = sorted(population, key=lambda x: fitness(x, partial_puzzle))[0]
    return best_solution

def crossover(parent1, parent2, partial_puzzle):

    child = [row[:] for row in parent1]
    empty_cells = [(i, j) for i in range(9) for j in range(9) if partial_puzzle[i][j] == 0]
    random.shuffle(empty_cells)

    for (i, j) in empty_cells:
        if random.choice([True, False]):
            child[i][j] = parent1[i][j]
        else:
            child[i][j] = parent2[i][j]

    return child

def mutate(individual, partial_puzzle):
  
    mutated_individual = [row[:] for row in individual]
    for i in range(9):
        empty_cells = [(i, j) for j in range(9) if partial_puzzle[i][j] == 0]
        random.shuffle(empty_cells)

        for (i, j) in empty_cells[:2]:  # Mutate at most 2 cells in each row
            valid_numbers = [num for num in range(1, 10) if is_valid_move(mutated_individual, i, j, num)]
            if valid_numbers:
                mutated_individual[i][j] = random.choice(valid_numbers)
    
#print(mutated_individual)

    return mutated_individual


def fitness(puzzle, partial_puzzle):
    conflicts = 0

    for i in range(9):
        row = set(puzzle[i])
        column = set(puzzle[j][i] for j in range(9))
        block = set()

        for j in range(9):
            block_row, block_col = 3 * (i // 3), 3 * (j // 3)
            block.add(puzzle[block_row + (j // 3)][block_col + (j % 3)])

        # satırda 1-9 arası rakamların kontrolu
        if set(range(1, 10)) != row:
            conflicts += 1
            

        # sütünda 1-9 arası rakamların kontrolu
        if set(range(1, 10)) != column:
            conflicts += 1

        for i in range(9):
            if sum(puzzle[i]) != 45 or sum(puzzle[j][i] for j in range(9)) != 45:
                conflicts += 1
      

    return conflicts


def print_sudoku(puzzle):
 
    for i in range(9):
        for j in range(9):
            print(puzzle[i][j], end=" ")
        print()

if __name__ == "__main__":


    partial_sudoku1 = [
    [0, 3, 6, 0, 5, 0, 7, 9, 8],
    [0, 4, 0, 0, 3, 7, 0, 2, 0],
    [2, 0, 0, 8, 0, 1, 0, 0, 6],
    [0, 8, 0, 7, 0, 0, 2, 5, 0],
    [3, 0, 4, 0, 2, 0, 8, 0, 0],
    [0, 0, 5, 1, 0, 3, 0, 0, 4],
    [5, 1, 0, 0, 7, 6, 4, 0, 0],
    [6, 0, 2, 0, 0, 0, 0, 8, 1],
    [0, 0, 0, 5, 0, 8, 0, 7, 0],
]
    
 

    print("Çözülecek Sudoku")
    print_sudoku(partial_sudoku1)
    

    solution = genetic_algorithm(partial_sudoku1, population_size=50, generations=1000)

    print("\n Çözülen Sudoku")
    print_sudoku(solution)
