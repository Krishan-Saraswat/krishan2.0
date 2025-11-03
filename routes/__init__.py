from routes.finance_routes import register_finance_routes

def register_all_routes(app):
    register_finance_routes(app)
