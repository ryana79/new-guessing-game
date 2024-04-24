from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# A dictionary with categories and lists of image URLs
image_dataset = {
    'animals': [
        {'url': 'https://cdn.pixabay.com/photo/2017/07/18/18/24/dove-2516641_1280.jpg', 'answer': 'dove'},
        {'url': 'https://upload.wikimedia.org/wikipedia/commons/4/41/Siberischer_tiger_de_edit02.jpg', 'answer': 'tiger'},
        {'url': 'https://cdn.pixabay.com/photo/2015/11/16/14/43/cat-1045782_1280.jpg', 'answer': 'cat'}
    ],
    'landmarks': [
        {'url': 'https://www.nationsonline.org/gallery/Monuments/Eiffel_Tower.jpg', 'answer': 'eiffel tower'},
        {'url': 'https://t3.ftcdn.net/jpg/03/04/85/26/360_F_304852693_nSOn9KvUgafgvZ6wM0CNaULYUa7xXBkA.jpg', 'answer': 'taj mahal'},
        {'url': 'https://cdn.pixabay.com/photo/2014/09/11/18/23/london-441853_1280.jpg', 'answer': 'big ben'}
    ],
    'fruits': [
        {'url': 'https://cdn.pixabay.com/photo/2017/06/02/18/24/fruit-2367029_1280.jpg', 'answer': 'mixed fruits'},
        {'url': 'https://upload.wikimedia.org/wikipedia/commons/a/af/Clementine_orange.jpg', 'answer': 'clementine'},
        {'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Durian.jpg/2560px-Durian.jpg', 'answer': 'durian'}
    ]
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        game_mode = request.form.get('mode')
        if game_mode == 'visual_quiz':
            return redirect(url_for('visual_quiz_setup'))
        else:
            difficulty = request.form['difficulty']
            max_number, attempts = {'easy': (10, 5), 'medium': (50, 7), 'hard': (100, 10)}[difficulty]
            session['max_number'] = max_number
            session['attempts'] = attempts
            session['secret_number'] = random.randint(1, max_number)
            return redirect(url_for('guess'))
    return render_template('index.html')

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if 'secret_number' not in session:
        return redirect(url_for('home'))

    message, game_over = None, False
    if request.method == 'POST':
        guess = int(request.form['guess'])
        session['attempts'] -= 1

        if guess == session['secret_number']:
            message = 'Correct! You guessed the number.'
            game_over = True
        elif guess < session['secret_number']:
            message = 'Too low!'
        else:
            message = 'Too high!'

        if session['attempts'] <= 0 and not game_over:
            message = f"No more attempts! The number was {session['secret_number']}."
            game_over = True

    return render_template('guess.html', message=message, game_over=game_over)

@app.route('/visual_quiz_setup', methods=['GET', 'POST'])
def visual_quiz_setup():
    if request.method == 'POST':
        category = request.form['category']
        session['category'] = category
        return redirect(url_for('visual_quiz'))
    return render_template('visual_quiz_setup.html')

@app.route('/visual_quiz', methods=['GET', 'POST'])
def visual_quiz():
    message = None  # Initialize message to None at the beginning of the function
    if 'category' not in session:
        return redirect(url_for('visual_quiz_setup'))

    category = session['category']
    images = image_dataset[category]
    image_info = session.get('current_image')

    # When a GET request, select a new random image
    if request.method == 'GET' or image_info is None:
        image_info = random.choice(images)
        session['current_image'] = image_info

    if request.method == 'POST':
        guess = request.form['guess'].lower()
        # Compare guess with the stored answer
        if guess == image_info['answer'].lower():
            message = "Correct! Try another one?"
            image_info = random.choice(images)  # Select a new random image and answer
            session['current_image'] = image_info
        else:
            message = f"Incorrect! It was {image_info['answer']}. Try another one?"

    return render_template('visual_quiz.html', message=message, src=image_info['url'])


if __name__ == '__main__':
    app.run(debug=False)

