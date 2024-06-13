from src.product_search import price_filter, similarity_search


def case_2(item:dict):
    category = item['product_category'] + ' ' + item['gender']
    price = item['price']
    
    # Perform similarity search based on the category
    items1 = similarity_search(category, 'category',5,20)
    ids = []
    for doc, score in items1:
        ids.append(doc.metadata['id'])
    
    price_staus = price_filter(ids, price, 5)
    
    return ids,price_staus

dict = {"product_category": "skin care", "gender": "man", "price": 25}

print(case_2(dict))