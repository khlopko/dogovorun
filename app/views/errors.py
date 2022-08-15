from flask import render_template


def register_error_handlers(app):
    app.errorhandler(400)(bad_request)
    app.errorhandler(403)(forbidden)
    app.errorhandler(404)(not_found)
    app.errorhandler(500)(internal_error)


def bad_request(error):
    return render_template('errors/400.html'), 400


def forbidden(error):
    return render_template('errors/403.html'), 403


def not_found(error):
    return render_template('errors/404.html'), 404


def internal_error(error):
    return render_template('errors/500.html'), 500