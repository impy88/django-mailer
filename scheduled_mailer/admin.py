# coding: utf-8

from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from scheduled_mailer.models import Message, DontSendEntry, MessageLog
from tinymce.widgets import TinyMCE
from .models import make_message
from django.utils.encoding import force_unicode
from django.core.mail import EmailMultiAlternatives
import lxml.html


class MessageAdminForm(forms.ModelForm):
    subject = forms.CharField(
        label = u"Тема", required=True)

    text = forms.CharField(
        label = u"Текст", widget=TinyMCE(), required=True)

    class Meta:
        model = Message
        fields = ('subject', 'text', 'when_send', 'priority')


class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "to_addresses", "subject", "when_added", "priority"]
    form         =  MessageAdminForm

    def save_model(self, request, obj, form, change):
        counter      = 0
        to           = None
        bcc          = []
        subject      = force_unicode(form.cleaned_data['subject'])
        message      = force_unicode(form.cleaned_data['text'])
        message_text = unicode(lxml.html.fromstring(form.cleaned_data['text']).text_content())
        emails       = set(User.objects.values_list('email', flat=True))
        
        for email in emails:
            counter = counter + 1

            if counter == 1 or (counter - 1) % 15 == 0: 
                to = email
            else:
                bcc.append(email)
            
            if counter == len(emails) or counter % 15 == 0:
                print 2
                msg = make_message(
                    subject=subject,
                    body=message_text,
                    to=[to],
                    bcc=bcc,
                    priority=form.cleaned_data['priority'],
                    when_send=form.cleaned_data['when_send'])

                e = msg.email
                e = EmailMultiAlternatives(e.subject, e.body, e.from_email, e.to, bcc=bcc)
                e.attach_alternative(message, "text/html")
                msg.email = e
                msg.save()

                bcc     = []
                to      = None

             

class DontSendEntryAdmin(admin.ModelAdmin):
    list_display = ["to_address", "when_added"]


class MessageLogAdmin(admin.ModelAdmin):
    list_display = ["id", "to_addresses", "subject", "when_attempted", "result"]


admin.site.register(Message, MessageAdmin)
admin.site.register(DontSendEntry, DontSendEntryAdmin)
admin.site.register(MessageLog, MessageLogAdmin)