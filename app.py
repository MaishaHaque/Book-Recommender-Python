from flask import Flask, render_template, request
import pickle
import numpy as np


popular_df = pickle.load(open('popularity.pkl','rb'))


books = pickle.load(open('books.pkl','rb'))
plot_df = pickle.load(open('plot.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values), 
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           rates = list(popular_df['no_of_ratings'].values),
                           rating = list(popular_df['avg_ratings'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('rec.html')


@app.route('/recommends',methods=['post'])
def recommended_books():
    user_input = request.form.get('user-input')
    index = np.where(plot_df.index == user_input)[0][0]
    similar_books=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1], reverse = True)[1:6]
    data = []
    for i in similar_books:
        item = []
        temp_df = books[books['Book-Title'] == plot_df.index[i[0]]]
        
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)

    return render_template('rec.html',data=data, user_input=user_input)

    

if __name__ == '__main__':
    app.run(debug = True)

