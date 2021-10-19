from decimal import Decimal
from django.conf import settings
from app.models import Computer


class Cart(object):

    def __init__(self, request):
        """
        initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID]= {}
        self.cart = cart

    def add(self, computer, quantity=1, update_quantity=False):
        """
        Add aproduct to the cart or update its quantity.
        """
        computer_id = str(computer.id)
        if computer_id not in self.cart:
            self.cart[computer_id] = {'quantity':0, 'price':str(computer.price)}
        if update_quantity:
            self.cart[computer_id]['quantity'] = quantity
        else:
            self.cart[computer_id]['quantity'] += quantity
        self.save()

    def save(self):
        #update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        #mark the session as "modified" to make sure its saved
        self.session.modifed = True

    def remove(self, computer):
        """
        Remove a product from the cart
        """
        computer_id = str(computer.id)
        if computer_id in self.cart:
            del self.cart[computer_id]
            self.save()

    def __iter__(self):
        """
        iterate over the items in the cart and get the products from the database.
        """
        computer_ids = self.cart.keys()
        # get the computer objects and add them to the cart
        computers = Computer.objects.filter(id__in=computer_ids)
        for computer in computers:
            self.cart[str(computer.id)]['computer'] = computer

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
