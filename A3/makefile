all:	
	mkdir bin
	cp src/parser.py bin/
	cp src/lexer.py bin/
	g++ src/html.cpp -o bin/make_html
	cp src/parser bin/parser
	chmod 777 bin/*
	chmod +x bin/*

clean:
	rm -r bin/
	rm for_tree.txt output.txt out.txt parser.out parser.txt parsetab.py right_derivation.html errors.txt
