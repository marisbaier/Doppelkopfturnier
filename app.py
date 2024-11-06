from flask import Flask, render_template, request, redirect, url_for
from tournament import DoppelkopfTournament, session, Player, Match, initialize_players

app = Flask(__name__)
tournament = DoppelkopfTournament()
initialize_players()

@app.route('/')
def index():
    players = tournament.get_rankings()
    ranked_players = []
    for rank, player in enumerate(players, 1):
        rank_image = tournament.get_rank_image(player.rating)
        ranked_players.append((rank, player, rank_image))
    return render_template('index.html', ranked_players=ranked_players)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        tournament.add_player(name)
        return redirect(url_for('index'))
    return render_template('add_player.html')

@app.route('/add_result', methods=['GET', 'POST'])
def add_result():
    if request.method == 'POST':
        table_results = [
            request.form['player1'],
            request.form['player2'],
            request.form['player3'],
            request.form['player4']
        ]
        tournament.update_scores(table_results)
        return redirect(url_for('index'))
    
    players_with_rank_image = []
    players = session.query(Player).all()
    for player in players:
        rank_image = tournament.get_rank_image(player.rating)
        players_with_rank_image.append((player, rank_image))
    return render_template('add_result.html', players_with_rank_images=players_with_rank_image)

@app.route('/player_history/<int:player_id>')
def player_history(player_id):
    # Hole den Spieler anhand der ID
    player = session.query(Player).get(player_id)
    
    if player:
        # Hole alle Spiele des Spielers
        matches = session.query(Match).filter_by(player_id=player_id).order_by(Match.timestamp).all()

        # Hole alle anderen Spieler und deren Matches
        other_players = session.query(Player).filter(Player.id != player_id).all()

        # Für jeden anderen Spieler deren Matches
        for other_player in other_players:
            other_player.matches = session.query(Match).filter_by(player_id=other_player.id).order_by(Match.timestamp).all()

        return render_template('player_history.html', player=player, matches=matches, other_players=other_players)
    else:
        return redirect(url_for('index'))  # Spieler nicht gefunden, zurück zur Rangliste
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
