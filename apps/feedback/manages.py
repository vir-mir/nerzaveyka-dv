#coding: utf-8

from apps.feedback.models import Fos, Callback


class Manages():

    def insert_fos(self, data):
        fos = Fos()

        fos.email = data['email']
        fos.fio = data['fio']
        fos.text = data['text']

        fos.save()

        return fos

    def insert_callback(self, data):
        callback = Callback()

        callback.email = data['email']
        callback.phone = data['phone']
        callback.fio = data['fio']
        callback.text = data['text']

        callback.save()

        return callback

