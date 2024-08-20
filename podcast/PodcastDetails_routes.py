from flask import Blueprint, render_template, request, redirect, url_for
import random
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.interface_repository import MemoryPodcastRepository

podcast_bp = Blueprint('podcast_bp', __name__)
csv_reader = CSVDataReader('podcasts.csv', 'episodes.csv')
repository = MemoryPodcastRepository(csv_reader)


@podcast_bp.route('/podcast/<int:podcast_id>', methods=['GET', 'POST'])
def podcast_details(podcast_id):
    podcast = repository.get_podcast_by_id(podcast_id)
    if podcast is None:
        return "Podcast not found", 404

    total_pages = (len(podcast.episodes) + 5) // 6
    current_page = int(request.args.get('page', 1))

    related_podcasts = repository.get_related_podcasts_by_id(podcast_id)
    if len(related_podcasts) > 4:
        related_podcasts = random.sample(related_podcasts, 4)
    else:
        random.shuffle(related_podcasts)

    return render_template('podcastDescription.html',
                           podcast=podcast,
                           current_page=current_page,
                           total_pages=total_pages,
                           related_podcasts=related_podcasts)

@podcast_bp.route('/change_batch/<int:podcast_id>', methods=['POST'])
def change_batch(podcast_id):
    return redirect(url_for('podcast_bp.podcast_details', podcast_id=podcast_id))


@podcast_bp.route('/episode/<int:episode_id>')
def play_episode(episode_id):
    episode = repository.get_episode_by_id(episode_id)
    if episode is None:
        return "Episode not found", 404
    return render_template('episode.html', episode=episode)
