# Variables
IMAGE_NAME = showtime
CONTAINER_NAME = showtime
TAR_NAME = showtime.tar
TAG=latest 

# Default target
all: build run

# Build the Docker image
build:
	docker build --platform linux/amd64 -t $(IMAGE_NAME):$(TAG) .

# Run the container
run:
	docker run --name $(CONTAINER_NAME) -v $(PWD)/output:/app/output $(IMAGE_NAME):$(TAG)

# Remove the container
clean: clean-image
	-docker rm -f $(CONTAINER_NAME) || true


# Remove the image
clean-image:
	-docker rmi $(IMAGE_NAME) || true

# Save the Docker image to a tar file
save:
	docker save $(IMAGE_NAME):$(TAG) > $(TAR_NAME)

# Load the Docker image from the tar file
load:
	docker load < $(TAR_NAME)

# Full cleanup (container, image, and tar file)
clean-all: clean clean-image
	rm -f $(TAR_NAME)

# Build, run, clean up, and save image to tar
complete: build run clean save-image

.PHONY: all build run clean clean-image save-image load-image clean-all complete
