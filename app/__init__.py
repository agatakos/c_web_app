from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, distinct
from flask import request, jsonify, abort, make_response
from instance.config import app_config
from datetime import datetime


# initialize sql-alchemy
db = SQLAlchemy()


# create app
def create_app(config_name):
    from app.models import Policy, Policy_Day, User_Month, Finance, session

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[DevelopmentConfig])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.route("/")
    def index():
        obj = {
            "LIST OF ENDPOINTS": "",
            "PolicyCount": "/policy_count/<user_id>",
            "DaysActive": "/days_active/<user_id>",
            "NewUserCount": "/new_user_count/<YYYY-MM-DD>",
            "LapsedUserCount": "/lapsed_users_count/<YYYY-MM>",
            "NewUserPremiums": "/new_user_premiums/<underwriter>",
        }
        return obj

    @app.route("/policy_count/<string:user_id>", methods=["GET"])
    def policy_count(user_id: str):
        policy = (
            session.query(
                Policy.user_id,
                db.func.count(Policy.policy_id).label("policy_count"),
            )
            .filter(Policy.user_id == user_id)
            .group_by(Policy.user_id)
            .all()
        )

        results = []

        for p in policy:
            obj = {"UserId": p.user_id, "PolicyCount": p.policy_count}

            results.append(obj)

        return make_response(jsonify(results)), 200

    @app.route("/days_active/<string:user_id>", methods=["GET"])
    def days_active(user_id: str):
        policy = (
            session.query(
                Policy.user_id,
                db.func.extract(
                    "day",
                    db.func.max(Policy.policy_end_date)
                    - db.func.min(Policy.policy_start_date),
                ).label("days_active"),
            )
            .filter(Policy.user_id == user_id)
            .group_by(Policy.user_id)
            .all()
        )

        results = []

        for p in policy:
            obj = {"user": p.user_id, "days_active": p.days_active}

            results.append(obj)

        return make_response(jsonify(results)), 200

    @app.route("/new_user_count/<string:date>", methods=["GET"])
    def new_users(date):
        date = str(datetime.strptime(date, "%Y-%m-%d").date())
        new_users = (
            session.query(
                Policy_Day.c.date,
                db.func.count(Policy_Day.c.user_id).label("count_of_users"),
                Policy_Day.c.status,
            )
            .filter(
                and_(Policy_Day.c.date == date, Policy_Day.c.status == "New")
            )
            .group_by(Policy_Day.c.date, Policy_Day.c.status)
            .all()
        )
        results = []

        for n in new_users:
            obj = {
                "NewUserCount": n.count_of_users,
                "Date": n.date,
                "Status": n.status,
            }

            results.append(obj)

        return make_response(jsonify(results)), 200

    @app.route("/lapsed_users_count/<string:year_month>", methods=["GET"])
    def lapsed_users(year_month):
        lapsed_users = (
            session.query(
                User_Month.c.year_month,
                db.func.count(User_Month.c.user_id).label("count_of_users"),
                User_Month.c.user_lifecycle_status.label("status"),
            )
            .filter(
                and_(
                    User_Month.c.user_lifecycle_status == "lapsed",
                    User_Month.c.year_month == year_month,
                )
            )
            .group_by(
                User_Month.c.year_month, User_Month.c.user_lifecycle_status
            )
            .all()
        )

        results = []

        for l in lapsed_users:
            obj = {
                "LapsedUserCount": l.count_of_users,
                "Month": l.year_month,
                "Status": l.status,
            }

            results.append(obj)

        return make_response(jsonify(results)), 200

    @app.route("/new_user_premiums/<string:underwriter>", methods=["GET"])
    def new_user_premiums(underwriter):
        new_user_premiums = (
            (
                session.query(
                    Policy.underwriter,
                    db.func.sum(distinct(Finance.premium)).label(
                        "premium_total"
                    ),
                )
            )
            .join(Finance, Finance.policy_id == Policy.policy_id)
            .join(User_Month, User_Month.c.user_id == Policy.user_id)
            .filter(
                and_(
                    User_Month.c.user_lifecycle_status == "new",
                    Finance.reason == "policy_sale",
                    Policy.underwriter == underwriter,
                )
            )
            .group_by(Policy.underwriter)
            .all()
        )

        results = []

        for p in new_user_premiums:
            obj = {
                "Underwriter": p.underwriter,
                "PremiumTotals": p.premium_total,
            }

            results.append(obj)

        return make_response(jsonify(results)), 200

    return app
