FROM quay.io/pypa/manylinux2014_x86_64

# Install uv
RUN /opt/python/cp311-cp311/bin/pip install uv
ENV PATH="/root/.local/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Create directory for wheels
RUN mkdir -p /app/wheelhouse && chmod +x /app/build_wheels.sh

# Default command to build wheels
CMD ["/app/build_wheels.sh"] 
