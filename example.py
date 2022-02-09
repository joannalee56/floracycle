from model import Classified

def filter_search(lst_of_tag_ids, cost_type, cost):

query = Classified.query.options(db.joinedload('tags'))

if filter_by_tags:
    query = query.filter(filtertags)

if lst_of_tag_ids:
    for id in lst_of_tag_ids:
        query = query.filter(Tag.tag_label == "events")

if max_price:
    query = query.filter(Classified.cost <= 50)
    query = query.filter(Classified.cost == "145")
if cost_type:
    query = query.filter(Classified.cost_type == 'sale')

    query = query.filter(Classified.post_title.in_(["wedding"]))
results = query.all()



