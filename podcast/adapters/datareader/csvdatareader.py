import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category


class CSVDataReader:
    def __init__(self, podcasts_file, episodes_file):
        self.podcasts_filename = podcasts_file
        self.episodes_filename = episodes_file
        self.podcasts = []
        self.episodes = []
        self.dataset_of_authors = set()
        self.dataset_of_categories = set()
        self.author_counter = 0
        self.category_counter = 0

    def read_csv_data(self):
        self.podcasts_filename = self.get_absolute_path(self.podcasts_filename)
        self.episodes_filename = self.get_absolute_path(self.episodes_filename)

        # print(f'Absolute podcast path: {self.podcasts_filename}')
        # print(f'Absolute episodes path: {self.episodes_filename}')
        # if not os.path.exists(self.podcasts_filename):
        #     raise FileNotFoundError(f"Podcast not found: {self.podcasts_filename}")
        # if not os.path.exists(self.episodes_filename):
        #     raise FileNotFoundError(f"Episode not found: {self.episodes_filename}")

        self.read_podcasts()
        self.read_episodes()

    def get_absolute_path(self, relative_path):                # get absolute path from content root path
        script_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
        absolute_path = os.path.abspath(os.path.join(project_root, relative_path))
        return absolute_path

    def read_podcasts(self):            # read all the podcast data and create object
        with open(self.podcasts_filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # row_count = 0
            for row in reader:
                # row_count += 1
                # Create author and add to list, set default name if empty
                author_name = row['author'].strip() if row['author'].strip() else "Unknown Author"
                author = self.create_author(author_name)

                # Create categories and add to list
                categories = self.create_categories(row['categories'])

                # Create podcast and add to list
                self.create_podcast(row, author, categories)

            # print(f"Total podcasts read: {row_count}")
            # print(f"Total podcasts stored: {len(self.podcasts)}")

    def read_episodes(self):
        with open(self.episodes_filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Find the corresponding podcast by its ID
                podcast_id = int(row['podcast_id'])
                correspodcast = next((p for p in self.podcasts if p.id == podcast_id), None)

                # Create episode and add to list
                self.create_episode(row, correspodcast)

            # print(f"Total episodes read: {row_count}")
            # print(f"Total episodes stored: {len(self.episodes)}")

    def create_author(self, author_name):
        author = next((a for a in self.dataset_of_authors if a.name == author_name), None)
        if not author:
            self.author_counter += 1
            author = Author(self.author_counter, author_name)
            self.dataset_of_authors.add(author)
        return author

    def create_categories(self, categories_str):
        categories = set()
        for cat_name in categories_str.split('|'):      # Split categories
            cat_name = cat_name.strip()
            category = next((c for c in self.dataset_of_categories if c.name == cat_name), None)
            if not category:
                self.category_counter += 1
                category = Category(self.category_counter, cat_name)
                self.dataset_of_categories.add(category)
            categories.add(category)        # add categories to the podcast
        return categories

    def create_podcast(self, row, author, categories):
        podcast = Podcast(
            int(row['id']), author, row['title'], row['image'],
            row['description'], row['website'], int(row['itunes_id']),
            row['language']
        )
        for category in categories:
            podcast.add_category(category)
        self.podcasts.append(podcast)

    def create_episode(self, row, correspodcast):
        audio_link = row['audio'] if row['audio'].strip() else "N/A"    # if there is no link, default is N/A

        episode = Episode(
            int(row['id']), correspodcast, row['title'], audio_link,
            int(row['audio_length']), row['description'], row['pub_date']
        )
        self.episodes.append(episode)


# if __name__ == "__main__":
#     csv_reader = CSVReader('../../podcasts.csv', 'episodes.csv')
#     csv_reader.read_csv()
#     count = 0
#
#     # with open('output.txt', 'w', encoding='utf-8') as f:
#     #     f.write("Podcasts:\n")
#     #     for podcast in csv_reader.podcasts:
#     #         count += 1
#     #         f.write(f"{count} {podcast}\n")
#     #
#     #     count = 0
#
#         # f.write("\nEpisodes:\n")
#         # for episode in csv_reader.episodes:
#         #     count += 1
#         #     f.write(f"{count} {episode}\n")
#
#     # print("Podcasts:")
#     # for podcast in csv_reader.podcasts:
#     #     print(podcast)
#
#     # print("Episodes")
#     # for Episodes in csv_reader.episodes:
#     #     print(Episodes)
#
#     # print("Authors:")
#     # for author in csv_reader.authors:
#     #     print(author)
#
#     print("Categories:")
#     for category in csv_reader.categories:
#         print(category)
#
