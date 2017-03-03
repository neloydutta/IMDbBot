import os
import requests
import json
import imdb

def bot_reply(message):
    print(message)

imdb_obj = imdb.IMDb()

def retrieve_entity(result):
    entities = result['entities']
    movie_score = -10
    movie_name = None
    for entity in entities:
        if entity['type'] == "builtin.encyclopedia.film.film":
            movie_name = entity['entity']
            break
        elif entity['type'] == "MovieName" and movie_score < entity['score']:
            movie_score = entity['score']
            movie_name = query_string[entity['startIndex']:entity['endIndex']+1]
    return movie_name


def retrieve_rr(movie_name, flag):
    movie_info = imdb_obj.search_movie(movie_name)
    movie_info = movie_info[0]
    print movie_info['rating']
    return "dummyreturn"

if __name__ == "__main__":
    while True:
        query_string = raw_input("Enter your message: ")
        response = requests.get("https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/66bfac41-ed46-4ea7-80f4"
                                "-9752234babb2?subscription-key=4fbd2c17c3ee4eb2b94c3563277c4574&q=" + query_string +
                                "&timezoneOffset=0.0&verbose=true")
        result = json.loads(response.text)
        print(result)
        if result['topScoringIntent']['intent'] == "FindReview":
            movie_name = retrieve_entity(result)
            if movie_name:
                review = retrieve_rr(movie_name, 'review')
                bot_reply("movie review, " + review)
            else:
                bot_reply("I couldn't get which movie's review you want!")
        elif result['topScoringIntent']['intent'] == "FindRating":
            movie_name = retrieve_entity(result)
            if movie_name:
                rating = retrieve_rr(movie_name, 'rating')
                bot_reply("movie review, " + rating)
            else:
                bot_reply("I couldn't get which movie's rating you want!")
        elif result['topScoringIntent']['intent'] == "Greet":
            bot_reply("greet")
        elif result['topScoringIntent']['intent'] == "None":
            bot_reply("none")
