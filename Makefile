# --- C.A.D.A Industrial Makefile ---
.PHONY: start push report setup discover infer audit clean validate test

# 1. Workflow Automation
start:
	git pull origin main
	docker compose up -d
	docker compose exec bitbot-dev /bin/bash

push:
	git add .
	git commit -m "$(msg)"
	git push origin main
	docker compose down

report:
	@echo "--- Daily Progress Report ---"
	@git log --since="today" --pretty=format:"* %s"

# 2. C.A.D.A Infrastructure
setup:
	@echo "Initializing environments..."
	python3 -m venv venv
	cd core/inference_swarm && cargo build --release

# 3. Discovery & Inference
discover:
	@echo "Mining ruleset..."
	python3 core/discovery_factory/engine.py --output data/manifests/latest.json

infer:
	@echo "Deploying Swarm..."
	cd core/inference_swarm && cargo run --release -- --manifest ../../data/manifests/latest.json

# 4. Forensic & QA (New Additions)
validate:
	@echo "Running Axiomatic Firewall Check..."
	python3 core/discovery_factory/constraints.py --verify data/manifests/latest.json

test:
	@echo "Running Deterministic Stress Test (1200 records)..."
	cd core/inference_swarm && cargo test --release -- --nocapture

audit:
	@echo "Verifying audit ledger integrity..."
	sha256sum logs/audit/audit_ledger.log

clean:
	rm -rf data/manifests/* logs/audit/*
	@echo "Environment sanitized."