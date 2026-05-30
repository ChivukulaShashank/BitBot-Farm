FROM python:3.12-slim

# Install system tools
RUN apt-get update && apt-get install -y git make

# Create a virtual environment
RUN python -m venv /opt/venv
# Set environment variables so commands use the venv automatically
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /workspace
COPY pyproject.toml .
# Install dependencies into the venv
RUN pip install --upgrade pip && pip install -e .

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

CMD ["/bin/bash"]