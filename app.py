from flask import Flask, render_template, request
import pickle
import numpy as np


popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values)
    )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input').strip()  

    data = []  

    
    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
            for _, row in temp_df.iterrows():
                item = [
                    row['Book-Title'],
                    row['Book-Author'],
                    row['Image-URL-M']
                ]
                data.append(item)

    
    elif user_input in books['Book-Author'].values:
        # Filter books by author
        author_books = books[books['Book-Author'] == user_input].drop_duplicates('Book-Title')
        for _, row in author_books.iterrows():
            item = [
                row['Book-Title'],
                row['Book-Author'],
                row['Image-URL-M']
            ]
            data.append(item)

    
    if not data:
        return render_template('recommend.html', error="No matching book or author found. Please try again.")

    # If recommendations are found, display them
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
