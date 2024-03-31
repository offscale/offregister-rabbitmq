# -*- coding: utf-8 -*-
from offregister_fab_utils.apt import apt_depends
from offutils import gen_random_str
from patchwork.files import append


def install0(**kwargs):
    installed = lambda: c.run(
        "dpkg-query --showformat='${Version}' --show rabbitmq-server", hide=True
    )

    if c.sudo("dpkg -s rabbitmq-server", hide=True, warn=True).exited != 0:
        apt_depends(c, "apt-transport-https", "curl")
        c.sudo(
            "curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc"
            " | apt-key add -"
        )
        c.sudo(
            'apt-key adv --keyserver "hkps.pool.sks-keyservers.net" --recv-keys "0x6B73A36E6026DFCA"'
        )
        codename = c.run("lsb_release -cs", hide=True)
        append(
            "/etc/apt/sources.list.d/bintray.erlang.list",
            "deb https://dl.bintray.com/rabbitmq-erlang/debian {codename} erlang".format(
                codename=codename
            ),
            use_sudo=True,
        )
        append(
            "/etc/apt/sources.list.d/bintray.rabbitmq.list",
            "deb https://dl.bintray.com/rabbitmq/debian {codename} main".format(
                codename=codename
            ),
            use_sudo=True,
        )
        c.sudo("apt-get update -qq")
        apt_depends(c, "rabbitmq-server")
        return "RabbitMQ {} installed".format(installed())

    return "[Already] RabbitMQ {} installed".format(installed())


def create_user1(**kwargs):
    password = kwargs.get("password", gen_random_str(15))
    c.sudo(
        "rabbitmqctl add_user {rmq_user} '{password}'".format(
            rmq_user=kwargs["rmq_user"], password=password
        )
    )
    if "rmq_vhost" in kwargs:
        c.sudo(
            "rabbitmqctl add_vhost {rmq_vhost}".format(rmq_vhost=kwargs["rmq_vhost"])
        )
    c.sudo(
        "rabbitmqctl set_permissions {rmq_vhost} {rmq_user} {permissions}".format(
            rmq_vhost="-p {rmq_vhost}".format(rmq_vhost=kwargs["rmq_vhost"])
            if "rmq_vhost" in kwargs
            else "",
            rmq_user=kwargs["rmq_user"],
            permissions=kwargs.get("permissions", '".*" ".*" ".*"'),
        )
    )
    return password
