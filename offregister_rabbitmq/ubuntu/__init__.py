from os import urandom

from fabric.operations import sudo, run

from offregister_fab_utils.apt import apt_depends


def install0(**kwargs):
    installed = lambda: run("dpkg-query --showformat='${Version}' --show rabbitmq-server", quiet=True)

    if sudo('dpkg -s rabbitmq-server', quiet=True, warn_only=True).failed:
        apt_depends('rabbitmq-server')
        return 'RabbitMQ {} installed'.format(installed())

    return '[Already] RabbitMQ {} installed'.format(installed())


def create_user1(**kwargs):
    password = kwargs.get('password', generate_temp_password(15))
    sudo("rabbitmqctl add_user {rmq_user} '{password}'".format(rmq_user=kwargs['rmq_user'], password=password),
         shell_escape=False)
    if 'rmq_vhost' in kwargs:
        sudo('rabbitmqctl add_vhost {rmq_vhost}'.format(rmq_vhost=kwargs['rmq_vhost']))
    sudo('rabbitmqctl set_permissions {rmq_vhost} {rmq_user} {permissions}'.format(
        rmq_vhost='-p {rmq_vhost}'.format(rmq_vhost=kwargs['rmq_vhost']) if 'rmq_vhost' in kwargs else '',
        rmq_user=kwargs['rmq_user'], permissions=kwargs.get('permissions', '".*" ".*" ".*"')
    ))
    return password


def generate_temp_password(length):
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    return "".join(chars[ord(c) % len(chars)] for c in urandom(length))
