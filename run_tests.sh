#!/bin/bash

# Build Docker Compose services without cache
docker compose -f docker-compose.test.yml build --no-cache

# Start Docker Compose services
docker compose -f docker-compose.test.yml up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 30

# Remove tests/config.json file if it exists
if [ -f "tests/config.json" ]; then
    rm tests/config.json
fi

# Run tests
pytest tests/

# Remove tests/config.json file if it exists
if [ -f "tests/config.json" ]; then
    rm tests/config.json
fi

# Capture the exit code of pytest
TEST_EXIT_CODE=$?

# Stop Docker Compose services
docker compose -f docker-compose.test.yml down

# Exit with the same code as pytest
exit $TEST_EXIT_CODE