all2: print_schedule_solution

all: print_sudoku_solution

sudoku/sudoku.cnf:
	sudoku/generate_sudoku.py > $@

schedule/schedule.cnf: schedule/config.json
	schedule/generate_schedule.py $< > $@

sudoku/particular_problem.cnf: sudoku/sudoku.cnf sudoku/start_positions
	cp $< $@
	sudoku/interpret_start_positions.py $< sudoku/start_positions >> $@

schedule/particular_problem.cnf: schedule/schedule.cnf schedule/other_conditions
	cp $< $@
	schedule/interpret_other_conditions.py $< schedule/other_conditions >> $@

sudoku/solution:	sudoku/particular_problem.cnf mergesat
	-./mergesat $< > $@

schedule/solution: schedule/particular_problem.cnf mergesat
	-./mergesat $< > $@

print_sudoku_solution: sudoku/sudoku.cnf sudoku/solution
	sudoku/interpret_solution.py $^

print_schedule_solution: schedule/temp.html
	elinks --dump $^

schedule/temp.html: schedule/schedule.cnf schedule/solution schedule/config.json
	schedule/interpret_solution.py $^ > $@

.PHONY: clean print_sudoku_solution print_schedule_solution

clean:
	rm -f sudoku/sudoku.cnf */particular_problem.cnf */solution schedule/schedule.cnf schedule/temp.html
