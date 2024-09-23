from .models import Product
from decimal import Decimal


class Cart():
    def __init__(self, request):
        self.session = request.session

        # eğer mevcut bir oturum varsa onun sepetinde olan ürünleri getirmemiz gerek
        cart = self.session.get("cart")

        # eğer mevcut bir oturum yoksa sepet içerisindeki cartı boş oluşturuyoruz
        if cart is None:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product, qty):

        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]["qty"] += qty
        else:
            self.cart[product_id] = {"price": str(product.price), "qty": qty}

        # Eğer miktar sıfır veya altına inerse ürünü sepetten sil
        if self.cart[product_id]["qty"] <= 0:
            del self.cart[product_id]

        # sepeti güncellediğimizde oturumu da güncellemeliyiz
        self.session.modified = True

    def update(self, product, btn_qty, qty):

        product_id = str(product.id)

        if btn_qty == "btn-plus":
            self.cart[product_id]["qty"] += qty
        else:
            self.cart[product_id]["qty"] -= qty

        # Eğer miktar sıfır veya altına inerse ürünü sepetten sil
        if self.cart[product_id]["qty"] <= 0:
            del self.cart[product_id]

        self.session.modified = True
    #
    # def prod_total_price(self):
    #
    #     for key, value in self.cart.items():
    #         self.cart[key]["price"] = str(Decimal(value["price"]) * Decimal(value["qty"]))
    #
    #     return self.cart

    def prod_total_price(self):
        total_price = Decimal('0.0')
        for key, value in self.cart.items():
            item_total = Decimal(value["price"]) * Decimal(value["qty"])
            self.cart[key]["total_price"] = str(item_total)
            total_price += item_total
        return total_price

    def get_prods(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        return products

    def __len__(self):
        return len(self.cart)
