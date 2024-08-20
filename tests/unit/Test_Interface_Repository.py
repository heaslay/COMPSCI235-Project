import pytest
from podcast.adapters.interface_repository import MemoryPodcastRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.domainmodel.model import Podcast, Author, Episode, Category


@pytest.fixture
def memory_repository():
    csvdatareader = CSVDataReader('podcasts.csv', 'episodes.csv')
    repository = MemoryPodcastRepository(csvdatareader)
    # empty database
    # repository._podcasts = []
    # repository._episodes = []
    # repository._authors = set()
    # repository._categories = set()

    return repository


@pytest.fixture
def test_data():
    base_id = 10000
    author = Author(base_id, "Test Author")
    podcast = Podcast(base_id, author, "Test Podcast")
    episode = Episode(base_id, podcast, "Test Episode", "audio.mp3")
    category = Category(base_id, "Test Category")
    return base_id, author, podcast, episode, category


def test_add_and_get_podcast(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_podcast(podcast)
    assert memory_repository.get_podcast_by_id(base_id) == podcast


def test_remove_podcast(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_podcast(podcast)
    memory_repository.remove_podcast(base_id)
    assert memory_repository.get_podcast_by_id(base_id) is None


def test_get_all_podcasts(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_podcast(podcast)
    all_podcasts = memory_repository.get_all_podcasts()
    print("First 5 Podcasts:", all_podcasts[:5])
    assert podcast in all_podcasts


def test_add_and_get_episode(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_episode(episode)
    assert memory_repository.get_episode_by_id(base_id) == episode


def test_remove_episode(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_episode(episode)
    memory_repository.remove_episode(base_id)
    assert memory_repository.get_episode_by_id(base_id) is None


def test_get_all_episodes(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_episode(episode)
    all_episodes = memory_repository.get_all_episodes()
    print("First 5 Episodes:", all_episodes[:5])
    assert episode in all_episodes


def test_add_and_get_author(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_author(author)
    assert memory_repository.get_author_by_id(base_id) == author


def test_remove_author(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_author(author)
    memory_repository.remove_author(base_id)
    assert memory_repository.get_author_by_id(base_id) is None


def test_get_all_authors(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_author(author)
    all_authors = memory_repository.get_all_authors()
    print("First 5 Authors:", list(all_authors)[:5])
    assert author in all_authors


def test_add_and_get_category(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_category(category)
    assert memory_repository.get_category_by_id(base_id) == category


def test_remove_category(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_category(category)
    memory_repository.remove_category(base_id)
    assert memory_repository.get_category_by_id(base_id) is None


def test_get_all_categories(memory_repository, test_data):
    base_id, author, podcast, episode, category = test_data
    memory_repository.add_category(category)
    all_categories = memory_repository.get_all_categories()
    print("First 5 Categories:", list(all_categories)[:5])
    assert category in all_categories

def test_get_related_podcasts_by_id(memory_repository):
    print(memory_repository.get_related_podcasts_by_id(1))

if __name__ == "__main__":
    pytest.main()
