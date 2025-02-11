import os
from flask import Blueprint, render_template, request, url_for, redirect
import math
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.interface_repository import MemoryPodcastRepository 
import podcast.podcasts.services as services
import random
from datetime import date, datetime

podcasts_blueprint = Blueprint('podcasts_bp', __name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
podcasts_csv_path = os.path.join(base_dir, '..', 'adapters', 'data', 'podcasts.csv')
episodes_csv_path = os.path.join(base_dir, '..', 'adapters', 'data', 'episodes.csv')


csv_reader = CSVDataReader(podcasts_csv_path, episodes_csv_path)
repository = MemoryPodcastRepository(csv_reader)

@podcasts_blueprint.route('/podcasts', methods=['GET'])
def home():
    current_page = int(request.args.get('page', 1))
    all_podcasts = services.get_all_podcasts(repository)

    # Sorting the podcast list by title
    sorted_podcasts = sorted(all_podcasts, key=lambda podcast: podcast.title)

    podcasts_per_page = 6
    total_podcasts = len(sorted_podcasts)
    total_pages = math.ceil(total_podcasts / podcasts_per_page)
    
    start_index = (current_page - 1) * podcasts_per_page
    end_index = start_index + podcasts_per_page

    podcasts_on_page = sorted_podcasts[start_index:end_index]

    return render_template(
        'podcastLibrary/library.html', 
        podcasts=podcasts_on_page, 
        current_page=current_page, 
        total_pages=total_pages
    )


@podcasts_blueprint.route('/description/<int:podcast_id>', methods=['GET'])
def show_description(podcast_id):
    # Retrieve the specific podcast by ID
    podcast = services.get_podcast_by_id(podcast_id, repository)
    if podcast is None:
        return "Podcast not found", 404

    # Retrieve related podcasts (modify this logic based on your actual implementation)
    related_podcasts = services.get_related_podcasts_by_id(podcast_id, repository)
    if len(related_podcasts) > 6:
        related_podcasts = random.sample(related_podcasts, 6)
    else:
        random.shuffle(related_podcasts)

    sorted_episodes = sorted(podcast.episodes, key=lambda epi: epi.pub_date) 

    # Determine current page and total pages for pagination
    episodes_per_page = 5    
    current_page = int(request.args.get('page', 1))

    total_pages = math.ceil(len(sorted_episodes) / episodes_per_page )

    displayed_episodes = sorted_episodes

    return render_template(
        'description/podcastDescription.html',
        podcast=podcast,
        episodes=displayed_episodes,
        related_podcasts=related_podcasts,
        current_page=current_page,
        total_pages=total_pages
    )

@podcasts_blueprint.route('/change_batch/<int:podcast_id>', methods=['POST'])
def change_batch(podcast_id):
    related_podcasts = services.get_related_podcasts_by_id(podcast_id, repository)
    random.shuffle(related_podcasts)

    return redirect(url_for('podcasts_bp.show_description', podcast_id=podcast_id))

@podcasts_blueprint.route('/play/<int:episode_id>')
def play_episode(episode_id):
    episode = services.get_episode_by_id(episode_id, repository)
    if not episode:
        return redirect(url_for('podcasts_bp.show_description'))

    podcast = episode.podcast

    return render_template('description/play_episode.html', episode=episode, podcast=podcast)


@podcasts_blueprint.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    current_page = int(request.args.get('page', 1))
    podcasts_per_page = 6

    if not query:
        return redirect(url_for('podcasts_bp.home'))

    all_podcasts = services.get_all_podcasts(repository)
    search_results = [
        podcast for podcast in all_podcasts
        if query.lower() in podcast.title.lower() or query.lower() in podcast.description.lower()
    ]

    total_results = len(search_results)
    total_pages = (total_results + podcasts_per_page - 1) // podcasts_per_page

    start_index = (current_page - 1) * podcasts_per_page
    end_index = start_index + podcasts_per_page
    paginated_results = search_results[start_index:end_index]

    return render_template(
        'search_results.html',
        query=query,
        podcasts=paginated_results,
        current_page=current_page,
        total_pages=total_pages
    )
