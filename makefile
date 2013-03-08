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
	TestWCDB1.py >& TestWCDB1.out

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
	rm -f *.piece





Mallory Farr	malloryfarr@austin.rr.com^t(512)9132887^t@Malloryfarr 
Alex Leonard	alexjleonard@gmail.com^t(214) 733-0058^t@ajl2265 
Wilson Bui	davo_letows@utexas.edu^t(832) 475-0125 @Davoletows 
Geovanni Monge	gsm@utexas.edu^t(281) 608-6121 @geosmon 
Taylor McCaslin^tTaylor4484@gmail.com^t(903) 574-1351 @Taylor4484
Holly Hatfield^th.hatfield@utexas.edu^t(469) 826-6454 @hjh558 
Daniel Enrlich^tDaniel.ehrlich1@gmail.com^t(281) 636-3178^t@danielehrlich^tAUDITOR


	rm -f *.tmp