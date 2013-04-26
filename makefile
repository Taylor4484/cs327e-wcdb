all:
	make run
	make test

diff:
	RunWCDB3.py < RunWCDB3.in.xml > RunWCDB3.tmp
	diff RunWCDB3.out.xml RunWCDB3.tmp
	rm RunWCDB3.tmp

doc:
	pydoc -w WCDB3

log:
	git log > WCDB3.log

run:
	RunWCDB3.py < RunWCDB3.in.xml

test:
	TestWCDB3.py

turnin-list:
	turnin --list hychyc07 cs327epj5

turnin-submit:
	turnin --submit hychyc07 cs327epj5 WCDB3.zip

turnin-verify:
	turnin --verify hychyc07 cs327epj5

zip:
	zip -r WCDB3.zip makefile                    \
	RunWCDB3.in.xml RunWCDB3.py RunWCDB3.out.xml \
	TestWCDB3.py TestWCDB3.out                   \
	WCDB3d.html WCDB3q.html WCDB3.log WCDB3.py   \
	WCDB3p.pdf WCDB3u.pdf WCDB3q.sql

clean:
	rm -f *.pyc
	rm -f *.tmp