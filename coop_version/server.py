from flask_restful import Api, Resource

from game_logic import game_data

api = Api()


class Move(Resource):
    def get(self, move, user_id):
        if move == 'send':
            return {'blocks': game_data['to_send'], 'run': game_data['running'], 'turn': game_data['turn'],
                    'score': game_data['score']}
        else:
            if (game_data['current_player'] and user_id == '1') or (not game_data['current_player'] and user_id == '2'):
                game_data['event'] = move
                print(move)
                return {"status": "200"}

            return {"status": "503"}


class NewUser(Resource):
    def get(self):
        game_data['users'] = game_data['users'] + 1
        user_id = game_data['users']

        if user_id == 1:
            game_data['ready_to_start'] = True

        if user_id <= 2:
            return {"id": user_id}
        else:
            return {"error": "too many users"}


api.add_resource(NewUser, '/new_user')
api.add_resource(Move, '/move/<move>/<user_id>')
