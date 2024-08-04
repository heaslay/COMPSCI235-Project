from __future__ import annotations


def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)


class Podcast:
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
        self._username = username.lower().strip()
        self._password = password
        self._subscription_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class Episode:
    def __init__(self, episode_id: int, belong: Podcast, title: str = "Untitled", audio: str = "", length: int = 0, description: str = "", date: str = ""):
        validate_non_negative_int(episode_id)
        validate_non_empty_string(title, "Episode title")
        validate_non_negative_int(length)
        if not isinstance(belong, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = episode_id
        self._belong = belong
        self._title = title.strip()
        self._audio = audio
        self._length = length
        self._description = description
        self._date = date

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def belong(self) -> Podcast:
        return self._belong
    
    @belong.setter
    def belong(self, new_belong: Podcast):
        if not isinstance(new_belong, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._belong = new_belong
    
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Episode title")
        self._title = new_title.strip()

    @property
    def audio(self) -> str:
        return self._audio
    
    @audio.setter
    def audio(self, new_audio: str):
        validate_non_empty_string(new_audio, "Episode audio")
        self._audio = new_audio
    
    @property
    def length(self) -> int:
        return self._length
    
    @length.setter
    def length(self, new_length: int):
        validate_non_negative_int(new_length)
        self._length = new_length

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Episode's description")
        self._description = new_description

    @property
    def date(self) -> str:
        return self._date
    
    @date.setter
    def date(self, new_date: str):
        validate_non_empty_string(new_date, "Episode published date")
        self._date = new_date

    def __repr__(self) -> str:
        return f"<Episode {self.id}: Belongs to {self.belong.title}>"
    
    def __eq__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.id == other.id
    
    def __lt__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.id < other.id
    
    def __hash__(self):
        return hash((self.id, self.belong))


class Review:
    def __init__(self, review_id: int, came: Podcast or Episode, writer: User, rating: int, content: str = ""): # type: ignore
        validate_non_negative_int(review_id)
        validate_non_negative_int(rating)
        if isinstance(came, Podcast):
            if not isinstance(came, Podcast):
                raise TypeError("Review must be from Podcast or Episode object.")
        else:
            if not isinstance(came, Episode):
                raise TypeError("Review must be from Podcast or Episode object.")
        self._id = review_id
        self._came = came
        self._writer = writer
        self._rating = rating
        self._content = content

    @property
    def id(self) -> int:
        return self.id
    
    @property
    def came(self) -> Podcast:
        return self._came
    
    def came(self) -> Episode:
        return self._came
        
    @property
    def writer(self) -> User:
        return self._writer
    
    @property
    def rating(self) -> int:
        return self._rating
    
    @rating.setter
    def rating(self, new_rating: int):
        validate_non_negative_int(new_rating)
        self._rating = new_rating
    
    @property
    def content(self) -> str:
        return self._content
    
    @content.setter
    def content(self, new_content: str):
        if not isinstance(new_content, str):
            validate_non_empty_string(new_content, "Review's content")
        self._content = new_content

    def __repr__(self) -> str:
        return f"<Review {self.id}>: Wrote from {self.writer}>"
    
    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.id == other.id and self.writer == other.writer
    
    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self.id < other.id
    
    def __hash__(self):
        return hash((self.id, self.writer))


class Playlist:
    def __init__(self, playlist_id: int, owner: User, title: str = "Untitle"):
        validate_non_negative_int(playlist_id)
        validate_non_empty_string(title, "Playlist's title")
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        self._id = playlist_id
        self._owner = owner
        self._title = title.strip()

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def owner(self) -> User:
        return self._owner
    
    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Playlist's title")
        self._title = new_title

    def __repr__(self) -> str:
        return f"<Playlist {self.id}: Owns by {self.owner.username}>"
    
    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.id == other.id
    
    def __lt__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.id < other.id
    
    def __hash__(self):
        return hash((self.id))