from imports import *


def read_csv(file_name):
    """
    reads a csv file and returns a list of dictionaries
    """
    with open(file_name, 'r', errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        return data


def write_to_csv(data, name):
    """
    writes a list of dictionaries to csv
    """
    with open('assets/' + name + '.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        headers = list(data[0].keys())
        writer.writerow(headers)
        for x in range(len(data)):
            writer.writerow(list(data[x].values()))


def save_as_json(data, file_name):
    """
    saves a list of dictionaries to json
    """
    with open('assets/' + file_name + '.json', 'w', encoding='utf-8') as f:
        json_str = json.dumps(data, indent=4)
        f.write(json_str)


def save_recommendation_as_json(song, predictions, sim_scores, file_name):
    """
    saves recommendations in a json file
    """
    with open('assets/' + file_name + '.json', 'w', encoding='utf-8') as f:
        result = {'id': song['id'], 'name': song['name'], 'recommendations': predictions,
                  'similarity_scores': sim_scores}
        json_str = json.dumps(result)
        f.write(json_str)


def append_recommendation_as_json(song, predictions, sim_scores, file_name):
    """
    appends recommendations to a json file
    """
    with open('assets/' + file_name + '.json', 'a', encoding='utf-8') as f:
        result = {'id': song['id'], 'name': song['name'], 'recommendations': predictions,
                  'similarity_scores': sim_scores}
        json_str = json.dumps(result)
        f.write(json_str + ',\n')


def save_artists_genres_csv(data, name):
    """
    saves genres of artists in an {artist : genre} dictionary
    """
    with open(name + '.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        header = ['artist', 'genre']
        writer.writerow(header)
        for key, value in data.items():
            writer.writerow([key, value])
