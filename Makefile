# BitBot-Farm Automation

# 1. Start the day: Sync, build, and enter
start:
	git pull origin main
	docker compose up -d
	docker compose exec bitbot-dev /bin/bash

# 2. End the day: Save work and tear down
# Usage: make push msg="your message here"
push:
	git add .
	git commit -m "$(msg)"
	git push origin main
	docker compose down

# 3. Generate your end-of-day progress report
report:
	@echo "--- Daily Progress Report ---"
	@git log --since="today" --pretty=format:"* %s"