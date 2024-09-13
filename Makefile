# Variables
IMAGE_NAME = swiss-clock-alpine
CONTAINER_NAME = swiss-clock-container
TAR_NAME = swiss-clock-alpine.tar

# Default target
all: build run

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container
run:
	docker run --name $(CONTAINER_NAME) -v $(PWD)/output:/app/output $(IMAGE_NAME)

# Remove the container
clean:
	docker rm -f $(CONTAINER_NAME) || true

# Remove the image
clean-image:
	docker rmi $(IMAGE_NAME) || true

# Save the Docker image to a tar file
save-image:
	docker save $(IMAGE_NAME) > $(TAR_NAME)

# Load the Docker image from the tar file
load-image:
	docker load < $(TAR_NAME)

# Full cleanup (container, image, and tar file)
clean-all: clean clean-image
	rm -f $(TAR_NAME)

# Build, run, clean up, and save image to tar
complete: build run clean save-image

.PHONY: all build run clean clean-image save-image load-image clean-all complete
