from libraries import serpstack

# def handler(event, context):
#     response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
#     res = {
#         "event": event,
#         "output": response.json(),
#         "context": context
#     }
#     print(res & 'hola')

#     return None

def elt_serpstack(event, context):
    keywords = ["data engineering services", "data analysis services", "mcdonalds"]
    location = "us"
    serpstack.serpStackApi().make_api_request(keywords, location)