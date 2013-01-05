all: drug.rdf physiobank.rdf unit.rdf

%.rdf: %.ttl
	rapper -i turtle $< -o rdfxml > $@
