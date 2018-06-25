from .views import BlockView, OfferView


def setup_routes(app):
    app.router.add_route('GET', '/bl.js', BlockView)
    app.router.add_route('POST', '/bl.js', BlockView)
    app.router.add_route('OPTIONS', '/bl.js', BlockView)
    app.router.add_route('POST', '/logger.json', OfferView)
