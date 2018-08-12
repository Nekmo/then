THEN
####
Esta biblioteca es una colección de medios de comunicación con servicios externos al programa, denominados
"componentes". Algunos ejemplos son email, Telegram o Slack. No sólo pueden enviarse mensajes, sino también eventos,
como puede ser a IFTTT, Homeassistant, entre otros. Then incluye además opciones para facilitar el uso entre
componentes y de configuración.


Ejemplo básico
==============

Éste es un ejemplo básico para una aplicación de monitorización de discos duros:

.. code-block:: python

    from them import Context
    from then.components import Email

    context = Context(
        subject='[ERROR] HDD SATAIII Barracuda lifetime 10%',
        body="Hello Nekmo,\nThis is the latest monitoring result: ..."
    )
    email = Email(to='nekmo@localhost')
    email.send(context)


O simplificado:

.. code-block:: python

    email = Email(to='nekmo@localhost')
    email.send(subject='[ERROR] HDD SATAIII Barracuda lifetime 10%',
               body="Hello Nekmo,\nThis is the latest monitoring result: ...")


Templates
=========

Como en muchas ocasiones los mensajes no son estáticos, es posible generar el contexto con templates:

.. code-block:: python

    from them.templates import FormatTemplateContext
    from then.components import Email

    context = FormatTemplateContext(
        subject="[{level.upper}] HDD {name} lifetime {lifetime}",
        body="Hello {user},\nThis is the latest monitoring result: {result}"
    ).args(level="error", name="SATAIII Barracuda", lifetime="10%", user="Nekmo", result="...")
    email = Email(to='nekmo@localhost')
    email.send(context)


Múltiples servicios
===================

No obstante, si queremos tener varios métodos de envío (como es la idea tras THEN) esta forma deja de ser eficiente,
incluyéndose así una forma de poder incluir varias configuraciones y contextos:

.. code-block:: python

    from then import Then
    from them.templates import FormatTemplateContext
    from then.components import Email, Telegram


    t = Then(
        Email(to='nekmo@localhost'),
        Telegram(token='...', to='nekmo'),
        Telegram(token='...', to='myfriend').use_as('telegram-friend'),
    t = t.context(
        FormatTemplateContext(
            subject="[{level.upper}] HDD {name} lifetime {lifetime}",
            body="Hello {user},\nThis is the latest monitoring result: {result}"
        ).context_as('default'),
        GetContext('default').join(body=['subject', 'body']).context_as('default@telegram'),
    )
    message = t.args(level="error", name="SATAIII Barracuda", lifetime="10%", user="Nekmo", result="...")
    message.use('telegram-friend').send()


Los servicios por defecto reciben el nombre de contexto "default", y se aplicará a todos los componentes que sea
posible, salvo que se defina uno usando arroba y a continuación el nombre del componente. El valor tras arroba
puede ser el nombre del componente con "use_as", o el nombre de la clase del componente. Es posible definir varios
valores para el método, como en el siguiente ejemplo::

    .context_as('default@telegram', 'default@email')

O de la siguiente forma::

    .context_as(name='default', components=['telegram', 'email'])

Puede haber varios default, incluso sin definir el componente. En tal caso, THEN escogerá el que mejor se adapte al
componente según las variables disponibles. Por ejemplo, si Telegram requiere "body", y 2 contextos por defecto
ofrecen dicha variable, pero una de ellas ofrece además subject, la cual no requiere Telegram, entonces usará la que
no tiene subject.


Pipe
====

Los pipe permiten transformar los contextos para adecuarse a las necesidades de otro componente. Permiten copiar
variables y transformar las variables existentes.

Ejemplo para convertir un template HTML a uno de texto plano

.. code-block:: python

    from them.pipes import Html2Plain
    from them.templates import FormatTemplateContext

    context = FormatTemplateContext(
        subject="[{level.upper}] HDD {name} lifetime {lifetime}",
        body="Hello <strong>{user}</strong>,\nThis is the latest monitoring result: <code>{result}</code>"
    )
    context2 = context.pipe(body=Html2Plain('body'))


Copiar variable body en description:

.. code-block:: python

    from them.templates import FormatTemplateContext

    context = FormatTemplateContext(
        subject="[{level.upper}] HDD {name} lifetime {lifetime}",
        body="Hello {user},\nThis is the latest monitoring result: {result}"
    )
    context2 = context.pipe(description='body')


Unir 2 variables y separarlas por un salto de línea (esta opción está de serie con el método join):

.. code-block:: python

    from them.pipes import Join
    from them.templates import FormatTemplateContext

    context = FormatTemplateContext(
        subject="[{level.upper}] HDD {name} lifetime {lifetime}",
        body="Hello {user},\nThis is the latest monitoring result: {result}"
    )
    context2 = context.pipe(body=Join('subject', 'body'), sep='\n\n')


Desde archivos
==============

Como no es posible ni eficiente introducir en el código la configuración del servicio, THEN permite leer desde
un archivo de configuración dicha información:

.. code-block:: python

    from then import Then, LoadConfig

    t = Then(LoadConfig('/path/to/config.json', section='components'))
    t.context( ... )

``LoadConfig`` es capaz de leer desde diferentes archivos de configuración (la cual determina por la extensión del
archivo, o usando el parámetro ``format=``), y su sección de configuración tiene una estructura cerrada:

.. code-block:: json

    {
        "components": [
            {
                "component: "email",
                "config": {
                    "to": "nekmo@localhost"
                }
            },
            {
                "component": "telegram",
                "config": {
                    "token": "...",
                    "to": "nekmo"
                }
            }
            {
                "component": "telegram",
                "config": {
                    "token": "...",
                    "to": "myfriend"
                },
                "use_as": "telegram-friend"
            }
        ]
    }


Reemplazar contexts
===================

El usuario puede querer reemplazar el template por defecto para un servicio, lo cual podría hacer desde un
fichero de configuración. La función ``from_config`` permite de nuevo este uso, en conjunto con su parámetro
``defaults=``.

.. code-block:: python

    from then import Then
    from then.components.email import EmailTemplate
    from then.components.telegram import TelegramTemplate


    t = Then(...)
    t = t.context(
        FormatTemplateContext(
            subject="[{level.upper}] HDD {name} lifetime {lifetime}",
            body="Hello {user},\nThis is the latest monitoring result: {result}"
        ).context_as('default'),
        GetContext('default').join(body=['subject', 'body']).context_as('default@telegram'),
    )
    t = t.context(LoadConfig('/path/to/config.json', section='contexts'))

En el archivo de configuración:

.. code-block:: json

    {
        "contexts": [
            {
                "context_as": "default",
                "options": {
                    "subject": "[HDD Monitor] {name} lifetime {lifetime} ({level.upper})",
                    "body": "Hi {user},\Latest monitoring result:\n{result}"
                }
            },
            {
                "context": "default@telegram"
                "use_context": "default",
                "join": ["subject", "body"]
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



Archivos adjuntos
=================

Cada servicio permite adjuntar diferentes tipos de archivos y datos, por lo que THEN soporta en su versión actual
los siguientes:

* Photo
* Audio
* Document
* Video
* Voice
* Contact
* Location
* File

Un ejemplo de su uso sería:

.. code-block:: python

    from then import Then
    from then.attach import Photo

    message = Then(configs=[
        ...
    ).use('telegram').render(**{
        ...
    })
    message.attach(Photo('/path/to/image.jpg')).send()


No obstante, cada servicio tiene sus propias limitaciones, sobre todo en cuanto a archivos adjuntos se refiere. Algunos
permiten enviar varios, otros sólo uno, y otros incluso ninguno. También hay limitaciones por tipo de archivo,
tamaño, etc. THEN tiene varias opciones para solventar estas posibles limitaciones, para las cuales se incluyen las
siguientes 3 opciones:

* **unsupported**: acción a realizar en caso de no soportarse el tipo de archivo. Posibles acciones: ``replace``
  (buscará la mejor solución), ``ignore`` (no se enviará este archivo) o ``raise`` (saltará una excepción).
* **error**: en caso de ocurrir una excepción, o no haber un posible replace, acción a realizar. Posible acciones:
  ``ignore`` (ignorar el error) o ``raise`` (saltará la excepción original).
* *nombre del servicio*. Esta última opción consiste en, usando el nombre del servicio (por ejemplo, *email*)
  definir una de las soluciones anteriores (``replace``, ``ignore`` o ``raise``) o definir otro tipo de adjunto a
  utilizar.


Ejemplo que conjunta las 3 opciones a nivel global:


.. code-block:: python

    from then import Then
    from then.attach import Photo

    message = Then(configs=[
        ...
    ).use('telegram').render(**{
        ...
    })
    message.attach(Photo('/path/to/image.jpg'), unsupported="ignore", error="ignore",
                   email="replace").send()


También es posible emplear estas opciones por cada archivo:

.. code-block:: python

    from then import Then
    from then.attach import Photo

    message = Then(configs=[
        ...
    ).use('telegram').render(**{
        ...
    })
    message.attach(Photo('/path/to/image.jpg', unsupported="ignore", error="ignore",
                         email=File('/path/to/image2.jpg'))).send()


Por defecto, **unsupported** usará ``replace`` y **error** usará ``raise``.
