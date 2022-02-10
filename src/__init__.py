import os

import sqlalchemy.orm.exc
from flask import Flask, redirect, url_for, render_template, abort, jsonify
from flask_migrate import Migrate


def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev')
    )

    if test_config is None:
        app.config.from_pyfile('../config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from .models import db, Ticket
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        return redirect(url_for('tickets'))

    @app.route('/tickets')
    def tickets():
        tickets_all = Ticket.query.all()
        return render_template('tickets_index.html', tickets=tickets_all)

    @app.route('/tickets/<int:ticket_id>')
    def tickets_show(ticket_id):
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).one()
            return render_template('tickets_show.html', ticket=ticket)
        except sqlalchemy.orm.exc.NoResultFound:
            abort(404)

    @app.route('/api/tickets')
    def api_tickets():
        tickets_all = Ticket.query.all()
        return jsonify([ticket.to_json() for ticket in tickets_all])

    @app.route('/api/tickets/<int:ticket_id>')
    def api_tickets_show(ticket_id):
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).one()
            return jsonify(ticket.to_json())
        except sqlalchemy.orm.exc.NoResultFound:
            abort(404)

    return app
