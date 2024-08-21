import os
from flask import Blueprint, render_template, request, url_for, redirect
import math
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.interface_repository import MemoryPodcastRepository
import random

podcasts_blueprint = Blueprint('podcasts_bp', __name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
podcasts_csv_path = os.path.join(base_dir, '..', 'adapters', 'data', 'podcasts.csv')
episodes_csv_path = os.path.join(base_dir, '..', 'adapters', 'data', 'episodes.csv')

csv_reader = CSVDataReader(podcasts_csv_path, episodes_csv_path)
repository = MemoryPodcastRepository(csv_reader)

@podcasts_blueprint.route('/podcasts', methods=['GET'])
def home():
    current_page = int(request.args.get('page', 1))
    all_podcasts = repository.get_all_podcasts()

    podcasts_per_page = 6
    total_podcasts = len(all_podcasts)
    total_pages = math.ceil(total_podcasts / podcasts_per_page)
    
    start_index = (current_page - 1) * podcasts_per_page
    end_index = start_index + podcasts_per_page

    podcasts_on_page = all_podcasts[start_index:end_index]

    return render_template(
        'podcastLibrary/library.html', 
        podcasts=podcasts_on_page, 
        current_page=current_page, 
        total_pages=total_pages
    )


@podcasts_blueprint.route('/description/<int:podcast_id>', methods=['GET'])
def show_description(podcast_id):
    # Retrieve the specific podcast by ID
    podcast = repository.get_podcast_by_id(podcast_id)
    if podcast is None:
        return "Podcast not found", 404

    # Retrieve related podcasts (modify this logic based on your actual implementation)
    related_podcasts = repository.get_related_podcasts_by_id(podcast_id)

    # Determine current page and total pages for pagination (example logic)
    episodes_per_page = 5
    total_pages = (len(podcast.episodes) + episodes_per_page - 1) // episodes_per_page
    current_page = int(request.args.get('page', 1))
    
    # Slice the episodes list based on the current page
    start_idx = (current_page - 1) * episodes_per_page
    end_idx = start_idx + episodes_per_page
    displayed_episodes = podcast.episodes[start_idx:end_idx]

    # Pass the podcast, displayed episodes, related podcasts, and pagination data to the template
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
    # Logic to change the batch of related podcasts or any other action
    # For simplicity, let's assume we're shuffling the related podcasts
    related_podcasts = repository.get_related_podcasts_by_id(podcast_id)
    random.shuffle(related_podcasts)

    # Redirect back to the podcast description page
    return redirect(url_for('podcasts_bp.show_description', podcast_id=podcast_id))
