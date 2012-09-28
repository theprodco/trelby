PREFIX = $(DESTDIR)/usr

.PHONY : clean dist deb

dist: names.txt.gz dict_en.dat.gz manual.html
	python setup.py sdist

dist-osx: names.txt.gz dict_en.dat.gz manual.html
	python setup.py py2app
	ln -s ./Contents/Resources/resources dist/Trelby.app/resources
	ln -s ./lib/python2.7/src dist/Trelby.app/Contents/resources/src
	ln -s ./Contents/Resources/manual.html dist/Trelby.app/manual.html
	cp -f names.txt.gz dict_en.dat.gz LICENSE README dist/Trelby.app/
 
deb: dist
	debuild -us -uc -b

names.txt.gz: names.txt
	gzip -c names.txt > names.txt.gz

dict_en.dat.gz: dict_en.dat
	gzip -c dict_en.dat > dict_en.dat.gz

manual.html: doc/*
	make -C doc && mv doc/manual.html .

rpm: dist
	python setup.py bdist_rpm

clean:
	rm -f bin/*.pyc src/*.pyc tests/*.pyc names.txt.gz dict_en.dat.gz manual.html MANIFEST
	rm -rf build dist
	dh_clean

install: dist
	python setup.py install

install-osx: dist-osx
	cp -r dist/Trelby.app /Applications
	mkdir -p ~/Desktop/Trelby
	ln -sf /Applications/Trelby.app ~/Desktop/Trelby/Trelby.app
	cp -f names.txt.gz dict_en.dat.gz manual.html LICENSE README fileformat.txt sample.trelby ~/Desktop/Trelby
