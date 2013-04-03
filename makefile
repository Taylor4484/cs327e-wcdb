all:
	make run
	make test

diff:
	RunWCDB2.py < RunWCDB2.in.xml > RunWCDB2.tmp
	diff RunWCDB2.out.xml RunWCDB2.tmp
	rm RunWCDB2.tmp

doc:
	pydoc -w WCDB2

log:
	git log > WCDB2.log

run:
	python RunWCDB2.py < RunWCDB2.in.xml > output.tmp

test:
	python TestWCDB2.py

turnin-list:
	turnin --list hychyc07 cs327epj4

turnin-submit:
	turnin --submit hychyc07 cs327epj4 WCDB2.zip

turnin-verify:
	turnin --verify hychyc07 cs327epj4

zip:
	zip -r WCDB2.zip makefile                                       \
	RunWCDB2.in.xml RunWCDB2.py RunWCDB2.out.xml                    \
	TestWCDB2.py TestWCDB2.out                                      \
	WCDB2.html WCDB2.log WCDB2.pdf WCDB2.py WCDB2.xml WCDB2.xsd.xml

clean:
	rm -f *.pyc
	rm -f *.tmp