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
            movie_name = query_string[entity['startIndex']:entity['endIndex'] + 1]
    return movie_name


def retrieve_rr(movie_name, flag):
    movie_info = imdb_obj.search_movie(movie_name)
    return_value = ""
    for idx in range(len(movie_info)):
        try:
            movie = imdb_obj.get_movie(movie_info[idx].movieID)
            if flag == "rating":
                rating = movie.get('rating')
                if rating:
                    return_value += movie.get('long imdb title') + "; Rating: " + str(rating) + ", votes: "+ str(movie.get('votes')) + "\n"
            elif flag == "director":
                director = movie.get('director')
                director = [i.get('name') for i in director]
                if director:
                    if len(director) == 1:
                        return_value += ", ".join(director) + " is director of " + movie.get('long imdb title') + "\n"
                    else:
                        return_value += ", ".join(director) + " are directors of " + movie.get('long imdb title') + "\n"
            elif flag == "cast":
                cast = movie.get('cast')
                cast = [i.get('name') for i in cast]
                return_value += "Cast of " + movie.get('long imdb title') + ": " + ', '.join(cast) + "\n\n"
        except Exception as e:
            print(e)
        if idx == 3:
            break
    return return_value


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
                bot_reply(review)
            else:
                bot_reply("I couldn't get which movie's review you want!")
        elif result['topScoringIntent']['intent'] == "FindRating":
            movie_name = retrieve_entity(result)
            if movie_name:
                rating = retrieve_rr(movie_name, 'rating')
                bot_reply(rating)
            else:
                bot_reply("I couldn't get which movie's rating you want!")
        elif result['topScoringIntent']['intent'] == "FindDirector":
            movie_name = retrieve_entity(result)
            if movie_name:
                director = retrieve_rr(movie_name, 'director')
                bot_reply(director)
            else:
                bot_reply("I couldn't get which movie's director you want!")
        elif result['topScoringIntent']['intent'] == "FindCast":
            movie_name = retrieve_entity(result)
            if movie_name:
                cast = retrieve_rr(movie_name, 'cast')
                bot_reply(cast)
            else:
                bot_reply("I couldn't get which movie's cast you want!")
        elif result['topScoringIntent']['intent'] == "Greet":
            bot_reply("Hello there!\nHere's what I can do for you: I can find you information like ratings, director, cast of any movie! Try me!")
        elif result['topScoringIntent']['intent'] == "None":
            bot_reply("I didn't understand your need! \nHere's what I can do for you: I can find you information like ratings, director, cast of any movie! Try me!")
