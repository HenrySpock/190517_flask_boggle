from flask import Flask, render_template, jsonify, request, session
from boggle import Boggle
from dotenv import load_dotenv
import json

load_dotenv('.flaskenv')

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'your-secret-key-here'

boggle_game = Boggle()

@app.route('/')
def home():
    """Render home page."""
    return render_template('home.html')

@app.route('/play')
def play():
    """Render Boggle game page."""
    board = boggle_game.make_board()
    session['board'] = board  # add this line to store the board in the session
    print(session)
    return render_template('play.html', board=board) 
    # return render_template('play.html', board_json=board_json)

# @app.route('/checkword')
# def check_word():
#     """Check if a given word is valid."""
#     word = request.args.get('word', '')
#     print(word)
#     board = session['board'] 
#     print(board)
#     result = boggle_game.check_valid_word(board, word)
#     # return jsonify({'result': result})
#     return jsonify({'result': json.dumps(result)})

@app.route('/checkword')
def check_word():
    """Check if a given word is valid and can be formed using the letters on the board."""
    print('****')
    word = request.args.get('word', '').lower()
    print(word)
    board = session['board']
    print(board)
    boggle_game = Boggle()
    valid_word = boggle_game.check_valid_word(board, word)
    print(valid_word)
    word = request.args.get('word', '').upper()
    word_on_board = boggle_game.find(board, word)
    print(word_on_board)
    print('****')
    if valid_word == 'ok' and word_on_board:
        result = 'ok'
    elif valid_word == 'not-word':
        result = 'not-word'
    else:
        result = 'not-on-board'
    return jsonify({'result': result})

@app.route('/game-over', methods=['POST'])
def game_over():
    """Handle AJAX request after game is over."""
    if 'num_plays' not in session:
        session['num_plays'] = 0
    if 'high_score' not in session:
        session['high_score'] = 0

    # update number of plays
    session['num_plays'] += 1

    # get score from request
    score = request.json['score']

    # check if current score is higher than the stored high score
    if 'high_score' not in session or score > session['high_score']:
        session['high_score'] = score

    # return updated high score and number of plays
    return jsonify({'high_score': session['high_score'],
                    'num_plays': session['num_plays']})


if __name__ == '__main__':
    app.run(debug=True)