from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Datenbank einrichten
Base = declarative_base()
engine = create_engine('sqlite:///doppelkopf_tournament.db')
Session = sessionmaker(bind=engine)
session = Session()

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    rating = Column(Float, default=1300)
    history = relationship("Match", back_populates="player")

    def update_rating(self, change):
        self.rating += change

class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    score_change = Column(Float)
    new_rating = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)
    
    player = relationship("Player", back_populates="history")

# Tabellen erstellen
Base.metadata.create_all(engine)

class DoppelkopfTournament:
    def __init__(self, base_k=128):
        self.base_k = base_k

    def add_player(self, name):
        if not session.query(Player).filter_by(name=name).first():
            player = Player(name=name)
            session.add(player)
            session.commit()
            print(f"Added player {name} with starting rating {player.rating}")

    def calculate_dynamic_points(self, player_rating, opponent_ratings, placement_index):
        avg_opponent_rating = sum(opponent_ratings) / len(opponent_ratings)
        rating_difference = avg_opponent_rating - player_rating
        expected_score = 1 / (1 + 10 ** (rating_difference / 400))
        placement_multipliers = [1.0, 0.66, 0.33, 0.0]
        return int(self.base_k * (placement_multipliers[placement_index] - expected_score))

    def update_scores(self, table_results):
        table_ratings = [session.query(Player).filter_by(name=name).first().rating for name in table_results]
        for i, name in enumerate(table_results):
            player = session.query(Player).filter_by(name=name).first()
            opponent_ratings = table_ratings[:i] + table_ratings[i+1:]
            point_change = self.calculate_dynamic_points(player.rating, opponent_ratings, i)
            
            player.update_rating(point_change)
            session.add(player)
            
            match = Match(
                player_id=player.id,
                score_change=point_change,
                new_rating=player.rating
            )
            session.add(match)
        session.commit()

    def get_rankings(self):
        return session.query(Player).order_by(Player.rating.desc()).all()
    
    def get_rank_image(self, rating):
        # Beispielhafte Rangstufen basierend auf Punkten
        if rating < 800:
            return "skillgroup1.png"
        elif 800 <= rating < 870:
            return "skillgroup2.png"
        elif 870 <= rating < 940:
            return "skillgroup3.png"
        elif 940 <= rating < 1010:
            return "skillgroup4.png"
        elif 1010 <= rating < 1080:
            return "skillgroup5.png"
        elif 1080 <= rating < 1150:
            return "skillgroup6.png"
        elif 1150 <= rating < 1220:
            return "skillgroup7.png"
        elif 1220 <= rating < 1290:
            return "skillgroup8.png"
        elif 1290 <= rating < 1360:
            return "skillgroup9.png"
        elif 1360 <= rating < 1430:
            return "skillgroup10.png"
        elif 1430 <= rating < 1500:
            return "skillgroup11.png"
        elif 1500 <= rating < 1570:
            return "skillgroup12.png"
        elif 1570 <= rating < 1640:
            return "skillgroup13.png"
        elif 1640 <= rating < 1710:
            return "skillgroup14.png"
        elif 1710 <= rating < 1780:
            return "skillgroup15.png"
        elif 1780 <= rating < 1850:
            return "skillgroup16.png"
        elif 1850 <= rating < 1920:
            return "skillgroup17.png"
        else:
            return "skillgroup18.png"  # Standard für hohe Punkte
    
def initialize_players():
    initial_players = [
        "Maris", "Noaaaaaahhhhhhh", "Tamino", "Anna", "Mark", "Kirill", "Sven",
        "Lukas", "Willis", "Georg Garbusow", "Claudius", "Mara", "Jakob", "Magda",
        "Clara E", "Justus", "Eka Vanderling", "Lauti", "Marina", "Jonas B", "Pola",
        "Seyed Soheil Hosseini Bidar", "Frieda", "Nora", "Pavel", "Joshua",
        "Henning Sauter", "Sir Connor von Minkowski", "Armand", "Jerome",
        "Konsti die Legende", "Philip Gilde", "Fips", "Moses", "Felix Pasche",
        "Uladzimir", "Alina", "Laura Pfeil", "Thomi", "Jule", "Cornelius Pech",
        "Vincent", "Philip Hagemeyer", "Damien", "Elena Galneder", "Tilman",
        "Hannes", "Franz", "Chef"
    ]
    for name in initial_players:
        if not session.query(Player).filter_by(name=name).first():
            player = Player(name=name)
            session.add(player)
    session.commit()
