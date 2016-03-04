cc1=python
cc2=g++

all:
	mkdir bin
	cp ./src/parser.py ./bin/
	cc2 ./src/make_html.cpp > ./bin/make_html
	cp ./src/parser ./bin/parser
	chmod 777 ./bin/*

clean:
	rm -r ./bin	
