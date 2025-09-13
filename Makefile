.PHONY: test clean

test:
    pytest tests/

clean:
    find . -type d -name "__pycache__" -exec rm -r {} +
