all:
	make run
	make test

diff:
	RunWCDB1.py < RunWCDB1.in.xml > RunWCDB1.tmp
	diff RunWCDB1.out.xml RunWCDB1.tmp
	rm RunWCDB1.tmp

doc:
	pydoc -w WCDB1

log:
	git log > WCDB1.log

run:
	RunWCDB1.py < RunWCDB1.in.xml

test:
	TestWCDB1.py

turnin-list:
	turnin --list hychyc07 cs327epj3

turnin-submit:
	turnin --submit hychyc07 cs327epj3 WCDB1.zip

turnin-verify:
	turnin --verify hychyc07 cs327epj3

zip:
	zip -r WCDB1.zip makefile                             \
	RunWCDB1.in.xml RunWCDB1.py RunWCDB1.out.xml          \
	TestWCDB1.py TestWCDB1.out                            \
	WCDB1.html WCDB1.log WCDB1.py WCDB1.xml WCDB1.xsd.xml

clean:
	rm -f *.pyc
	rm -f *.tmp