from fabric.operations import sudo, run

from offregister_fab_utils.apt import apt_depends


def install0(**kwargs):
    installed = lambda: run("dpkg-query --showformat='${Version}' --show rabbitmq-server", quiet=True)

    if sudo('dpkg -s rabbitmq-server', quiet=True, warn_only=True).failed:
        apt_depends('rabbitmq-server')
        return 'RabbitMQ {} installed'.format(installed())

    return '[Already] RabbitMQ {} installed'.format(installed())
