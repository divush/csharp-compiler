all:
	rm -r ./bin	
	mkdir bin
	cp ./src/parser.py ./bin/
	g++ ./src/html.cpp > ./bin/make_html
	cp ./src/parser ./bin/parser
	chmod 777 ./bin/*
	chmod +x ./bin/*

clean:
	rm -r ./bin	
