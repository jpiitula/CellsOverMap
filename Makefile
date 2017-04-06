all: example/numerot.html

example/numerot.html: src/makecellomap.py src/cellomap.html src/cellomap.css src/cellomap.js test/numerot.json
	mkdir --parents tmp
	python3 src/makecellomap.py test/numerot.json --xmax=10 --ymax=10 > $@
