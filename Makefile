# Start MySQL Server on macOS
start-mysql:
	@echo "Starting MySQL server..."
	brew services start mysql

# Stop MySQL Server
stop-mysql:
	@echo "Stopping MySQL server..."
	brew services stop mysql

# Restart MySQL Server
restart-mysql:
	@echo "Restarting MySQL server..."
	brew services restart mysql

# Check MySQL Server Status
status-mysql:
	brew services list | grep mysql

# Run Django/Flask/FastAPI server
runserver:
	python manage.py runserver

# Start MySQL and App Server
start:
	make start-mysql && make runserver

# Stop everything
stop:
	make stop-mysql