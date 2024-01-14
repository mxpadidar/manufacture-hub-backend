source_dir = src
virtualenv = .venv

cleanup:
	@find . -type d \( -path "./$(virtualenv)" -o -path "./.data" \) -prune -o -type d -name '*cache*' \
	-exec echo Removing {} \; \
	-exec rm -rf {} +
tree:
	@$(MAKE) cleanup
	@tree -a -I "$(virtualenv)|.git|.data"

run-app:
	@poetry run python ${source_dir}/main.py

dcup:
	@docker compose up -d

dcdown:
	@docker compose down

pre-commit:
	@git add .
	@pre-commit run -a

pytest:
	@pytest tests/ -v

commit:
	@read -p "Enter commit message: " message; \
	git add .; \
	git commit -m "$$message"; \
	git push -u origin master

revision:
	@read -p "Enter revision message: " message; \
	alembic revision --autogenerate -m "$$message"

.PHONY: cleanup tree run-app dcup dcdown pre-commit pytest commit revision
