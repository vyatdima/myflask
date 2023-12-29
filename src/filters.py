from src import app

@app.template_filter('first_simvol')
def first_simvol_filter(s):
    return f'{s[:1]}.'


# @app.context_processor
# def utility_processor():
#     def list_events(param1):
#         list = User.query.all()
#         print(list)
#         return f'это список {param1}:\n {list}'
#     return dict(list_events=list_events)

