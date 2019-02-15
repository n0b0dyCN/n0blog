from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views
from . import posts_api
from . import links_api
from . import comments_api
from . import statistics_api
from . import backup