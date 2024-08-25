import pytest
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from datetime import datetime

@pytest.fixture
def csv_data_reader():
    return CSVDataReader('podcasts.csv', 'episodes.csv')


def test_csv_data_reader(csv_data_reader):
    # print前5个Podcasts
    for podcast in csv_data_reader.podcasts[:5]:
        print(f"Podcast: {podcast.title}, {podcast.id}")
        print("  First 5 Categories:", podcast.categories)
        print("  First 5 Episodes:", podcast.episodes)
        print()

    episodes_for_podcast_4 = [episode for episode in csv_data_reader.episodes if episode.belong.id == 4]
    print("Episodes for Podcast ID 4:")
    for episode in episodes_for_podcast_4:
        print(f"  Episode ID: {episode.id}, Title: {episode.title}")
    print()


def test_check_podcast_categories_and_episodes(csv_data_reader):
    # Check if the podcast has the correct categories and episodes added
    podcast_ids_to_check = [1, 5, 10, 20]
    for podcast_id in podcast_ids_to_check:
        podcast = next((p for p in csv_data_reader.podcasts if p.id == podcast_id), None)
        assert podcast is not None, f"Podcast ID {podcast_id} not found."

        assert podcast.categories, f"Podcast ID {podcast_id} has no categories."

        assert podcast.episodes, f"Podcast ID {podcast_id} has no episodes."

        print(f"Podcast ID {podcast_id}: {podcast.title}")
        print(f"  Categories: {podcast.categories}")
        print(f"  Episodes: {podcast.episodes}")





if __name__ == "__main__":
    pytest.main()