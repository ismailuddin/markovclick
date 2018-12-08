python_version_major := $(word 1,${python_version_full})

.PHONY: build_docs serve_docs

init: 	
	pip install -r requirements.txt
test:	
	pytest
build_docs:
	$(MAKE) -C docs html
serve_docs:
ifeq (python_version_major, 2)
	cd docs/_build/html && python -m SimpleHTTPServer
else
	cd docs/_build/html && python -m http.server
endif	
