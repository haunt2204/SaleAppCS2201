import json


def load_categories():
    with open("data/categories.json", encoding="utf-8") as f:
        return json.load(f)


def load_products(q=None, cate_id=None):
    with open("data/products.json", encoding="utf-8") as f:
        products = json.load(f)

        if q:
            products = [p for p in products if p["name"].find(q) >= 0]
        if cate_id:
            products = [p for p in products if p["id"].__eq(int(cate_id))]

        return products


if __name__=="__main__":
    print(load_products())