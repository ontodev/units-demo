build:
	mkdir -p $@

build/si_input.tsv: | build
	curl -L -o $@ "https://docs.google.com/spreadsheets/d/1AlKZIauwtQNg49ujaoD4OL_kTs1Is0-NlEqTvoR2a_o/export?format=tsv&gid=214313365"

resources/si_input.json: build/si_input.tsv
	 tail -n +2 $< | \
	 cut -f1-2 | \
	 jq --raw-input --slurp 'split("\n") | map(split("\t")) | . [0:-1] | map({"id": .[0], "label": .[1]})' > $@

.PHONY: refresh_json
refresh_json:
	rm build/si_input.tsv
	make build/si_input.tsv
	make resources/si_input.json
