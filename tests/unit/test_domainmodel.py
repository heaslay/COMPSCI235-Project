import pytest
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from datetime import datetime

def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.user) == "<User 1: shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.user = new_user
    assert my_subscription.user == new_user

    with pytest.raises(TypeError):
        my_subscription.user = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1

# TODO : Write Unit Tests for CSVDataReader, Episode, Review, Playlist classes
# Tests for Episode class
def test_episode_initialization(my_podcast):
    episode = Episode(1, my_podcast, "Episode 1", "audio.mp3", 300, "Description", "2024-08-05")
    assert episode.id == 1
    assert episode.podcast == my_podcast
    assert episode.title == "Episode 1"
    assert episode.audio == "audio.mp3"
    assert episode.length == 300
    assert episode.description == "Description"
    assert episode.pub_date == "2024-08-05"
    assert repr(episode) == "<Episode 1: Belongs to Joe Toste Podcast - Sales Training Expert>"

    with pytest.raises(ValueError):
        Episode(2, my_podcast, "", "audio.mp3", 300, "Description", "2024-08-05")

    with pytest.raises(ValueError):
        Episode(2, my_podcast, "Episode 2", "", 300, "Description", "2024-08-05")


def test_episode_setters(my_podcast):
    episode = Episode(1, my_podcast, "Episode 1", "audio.mp3", 300, "Description", "2024-08-05")
    episode.title = "New Title"
    assert episode.title == "New Title"

    episode.audio = "new_audio.mp3"
    assert episode.audio == "new_audio.mp3"

    episode.length = 350
    assert episode.length == 350

    episode.description = "New Description"
    assert episode.description == "New Description"

    episode.pub_date = "2024-08-06"
    assert episode.pub_date == "2024-08-06"

    with pytest.raises(ValueError):
        episode.title = ""

    with pytest.raises(ValueError):
        episode.audio = ""

    with pytest.raises(ValueError):
        episode.pub_date = ""


def test_review_initialization(my_podcast, my_user):
    review = Review(1, my_podcast, my_user, 5, "Great episode!")
    assert review.id == 1
    assert review.came == my_podcast
    assert review.user == my_user
    assert review.rating == 5
    assert review.content == "Great episode!"
    assert repr(review) == "<Review 1>: Wrote from shyamli>"

    with pytest.raises(ValueError):
        Review(2, my_podcast, my_user, -1)

    with pytest.raises(TypeError):
        Review(2, "not a podcast", my_user, 5)

    with pytest.raises(TypeError):
        Review(2, my_podcast, "not a user", 5)


def test_review_setters(my_podcast, my_user):
    review = Review(1, my_podcast, my_user, 5, "Great episode!")
    review.rating = 4
    assert review.rating == 4

    review.content = "Good episode"
    assert review.content == "Good episode"

    with pytest.raises(ValueError):
        review.rating = -1

    with pytest.raises(ValueError):
        review.content = ""


def test_playlist_initialization(my_user):
    playlist = Playlist(1, my_user, "My Playlist")
    assert playlist.id == 1
    assert playlist.user == my_user
    assert playlist.title == "My Playlist"
    assert repr(playlist) == "<Playlist 1: Owns by shyamli>"

    with pytest.raises(ValueError):
        Playlist(2, my_user, "")

    with pytest.raises(ValueError):
        Playlist(2, my_user, 123)


def test_playlist_setters(my_user):
    playlist = Playlist(1, my_user, "My Playlist")
    playlist.title = "New Playlist"
    assert playlist.title == "New Playlist"

    new_user = User(2, "asma", "pw67890")
    playlist.user = new_user
    assert playlist.user == new_user

    with pytest.raises(ValueError):
        playlist.title = ""

    with pytest.raises(TypeError):
        playlist.user = "not a user"

def test_csv_data_reader():

    reader = CSVDataReader('podcasts.csv', 'episodes.csv')
    reader.read_csv_data()
    assert len(reader.dataset_of_authors) > 0
    assert len(reader.podcasts) > 0
    assert len(reader.episodes) > 0

    author_names = [author.name for author in reader.dataset_of_authors]
    assert len(author_names) == len(set(author_names)), "Duplicate authors found."

    for podcast in reader.podcasts:
        categories = [cat.name for cat in podcast.categories]
        assert len(categories) == len(set(categories)), f"Duplicate categories found in podcast {podcast.title}"

    # Validate the first podcast
    podcast = reader.podcasts[0]
    assert isinstance(podcast, Podcast), "First item in podcasts is not a Podcast object."
    assert isinstance(podcast.author, Author), "Podcast author is not an Author object."
    assert len(podcast.categories) > 0, "Podcast has no categories."

    # Validate the first episode
    episode = reader.episodes[0]
    assert isinstance(episode, Episode), "First item in episodes is not an Episode object."
    assert isinstance(episode.podcast, Podcast), "Episode's podcast is not a Podcast object."
    assert episode.podcast in reader.podcasts, "Episode's podcast is not in the podcasts list."

    # Test empty strings for author and audio link are handled
    assert episode.title != "", "Episode title should not be empty."
    assert episode.audio != "N/A", "Audio link should be correctly set."

    # Test error handling
    # Test that the method raises a FileNotFoundError if the file does not exist
    with pytest.raises(FileNotFoundError):
        invalid_reader = CSVDataReader('invalid_path/podcasts.csv', 'invalid_path/episodes.csv')
        invalid_reader.read_csv_data()

    # I assume these are debug statements, I will leave them here for now - Isaac.
    # print(reader.podcasts)
    # print(reader.episodes)
    # print(len(reader.podcasts))
    # print(len(reader.episodes))