#!/bin/bash

echo "🌸 Starting Flower - Visual Flow Builder"
echo "========================================"

# Build and start all services
docker-compose up --build -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🐰 RabbitMQ Management: http://localhost:15672"
echo ""
echo "🔑 Super Admin Login:"
echo "   Email: admin@flower.com"
echo "   Password: admin123"
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"