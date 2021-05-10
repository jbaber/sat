all: print_solution

sudoku/sudoku.cnf:
	sudoku/generate_sudoku.py > $@

sudoku/particular_problem.cnf: sudoku/sudoku.cnf sudoku/start_positions
	cp $< $@
	sudoku/interpret_start_positions.py $< sudoku/start_positions >> $@

sudoku/solution:	sudoku/particular_problem.cnf mergesat
	-./mergesat $< > $@

print_solution: sudoku/sudoku.cnf sudoku/solution
	sudoku/interpret_solution.py $^

.PHONY: clean print_solution

clean:
	rm -f sudoku/sudoku.cnf sudoku/particular_problem.cnf sudoku/solution
