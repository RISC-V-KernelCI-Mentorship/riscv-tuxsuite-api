# Configuration

## Environment variables

The app is configured via environment variables, which are defined in tow `.env` files.

1. `.env`: Contains sereval definitions that affect the behaviour of the app itself.
2. `.env_caddy`: Variables used to configure `Caddy`.

These were splitted since they're used by two different containers. Templates for both of this files can be found in the root of the project, in `.env.example` and `.env_caddy.example` respectively.

### `.env`

* `PROJECT_NAME`: Name of the project
* `BACKEND_CORS_ORIGINS`: CORS configuration
* `LOGS_FILE`: Path to the file used to store logs
* `DEBUG`: `true`|`false`
* `DB_URL`: URL used to connect to the database
* `DB_CERT_PATH`: Path to the certificate used when performing an SSL conenction
* `TUXSUITE_TOKEN`: Access token used to connect to TuxSuite. Only required when using `tuxsuite`runner. Please contact the [TuxSuite team](https://tuxsuite.com/) to request a token
* `KCIDB_SUBMIT_URL`: KCIDB URL used to perform submissions
* `KCIDB_TOKEN`: Token required to perform submissions. Please contact the [KernelCI team](https://github.com/kernelci/kcidb?tab=readme-ov-file) to get one

### `.env_caddy`

* `EXT_ENDPOINT1`: URL used to access the VM
* `LOCAL_1`: `localhost`
* `LOCAL_2`: `127.0.0.1`, or any other IP used to refer to `localhost`

## Database

The app requires a database to store tests that have already been run and build results.
The connection to the database is setup using `SQLAlchemy`. You can find more information regarding `SQLAlchemy` database support [here](https://docs.sqlalchemy.org/en/20/dialects/index.html).

The `.env` file contains to variables related to database configuration:

1. `DB_URL`: Corresponds to the database URL. More information regarding how these should be constructed can be found in `SQLAlchemy`[documentation](https://docs.sqlalchemy.org/en/20/core/engines.html).
2. `DB_CERT_PATH`: Path to the certificate used when performing and SSL connection. If you're running the app in a container this file should be [bind mounted](https://docs.docker.com/engine/storage/bind-mounts/), so that it becomes accessible inside the container.

The app has been tested using `SQLite` and `Postgres`.
