# Deployment

## Running the project locally

The project provides a `Makefile` that allows running the app and installing dependencies.
You can run the project locally in a container using `make run-dev`. This command will use `docker-compose-dev.yml`, which will build the app's container.

If you want to run the app directly you can execute `make run-app`. Note that this will require you to install the dependencies beforehand, which can be done with `make install`.

It is important to note that the `make` command is meant to be executed from the project's root directory.

## Deploy in production

The project includes a release workflow that builds and publishes a docker image when creating a release. The `docker-compose.yml` uses that image to deploy a container with the app.
You can use the image to deploy the app in any cloud service, or in any VM.
Below we describe how the app can be deployed in any VM with `systemd` support, by running the containers as a service.

### 1. Install dependencies

The VM will need `docker`, and `docker compose` installed. Details on how to do this can be found in [`dockerdocs`](https://docs.docker.com/desktop/setup/install/linux/).

### 2. Create necessary files in the VM

Since this is considered a third-party app we recommend creating a folder in `/opt/`.

```shell
mkdir /opt/riscv-kci-bridge/
```

Then you'll need to get `Caddyfile`, `docker-compose.yml`, and `log.ini` files into this folder. You can get these files from the GitHub repo.

```shell
    /opt/riscv-kci-bridge/
        caddy/
            Caddyfile
        docker-compose.yml
        log.ini
```

### 3. Create a service file

To enable the service you need to create a `riscv-kci-bridge.service` file in `/etc/systemd/system`.

```shell
[Unit]
Description=REST services to run tests and builds for RISC-V and submit results to KCIDB
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=docker compose -f /opt/riscv-kcidb-bridge/docker-compose.yml up
ExecStop=docker compose -f /opt/riscv-kcidb-bridge/docker-compose.yml stop

[Install]
WantedBy=default.target
```

### 4. Enable the service

To enabble the service run `systemctl enable riscv-kci-bridge.service`.

### 5. Start the service

After enabling the service you can start using the `service` command.
To start the service run `service riscv-kci-bridge start`.

### 6. Extra commands

You can stop the service with `service riscv-kci-bridge stop`, and restart them with `service riscv-kci-bridge restart`.

### 7. Updating the app

To update the app you need to:

1. Poll the new version of the image: use `docker pull image`.
2. Stop the containers: you can use `service riscv-kci-bridge stop`.
3. Remove the existing container: you can use `docker container ls --all` to get all containers, and `docker container rm container_id` to remove the container.
4. Start up the container again: with `service riscv-kci-bridge start`.
