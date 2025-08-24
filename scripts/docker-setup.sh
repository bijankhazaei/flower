#!/bin/bash

# Flower Docker Setup Script

set -e

echo "🌸 Setting up Flower development environment..."

# Create logs directory
mkdir -p logs

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Build and start services
echo "🐳 Building and starting Docker services..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

echo "✅ Flower development environment is ready!"
echo ""
echo "🌐 Access points:"
echo "  - Flower API: http://localhost:8000"
echo "  - RabbitMQ Management: http://localhost:15672 (flower/flower)"
echo "  - PostgreSQL: localhost:5432 (flower/flower/flower)"
echo "  - Redis: localhost:6379"
echo ""
echo "📋 Useful commands:"
echo "  - View logs: docker-compose logs -f flower"
echo "  - Stop services: docker-compose down"
echo "  - Rebuild: docker-compose up --build"