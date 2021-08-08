import pandas as pd
from turicreate import SFrame, recommender, load_model
import os

from web.models import Ordered

data_dir = '../data'
model_dir = '../models'
model_file_names = os.listdir(model_dir)
department_dict = {}
department_model_dict = {}

product_meta_df = pd.read_csv(os.path.join(data_dir, "products_added.csv"))

for model_name in model_file_names:
    department_dict[model_name.split("_")[1]] = model_name.split("_")[0]
    department_model_dict[model_name.split("_")[1]] = load_model(os.path.join(model_dir, model_name))

def item_recommendation(item_id):
    department_id = product_meta_df.loc[product_meta_df["product_id"]==item_id]['department_id'].values[0]
    return list(department_model_dict[department_id].get_similar_items(items=[item_id])["similar"][:5])

def user_recommendation(user_id):
    my_deparments = list(department_dict.keys())
    my_sframe = department_model_dict[my_deparments[0]].recommend(users=[user_id])

    for department_id in my_deparments[1:]:
        try:
            my_sframe = my_sframe.append(department_model_dict[department_id].recommend(users=[user_id]))
        except KeyError:
            print("Department ID ({}) does not have a model".format(department_id))

    return list(my_sframe.topk('score', k=5)['item_id'])
