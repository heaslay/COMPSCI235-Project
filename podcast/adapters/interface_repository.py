from abc import ABC, abstractmethod
from typing import List, Set, Optional
from podcast.domainmodel.model import Podcast, Episode, Author, Category, User, Playlist, Review
from podcast.adapters.datareader.csvdatareader import CSVDataReader


class AbstractPodcastRepository(ABC):

    @abstractmethod
    def get_related_podcasts_by_id(self, podcast_id: int) -> List[Podcast]:
        pass

    @abstractmethod
    def get_podcast_by_id(self, podcast_id: int) -> Optional[Podcast]:
        pass

    @abstractmethod
    def get_all_podcasts(self) -> List[Podcast]:
        pass

    @abstractmethod
    def get_episode_by_id(self, episode_id: int) -> Optional[Episode]:
        pass

    @abstractmethod
    def get_all_episodes(self) -> List[Episode]:
        pass

    @abstractmethod
    def get_author_by_id(self, author_id: int) -> Optional[Author]:
        pass

    @abstractmethod
    def get_all_authors(self) -> Set[Author]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def get_all_categories(self) -> Set[Category]:
        pass

    @abstractmethod
    def add_podcast(self, podcast: Podcast):
        pass

    @abstractmethod
    def add_episode(self, episode: Episode):
        pass

    @abstractmethod
    def add_author(self, author: Author):
        pass

    @abstractmethod
    def add_category(self, category: Category):
        pass

    @abstractmethod
    def remove_podcast(self, podcast_id: int) -> bool:
        pass

    @abstractmethod
    def remove_episode(self, episode_id: int) -> bool:
        pass

    @abstractmethod
    def remove_author(self, author_id: int) -> bool:
        pass

    @abstractmethod
    def remove_category(self, category_id: int) -> bool:
        pass


class MemoryPodcastRepository(AbstractPodcastRepository):

    def __init__(self, csvdatareader):
        self._podcasts = csvdatareader.podcasts
        self._episodes = csvdatareader.episodes
        self._authors = csvdatareader.dataset_of_authors
        self._categories = csvdatareader.dataset_of_categories

    def get_related_podcasts_by_id(self, podcast_id: int) -> List[Podcast]:
        current_podcast = self.get_podcast_by_id(podcast_id)
        if not current_podcast:
            return []

        related_podcasts = []
        for podcast in self._podcasts:
            if podcast.id != podcast_id:
                if not set(current_podcast.categories).isdisjoint(podcast.categories):
                    related_podcasts.append(podcast)

        return related_podcasts[:4]



    def get_podcast_by_id(self, podcast_id: int) -> Optional[Podcast]:
        for podcast in self._podcasts:
            if podcast.id == podcast_id:
                return podcast
        return None

    def get_all_podcasts(self) -> List[Podcast]:
        return self._podcasts

    def get_episode_by_id(self, episode_id: int) -> Optional[Episode]:
        for episode in self._episodes:
            if episode.id == episode_id:
                return episode
        return None

    def get_all_episodes(self) -> List[Episode]:
        return self._episodes

    def get_author_by_id(self, author_id: int) -> Optional[Author]:
        for author in self._authors:
            if author.id == author_id:
                return author
        return None

    def get_all_authors(self) -> Set[Author]:
        return self._authors

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        for category in self._categories:
            if category.id == category_id:
                return category
        return None

    def get_all_categories(self) -> Set[Category]:
        return self._categories

    def add_podcast(self, podcast: Podcast):
        self._podcasts.append(podcast)

    def add_episode(self, episode: Episode):
        self._episodes.append(episode)

    def add_author(self, author: Author):
        self._authors.add(author)

    def add_category(self, category: Category):
        self._categories.add(category)

    def remove_podcast(self, podcast_id: int) -> bool:
        podcast_to_remove = self.get_podcast_by_id(podcast_id)
        if podcast_to_remove:
            self._podcasts.remove(podcast_to_remove)
            return True
        return False

    def remove_episode(self, episode_id: int) -> bool:
        episode_to_remove = self.get_episode_by_id(episode_id)
        if episode_to_remove:
            self._episodes.remove(episode_to_remove)
            return True
        return False

    def remove_author(self, author_id: int) -> bool:
        author_to_remove = self.get_author_by_id(author_id)
        if author_to_remove:
            self._authors.remove(author_to_remove)
            return True
        return False

    def remove_category(self, category_id: int) -> bool:
        category_to_remove = self.get_category_by_id(category_id)
        if category_to_remove:
            self._categories.remove(category_to_remove)
            return True
        return False
