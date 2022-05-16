from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    # IF ERROR IN bd session
    db.session.rollback()   # неудачные сеансы базы данных
                            # не мешают доступу к базе данных,
                            # вызванным шаблоном откат сеанса.
                            # Это сбрасывает сеанс в чистое состояние.
    return render_template('errors/500.html'), 500
