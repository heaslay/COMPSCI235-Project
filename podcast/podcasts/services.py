from typing import List, Iterable
from podcast.adapters.interface_repository import AbstractPodcastRepository
from podcast.domainmodel.model import Podcast, Episode, Author, Category, User, Playlist, Review


class NonExistentPodcastException(Exception):
    pass


def get_related_podcasts_by_id(podcast_id: int, repo: AbstractPodcastRepository):
    podcast = repo.get_related_podcasts_by_id(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException
    return podcast

def get_podcast_by_id(podcast_id: int, repo: AbstractPodcastRepository):
    podcast = repo.get_podcast_by_id(podcast_id)
    if podcast is None:
        raise NonExistentPodcastException
    return podcast

def get_all_podcasts(repo: AbstractPodcastRepository):
    podcasts = repo.get_all_podcasts()
    return podcasts

def get_episode_by_id(episode_id: int, repo: AbstractPodcastRepository):
    episode = repo.get_episode_by_id(episode_id)
    if episode is None:
        raise NonExistentPodcastException
    return episode


# ============================================
# Functions to convert model entities to dicts
# ============================================

# def podcast_to_dict(podcast: Podcast):
#     podcast_dict = {
#     'id': podcast.id,
#     'author': author_to_dict(podcast.author),
#     'title': podcast.title,
#     'image': podcast.image,
#     'description': podcast.description,
#     'website': podcast.website, 
#     'itunes_id': podcast.itunes_id, 
#     'language': podcast.language,
#     'categories': categories_to_dict(podcast.categories),
#     'episodes': episodes_to_dict(podcast.episodes)
#     }
#     return podcast_dict

# def podcasts_to_dict(podcasts: List[Podcast]):
#     return [podcast_to_dict(podcast) for podcast in podcasts]


# def episode_to_dict(episode: Episode):
#     episode_dict = {
#         'episode_id': episode.id,
#         'podcast': podcast_to_dict(episode.podcast),
#         'title': episode.title, 
#         'audio': episode.audio, 
#         'length': episode.length, 
#         'description': episode.description, 
#         'pub_date': episode.pub_date
#     }
#     return episode_dict

# def episodes_to_dict(episodes: List[Episode]):
#     return [episode_to_dict(episode) for episode in episodes]

# def author_to_dict(author: Author):
#     author_dict = {
#         'author_id': author.id, 
#         'name': author.name
#     }
#     return author_dict

# def category_to_dict(category: Category):
#     category_dict ={
#         'category_id': category.id, 
#         'name': category.name
#     }
#     return category_dict

# def categories_to_dict(categories: List[Category]):
#     return [category_to_dict(category) for category in categories]
