from libraries import serpstack
#
def elt_serpstack(event, context):
    keywords = ["mcdonalds", "data", "consultancy", "data engineering"]
    location = "us"
    api_result = serpstack.serpStackApi().make_api_request(keywords, location)
    serpstack.save_results_to_csv(api_result)