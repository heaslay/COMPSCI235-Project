import pytest
from datetime import datetime

from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.interface_repository import MemoryPodcastRepository
from podcast.podcasts import services as pod_services
from typing import List
from podcast.domainmodel.model import Podcast, Author, Episode, Category
import random

@pytest.fixture
def in_interface_repo():
    csvdatareader = CSVDataReader('podcasts.csv', 'episodes.csv')
    repository = MemoryPodcastRepository(csvdatareader)
    return repository



def test_get_related_podcasts_by_id(in_interface_repo):
    podcast_id = 27
    category = "Education"
    relate_pod = pod_services.get_related_podcasts_by_id(podcast_id, in_interface_repo)
    for podcast in relate_pod:
        assert podcast.id != 23
        assert "Education" in podcast.categories


def test_get_podcast_by_id(in_interface_repo):
    podcast_id = 22
    podcast = pod_services.get_podcast_by_id(podcast_id, in_interface_repo)
    assert podcast.id == 22
    
def test_get_all_podcasts(in_interface_repo):
    randnum = random.randint(1, 1000)
    podcast1 = pod_services.get_podcast_by_id(randnum)
    
    podcasts = pod_services.get_all_podcasts(in_interface_repo)
    assert len(podcasts) == 1000
    assert podcast1.id == podcasts[randnum].id
    assert podcasts[randnum].title == podcast1.title
    assert podcast1.author.name == podcasts[randnum].author.name
    assert podcasts[randnum].image == podcast1.image
    assert podcasts[randnum].website == podcast1.website
    assert podcasts[randnum].itunes_id == podcast1.itunes_id
    assert podcasts[randnum].description == podcast1.description
    length = len(podcasts[randnum].episodes)
    for index in range(0, length):
        assert podcast1.episodes[index].id == podcasts[randnum].episodes[index].id
    for index in range(0, length):
        assert podcast1.categories[index].id == podcasts[randnum].categories[index].id
        
    
def test_get_episode_by_id(in_interface_repo):
    episode_id = 24
    episode = pod_services.get_episode_by_id(episode_id, in_interface_repo)
    assert episode.id == 24

