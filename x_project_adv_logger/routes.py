from .views import BlockView, OfferView


def setup_routes(app):
    app.router.add_route('GET', '/v2/bl.js', BlockView)
    app.router.add_route('POST', '/v2/bl.js', BlockView)
    app.router.add_route('OPTIONS', '/v2/bl.js', BlockView)
    app.router.add_route('POST', '/v2/logger.json', OfferView)

    app.router.add_route('GET', '/v1/bl.js', BlockView)
    app.router.add_route('POST', '/v1/bl.js', BlockView)
    app.router.add_route('OPTIONS', '/v1/bl.js', BlockView)
    app.router.add_route('POST', '/v1/logger.json', OfferView)

    app.router.add_route('GET', '/bl.js', BlockView)
    app.router.add_route('POST', '/bl.js', BlockView)
    app.router.add_route('OPTIONS', '/bl.js', BlockView)
    app.router.add_route('POST', '/logger.json', OfferView)
