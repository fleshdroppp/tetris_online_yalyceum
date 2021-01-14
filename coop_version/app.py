from threading import Thread

from flask import Flask

from game_logic import game
from game_logic import game_data


def create_app():
    # Flask init
    app = Flask(__name__)

    # Spawn game thread
    job = Thread(target=game)
    job.start()

    # Register API
    from server import api
    api.init_app(app)

    return app


if __name__ == '__main__':
    main_app = create_app()
    main_app.run(debug=False)
    # choose your ip and port
    # main_app.run(host="0.0.0.0", port=3333)
