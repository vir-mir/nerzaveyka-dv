#coding: utf-8

from apps.types_services.models import Item


class Manages():

    def get_items(self):
        return Item.objects.all()

    def get_all_items_portfolio(self, id):

        data = Item.objects.filter(portfolios__id=id)

        newData = []

        if data:
            for i in data:
                newData.append(i.id)

            return newData

        return data

    def get_item_id(self, id):
        try:
            return Item.objects.get(id=id)
        except Item.DoesNotExist:
            return None

    def delete_item_id(self, id):
        item = self.get_item_id(id)
        for portfolio in item.portfolios.all():
            item.portfolios.remove(portfolio)
        item.delete()

    def insert_item(self, data):
        item = Item()

        item.name = data['name']

        item.save()

        if data.has_key('data') and data['data']:
            for portfolio in data['data']:
                item.portfolios.remove(portfolio)
                item.portfolios.add(portfolio)

        return item

    def update_item(self, data):
        item = self.get_item_id(data['id'])

        item.name = data['name']

        item.save()

        if data.has_key('data') and data['data']:
            for portfolio in data['data']:
                item.portfolios.remove(portfolio)
                item.portfolios.add(portfolio)
        else:
            for portfolio in item.portfolios.all():
                item.portfolios.remove(portfolio)

        return item


