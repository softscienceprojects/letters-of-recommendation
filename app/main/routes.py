from app.main import bp

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    # get the title and first image of the most recent post
    return "HELLO"

@bp.route('/posts', methods=['GET'])
def posts():
    pass


