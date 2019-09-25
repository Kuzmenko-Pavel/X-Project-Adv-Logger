from .views import BlockView, OfferView


def setup_routes(app):
    app.router.add_route('GET', '/v2/bl.js', BlockView)
    app.router.add_route('POST', '/v2/bl.js', BlockView)
    app.router.add_route('OPTIONS', '/v2/bl.js', BlockView)
    app.router.add_route('POST', '/v2/logger.json', OfferView)
