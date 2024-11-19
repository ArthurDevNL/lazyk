FROM quay.io/pypa/manylinux2014_x86_64

# Install poetry
RUN curl -sSL https://install.python-poetry.org | /opt/python/cp310-cp310/bin/python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Create directory for wheels
RUN mkdir -p /app/wheelhouse && chmod +x /app/build_wheels.sh

# Default command to build wheels
CMD ["/app/build_wheels.sh"] 