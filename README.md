offregister_rabbitmq
====================
This package follows the offregister specification for RabbitMQ

## Install dependencies

    pip install -r requirements.txt

## Install package

    pip install .

## Example config

    {
        "module": "offregister-rabbitmq",
        "type": "fabric",
        "kwargs": {
        }
    }

To setup your environment to use this config, follow [the getting started guide](https://offscale.io/docs/getting-started).

## Roadmap

  - Additional users and passwords (example: `rabbitmqctl add_user username_here password_here`)
  - Custom config
  - Clustering
