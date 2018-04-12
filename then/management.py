# -*- coding: utf-8 -*-

"""Console script for then."""


# @click.argument('<arg>')
def manage():
    from then.components.email import EmailConfig, EmailTemplate
    config = EmailConfig(to='nekmo@localhost', server='localhost:1025')
    template = EmailTemplate(subject='{name}', body='Body: {name}')
    message = template.render(name='foo')  # EmailMessage
    message.send(config)
    # tpl.template(subject='{name}', body='Body: {name}').send(name='foo')

