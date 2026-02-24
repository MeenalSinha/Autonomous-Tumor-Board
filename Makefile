.PHONY: help install test run-ui run-api clean format lint

help:
	@echo "Autonomous Tumor Board - Available Commands"
	@echo ""
	@echo "  make install     Install dependencies"
	@echo "  make test        Run test suite"
	@echo "  make run-ui      Start Streamlit UI"
	@echo "  make run-api     Start FastAPI backend"
	@echo "  make clean       Remove generated files"
	@echo "  make format      Format code with black"
	@echo "  make lint        Run code quality checks"
	@echo ""

install:
	pip install -r requirements.txt

test:
	python test_system.py

run-ui:
	streamlit run app.py

run-api:
	uvicorn api:app --reload

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -f data/outputs/*.json
	rm -f data/outputs/*.pdf

format:
	black agents/ models/ orchestrator/ utils/ app.py api.py test_system.py

lint:
	python -m py_compile agents/*.py
	python -m py_compile models/*.py
	python -m py_compile orchestrator/*.py
	python -m py_compile utils/*.py
