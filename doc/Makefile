XSLTPROC = xsltproc

BOOK_HTML_TARGET = manual.html

BOOK_XML_SOURCE = manual.xml
BOOK_VERSION_SOURCE = version.xml
BOOK_ALL_SOURCE = *.xml

XSL_HTML = html-stylesheet.xsl
UNAME := $(shell uname)

ifeq ($(UNAME), Darwin)
export SGML_CATALOG_FILES=catalog-osx
else
export SGML_CATALOG_FILES=catalog
endif

# Book xsltproc options for HTML output
# Note: --stringparam arguments no longer go here; 
# see tools/html-stylesheet.xsl and tools/chunk-stylesheet.xsl
BOOK_HTML_XSLTPROC_OPTS = 

all: html

clean: book-clean

html: $(BOOK_HTML_TARGET)

$(BOOK_HTML_TARGET): $(BOOK_ALL_SOURCE) $(BOOK_VERSION_SOURCE)
	$(XSLTPROC) --catalogs $(BOOK_HTML_XSLTPROC_OPTS) \
           --output $(BOOK_HTML_TARGET) $(XSL_HTML) $(BOOK_XML_SOURCE)

book-clean:
	rm -f $(BOOK_HTML_TARGET)

