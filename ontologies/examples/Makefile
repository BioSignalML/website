all: drug.rdf physiobank.rdf unit.rdf sleep.rdf

%.rdf: %.ttl
	rapper -i turtle $< -o rdfxml > $@
