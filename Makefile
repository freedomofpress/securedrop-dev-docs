.PHONY: docs
docs:  ## Build project documentation with live reload for editing.
	@echo "███ Building docs and watching for changes..."
	make clean && poetry run sphinx-autobuild docs/ docs/_build/html
	@echo

.PHONY: docs-lint
docs-lint:  ## Check documentation for common syntax errors.
	@echo "███ Checking for common errors..."
	@./check_errors.sh
	@echo "███ Linting documentation..."
# The `-W` option converts warnings to errors.
# The `-n` option enables "nit-picky" mode.
	@make clean && poetry run sphinx-build -Wn docs/ docs/_build/html
	@echo

.PHONY: docs-linkcheck
docs-linkcheck:  ## Check documentation for broken links.
	@make clean && poetry run sphinx-build -b linkcheck -Wn docs/ docs/_build/html
	@echo

.PHONY: pygments-css
pygments-css:  ## Generate Pygments dark theme CSS for syntax highlighting.
	@echo "███ Generating Pygments dark theme CSS..."
	@poetry run python extract_css.py lightbulb
	@echo

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%:
	@poetry run sphinx-build -M $@ docs/ docs/_build
