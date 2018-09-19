"""Main collection of views."""
from datetime import datetime
from flask import Blueprint, jsonify, render_template
from flask import current_app as app
from plugins import top_banner, left_panel, right_top, right_bottom, bottom_banner

# Blue print for the main display
blueprint = Blueprint(
    "smartmirror",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Blueprint for the Top Banner section
top_banner_blueprint = Blueprint(
    "top_banner",
    __name__,
    template_folder="template",
    static_folder="static"
)

# Blueprint for the right top panel
right_top_blueprint = Blueprint(
    "right_top_blueprint",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Blueprint for the left panel
left_blueprint = Blueprint(
    "left_blueprint",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Blueprint for the right bottom panel
right_bottom_blueprint = Blueprint(
    "right_bottom_blueprint",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Blueprint for the bottom banner
bottom_banner_blueprint = Blueprint(
    "bottom_banner_blueprint",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@blueprint.route("/", methods=["GET"])
def smartmirror():
    """Main Smart Mirror Template."""
    top_banner = source_template("top_banner", app.config)
    right_top_panel = source_template("right_top_panel", app.config)
    right_bottom_panel = source_template("right_bottom_panel", app.config)
    left_panel = source_template("left_panel", app.config)
    bottom_banner = source_template("bottom_banner", app.config)

    if app.config.get("environment") == "testing":
        app.logger.info("Using testing css file.")
        style = "main_testing.css"
    else:
        app.logger.info("Using production css file.")
        style = "main_prod.css"

    return render_template(
        "main.html",
        style=style,
        right_top_panel=right_top_panel,
        top_banner=top_banner,
        right_bottom_panel=right_bottom_panel,
        left_panel=left_panel,
        bottom_banner=bottom_banner
    )

##########################################################
"""
This Section contains the endpoint for the Top Banner
Currently the only plugins available are the following:
    -Greetings
    -Quotes
    -Python Tips
    -Reminders
"""
###########################################################


@top_banner_blueprint.route("/top_banner", methods=["GET", "POST"])
def top_banner_endpoint():
    """Endpoint for the Top Banner."""
    tb_config = app.config.get("top_banner").keys()[0]

    if tb_config == "greetings":
        data = top_banner.GreetingPlugin(app.logger)
        return jsonify(data.greetings())
    elif tb_config == "quotes":
        data = top_banner.QuotePlugin(app.logger)
        return jsonify(data.quotes())
    elif tb_config == "python_tips":
        data = top_banner.PythonTipPlugin(app.logger)
        return jsonify(data.python_tips())
    else:
        return jsonify({"Error": "No plugins selected"})


###########################################################
"""
This Section contains the endpoint for the right top panel
Currently the only plugins available are the following:
    -Date and Time
"""
###########################################################


@right_top_blueprint.route("/right_top", methods=["GET", "POST"])
def right_top_endpoint():
    """Route for the current time and data."""
    rt_config = app.config.get("right_top_panel").keys()[0]
    if rt_config == "time":
        data = right_top.DateTime(app.logger)
        return jsonify(data.date_time())
    else:
        return jsonify({"Error": "No plugins selected"})


###########################################################
"""
This Section contains the endpoint for the left panel
Currently the only plugins available are the following:
    -WunderGround
    -Stock
    -Place Holder
"""
###########################################################


@left_blueprint.route("/left_panel", methods=["GET", "POST"])
def left_endpoint():
    """Route for the left panel."""
    lp_config = app.config.get("left_panel").keys()[0]
    if lp_config == "wunderground":
        creds = app.config.get("left_panel").get("wunderground")
        api_key = creds.get("api_key")
        state = creds.get("state")
        zipcode = creds.get("zipcode")
        data = left_panel.WunderGround(api_key, state, zipcode, app.logger)
        return jsonify(data.current_with_forecast())
    elif lp_config == "stock":
        creds = app.config.get("left_panel").get("stock")
        api_key = creds.get("api_key")
        tickers = creds.get("tickers")
        data = left_panel.StockData(api_key, tickers, app.logger)
        return jsonify(data.get_stock_price())


###########################################################
"""
This Section contains the endpoint for the right bottom panel
Currently the only plugins available are the following:
    -New Jersey Transit
    -RSS feeds
"""
###########################################################


@right_bottom_blueprint.route("/right_bottom", methods=["GET", "POST"])
# @cache.cached(timeout=10)
def right_bottom_endpoint():
    """Route for the right bottom panel."""
    rb_config = app.config.get("right_bottom_panel").keys()[0]
    if rb_config == "njt":
        data = right_bottom.NJTPlugin(app.logger)
        pword = app.config.get("right_bottom_panel").get("njt")["password"]
        username = app.config.get("right_bottom_panel").get("njt")["username"]
        station = app.config.get("right_bottom_panel").get("njt")["train_station"]
        data_set = data.full_njt_dataset(pword, username, station, "Eastbound")
        return jsonify(data_set)
    elif rb_config == "rss":
        feed = app.config.get("right_bottom_panel").get("rss")["rss_feed"]
        data = right_bottom.RssPlugin(feed, app.logger)
        articles = data.rss_feed()
        return jsonify(articles)
    else:
        return jsonify({"Error": "No plugins selected"})


###########################################################
"""
This Section contains the endpoint for the bottom banner
Currently the only plugins available are the following:
    -US Holidays
    -Chuck Norris Jokes
"""
###########################################################


@bottom_banner_blueprint.route("/bottom_banner", methods=["GET", "POST"])
def bottom_banner_endpoint():
    """Route for the bottom banner."""
    bb_config = app.config.get("bottom_banner").keys()[0]
    if bb_config == "us_holidays":
        year = datetime.now().year
        data = bottom_banner.UsHolidays(year, app.logger)
        return jsonify(data.us_holidays())
    elif bb_config == "chuck_norris":
        data = bottom_banner.ChuckNorris(app.logger)
        return jsonify(data.joke())
    else:
        return jsonify({"Error": "No plugins selected"})


###########################################################
"""
Helper Functions
"""
###########################################################


def source_template(panel, config):
    """Helper function to determine if a template is needed."""
    if config.get(panel):
        _config = config.get(panel)
        template = "{p}/{t}.html".format(p=panel, t=_config.keys()[0])
        return template
    else:
        return False
