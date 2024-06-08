import pandas as pd

df = pd.read_csv("DataFiles/data.csv")

def image_tracker(items:list):
    list = items[:3]
    rows_dict = df[df['id'].isin(list)].to_dict('records')
    for row in rows_dict:
        print(f"id:{row['id']}, price : {row['price']}")
    with open("DataFiles/output.txt", "w") as file:
        for row in rows_dict:
            file.write(f"id :{row['id']}, price :{row['price']}\n")

    image_list = []
    for row in rows_dict:
        image_list.append(row['img_primary'])

    url_list = []
    for row in rows_dict:
        url_list.append(row['url'])
    
    return image_list, url_list



a = ['p10', 'p11', 'p12']
image_tracker(a)