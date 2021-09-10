from flask import Flask

def init_app(app: Flask):
    from app.views.routes_views import routes_views
    routes_views(app)
    return app