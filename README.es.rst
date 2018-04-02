THEN
####
Muchos programas pueden requerir comunicarse con el usuario o con otros sistemas ante ciertos eventos. En tal
situación, lo más habitual es implementar el envío de un email, y permitir al usuario configurar el servidor, el
origen y el destinarario de dicho email. No obstante, esta solución es insuficiente para muchos usuarios de la
aplicación, y acaban requiriendo la implementación de nuevos métodos de envío, como SMS, Telegram. IFTTT, Slack...
Este trabajo de implementación, que se repite en muchas aplicaciones, puede (y debería) ser realizada por una
biblioteca especiazada, la cual ha sido creada bajo el nombre de THEN.

Los 3 pilares de THEN son:

* Configuración del servicio.
* Template de renderizado
* Mensaje

Ejemplo básico
==============

Éste es un ejemplo básico de una aplicación de monitorización de discos duros (sin aprovechar todo el potencial de
THEN) que conjunta las 3 partes:

.. code-block:: python

    from then.components.email import EmailConfig, EmailTemplate

    config = EmailConfig(to='nekmo@localhost')
    template = EmailTemplate(subject="[{level.upper}] HDD {name} lifetime {lifetime}",
                             body="Hello {user},\nThis is the latest monitoring result: {result}")
    template.set_config(config)
    message = template.render({
        "level": "error", "name": "SATAIII Barracuda", "lifetime": "10%", "user": "Nekmo", "result": "...",
    })  # EmailMessage
    message.send()


O simplificado:

.. code-block:: python

    from then.components.email import EmailConfig

    config = EmailConfig(to='nekmo@localhost').template(
        subject="[{level.upper}] HDD {name} lifetime {lifetime}",
        body="Hello {user},\nThis is the latest monitoring result: {result}"
    ).render({
        "level": "error", "name": "SATAIII Barracuda", "lifetime": "10%", "user": "Nekmo", "result": "...",
    }).send()


Múltiples servicios
===================

No obstante, si queremos tener varios métodos de envío (como es la idea tras THEN) esta forma deja de ser eficiente,
incluyéndose así una forma de poder incluir varias configuraciones y templates personalizados por cada servicio:

.. code-block:: python

    from then import Then
    from then.components.email import EmailConfig, EmailTemplate
    from then.components.telegram import TelegramConfig, TelegramTemplate

    t = Then(configs=[
        EmailConfig(to='nekmo@localhost'),
        TelegramConfig(token='...', to='@nekmo'),
    ], templates=[
        EmailTemplate(subject="[{level.upper}] HDD {name} lifetime {lifetime}",
                      body="Hello {user},\nThis is the latest monitoring result: {result}"),
        TelegramTemplate(body="**[{level.upper}] HDD {name} lifetime {lifetime}**\n\nResult: {result}"),
    ])
    t.use('telegram').render({
        "level": "error", "name": "SATAIII Barracuda", "lifetime": "10%", "user": "Nekmo", "result": "...",
    }).send()


Desde archivos
==============

Como no es posible ni eficiente introducir en el código la configuración del servicio, THEN permite leer desde
un archivo de configuración dicha información:

.. code-block:: python

    from then import Then, from_config

    Then(configs=from_config('/path/to/config.json', section='send_config'), templates=[
        ...
    ])

``from_config`` es capaz de leer desde diferentes archivos de configuración (la cual determina por la extensión del
archivo, o usando el parámetro ``format=``, y su sección de configuración tiene una  estructura cerrada:

.. code-block:: json

    {
        "send_config": [
            {
                "service_name: "email",
                "to": "nekmo@localhost"
            },
            {
                "service_name: "telegram",
                "token": "...",
                "to": "name"
            }
        ]
    }


Múltiples configuraciones
=========================

Por defecto, se usará la primera configuración para el servicio disponible. No obstante, es posible tener varias
disponibles usando el parámetro adicional ``send_name``, y usando dicho ``send_name`` en ``.use()``:

.. code-block:: python

    from then import Then
    from then.components.email import EmailConfig

    t = Then(configs=[
        EmailConfig(to='nekmo@localhost', send_name="nekmo"),
        EmailConfig(to='alerts@localhost', send_name="alerts"),
    ], templates=[
        ...
    ])
    t.use('alerts').render({
        ...
    }).send()

En cualquiera de los casos, se recomienda dejar al usuario la posibilidad de definir el nombre de servicio o
*send_name* a emplear para el envío de un mensaje con ``.use()``.


Reemplazar templates
====================

El usuario puede querer reemplazar el template por defecto para un servicio, lo cual podría hacer desde un
fichero de configuración. La función ``from_config`` permite de nuevo este uso, en conjunto con su parámetro
``defaults=``.

.. code-block:: python

    from then import Then
    from then.components.email import EmailTemplate
    from then.components.telegram import TelegramTemplate


    t = Then(configs=[
        ...
    ], templates=from_config('/path/to/config.json', section='send_template', defaults=[
        EmailTemplate(subject="[{level.upper}] HDD {name} lifetime {lifetime}",
                      body="Hello {user},\nThis is the latest monitoring result: {result}"),
        TelegramTemplate(body="**[{level.upper}] HDD {name} lifetime {lifetime}**\n\nResult: {result}"),
    ])

En el archivo de configuración:

.. code-block:: json

    {
        "send_template": [
            {
                "service_name: "email",
                "subject": "[{level.upper}] HDD {name} lifetime {lifetime}",
                "body": "Hello {user},\nThis is the latest monitoring result: {result}"
            },
            {
                "service_name: "telegram",
                "body": "**[{level.upper}] HDD {name} lifetime {lifetime}**\n\nResult: {result}"
            }
        ]
    }


Diferentes renders
==================
Por defecto, THEN utiliza para renderizar los templates la función ``.format()`` de Python, la cual puede
consultarse `aquí <https://docs.python.org/3/library/string.html#formatstrings>`_. Pero este formato puede quedarse
corto para según qué situaciones, necesitando opciones más potentes. Existen otras formas de renderizar, como por
ejemplo Jinja2. La forma manual de usar estos renders sería como la siguiente:

.. code-block:: python

    from then.components.email import EmailTemplate
    from then.renders import Jinja2RenderMixin

    class Jinja2RenderTemplate(Jinja2RenderMixin, EmailTemplate):
        pass

    Jinja2RenderTemplate(
        subject="[{{ level | upper }}] HDD {{ name }} lifetime {{ lifetime }}",
        body="Hello {{ user }},\nThis is the latest monitoring result: {{ result }}"
    )

Pero THEN es capaz de hacer este trabajo de forma automática:

.. code-block:: python

    from then import Then
    from then.components.email import EmailTemplate
    from then.renders import Jinja2RenderMixin

    t = Then(configs=[
        ...
    ], templates=[
        EmailTemplate(subject="[{{ level | upper }}] HDD {{ name }} lifetime {{ lifetime }}",
                      body="Hello {{ user }},\nThis is the latest monitoring result: {{ result }}"),
    ], template_mixin=Jinja2RenderMixin)

