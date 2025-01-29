# install dependencies using uv, not pip, using pyproject.toml
install:
	@echo "Installing dependencies..."
	uv sync


# Run paper crawling job
crawl:
	@echo "Running Paper crawling job..."
	uv run backend/job.py "$$(jq -c . keywords.json)"

lint-backend:
	@echo "Running lint..."
	uv run ruff check backend

format-backend:
	@echo "Running formatting..."
	uv run ruff format backend
	uv run isort backend

format-javascript:
	@echo "Beautifying Javascript files..."
	find frontend/assets -type f -name "*.js" | xargs uv run js-beautify -r

format-css:
	@echo "Beautifying CSS files..."
	find frontend/assets -type f -name "*.css" | xargs uv run css-beautify -r
