all: print_solution

sudoku.cnf:
	./generate_sudoku.py > $@

particular_problem.cnf: sudoku.cnf start_positions
	cp $< $@
	./interpret_start_positions.py $< start_positions >> $@

solution:	particular_problem.cnf mergesat
	-./mergesat $< > $@

print_solution: sudoku.cnf solution
	./interpret_solution.py $^

.PHONY: clean

clean:
	rm -f sudoku.cnf particular_problem.cnf solution

