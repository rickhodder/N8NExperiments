#!/usr/bin/env python3
"""
Improv Comedy Show Scheduler

This script creates optimized show schedules for improv comedy performances
by matching games with available performers based on various criteria.
"""

import json
import random
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import argparse
import sys


@dataclass
class Game:
    name: str
    description: str
    min_players: int
    max_players: int
    category: str
    difficulty: str
    duration_minutes: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Game':
        return cls(**data)


@dataclass
class Performer:
    name: str
    experience_level: str
    preferred_games: List[str]
    strengths: List[str]
    availability: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Performer':
        return cls(**data)


@dataclass
class ScheduledGame:
    game: Game
    performers: List[Performer]
    start_time: int  # minutes from show start
    notes: str = ""


class ImprovScheduler:
    def __init__(self, games_file: str, performers_file: str):
        self.games = self._load_games(games_file)
        self.performers = self._load_performers(performers_file)
        
    def _load_games(self, file_path: str) -> List[Game]:
        """Load games from JSON file"""
        with open(file_path, 'r') as f:
            games_data = json.load(f)
        return [Game.from_dict(game) for game in games_data]
    
    def _load_performers(self, file_path: str) -> List[Performer]:
        """Load performers from JSON file"""
        with open(file_path, 'r') as f:
            performers_data = json.load(f)
        return [Performer.from_dict(performer) for performer in performers_data]
    
    def get_available_performers(self, availability_filter: str = None) -> List[Performer]:
        """Filter performers by availability"""
        if not availability_filter:
            return self.performers
        
        availability_order = {"high": 3, "medium": 2, "low": 1}
        min_availability = availability_order.get(availability_filter, 1)
        
        return [p for p in self.performers 
                if availability_order.get(p.availability, 1) >= min_availability]
    
    def find_suitable_games(self, available_performers: List[Performer], 
                           max_duration: int = None) -> List[Game]:
        """Find games that can be played with available performers"""
        suitable_games = []
        performer_count = len(available_performers)
        
        for game in self.games:
            if game.min_players <= performer_count <= game.max_players:
                if max_duration is None or game.duration_minutes <= max_duration:
                    suitable_games.append(game)
        
        return suitable_games
    
    def score_game_performer_match(self, game: Game, performers: List[Performer]) -> float:
        """Score how well a game matches with selected performers"""
        score = 0.0
        
        # Preference scoring
        for performer in performers:
            if game.name in performer.preferred_games:
                score += 2.0
        
        # Experience level matching
        difficulty_score = {"easy": 1, "medium": 2, "hard": 3}
        experience_score = {"beginner": 1, "intermediate": 2, "advanced": 3}
        
        game_difficulty = difficulty_score.get(game.difficulty, 2)
        avg_experience = sum(experience_score.get(p.experience_level, 2) 
                           for p in performers) / len(performers)
        
        # Ideal: game difficulty matches average experience
        if abs(game_difficulty - avg_experience) <= 0.5:
            score += 1.5
        elif abs(game_difficulty - avg_experience) <= 1.0:
            score += 1.0
        
        # Category variety bonus (calculated at schedule level)
        score += random.uniform(0, 0.5)  # Small random factor for variety
        
        return score
    
    def select_performers_for_game(self, game: Game, 
                                 available_performers: List[Performer],
                                 used_performers: List[Performer] = None) -> List[Performer]:
        """Select optimal performers for a specific game"""
        if used_performers is None:
            used_performers = []
        
        # Prefer performers who haven't been used recently
        unused_performers = [p for p in available_performers if p not in used_performers[-3:]]
        if len(unused_performers) < game.min_players:
            unused_performers = available_performers
        
        # Score all possible combinations
        candidate_performers = unused_performers[:game.max_players]
        
        # For games requiring specific numbers, try to hit the sweet spot
        target_count = min(game.max_players, max(game.min_players + 1, len(candidate_performers)))
        
        # Prioritize performers who prefer this game
        preferred_performers = [p for p in candidate_performers if game.name in p.preferred_games]
        other_performers = [p for p in candidate_performers if game.name not in p.preferred_games]
        
        # Mix preferred and other performers
        selected = preferred_performers[:target_count]
        if len(selected) < target_count:
            selected.extend(other_performers[:target_count - len(selected)])
        
        # Ensure minimum requirements
        if len(selected) < game.min_players:
            selected.extend(available_performers[:game.min_players - len(selected)])
        
        return selected[:target_count]
    
    def create_schedule(self, show_duration: int = 60, 
                       available_performers: List[Performer] = None,
                       game_count: int = None) -> List[ScheduledGame]:
        """Create an optimized show schedule"""
        if available_performers is None:
            available_performers = self.get_available_performers("medium")
        
        if len(available_performers) < 2:
            raise ValueError("Need at least 2 performers to create a schedule")
        
        schedule = []
        current_time = 0
        used_performers = []
        used_categories = []
        
        # Calculate target number of games if not specified
        if game_count is None:
            avg_game_duration = sum(g.duration_minutes for g in self.games) / len(self.games)
            game_count = max(3, int(show_duration * 0.7 / avg_game_duration))  # 70% of time for games
        
        suitable_games = self.find_suitable_games(available_performers)
        
        for game_num in range(game_count):
            # Time check
            if current_time >= show_duration - 5:  # Leave 5 minutes buffer
                break
            
            # Find best game for this slot
            remaining_time = show_duration - current_time
            available_games = [g for g in suitable_games if g.duration_minutes <= remaining_time]
            
            if not available_games:
                break
            
            # Score games based on various factors
            game_scores = []
            for game in available_games:
                selected_performers = self.select_performers_for_game(
                    game, available_performers, used_performers
                )
                
                base_score = self.score_game_performer_match(game, selected_performers)
                
                # Category variety bonus
                category_bonus = 0.5 if game.category not in used_categories[-2:] else 0
                
                # Time fitting bonus
                time_bonus = 0.3 if game.duration_minutes <= remaining_time * 0.8 else 0
                
                total_score = base_score + category_bonus + time_bonus
                game_scores.append((game, selected_performers, total_score))
            
            # Select best game
            game_scores.sort(key=lambda x: x[2], reverse=True)
            best_game, best_performers, _ = game_scores[0]
            
            # Add to schedule
            scheduled_game = ScheduledGame(
                game=best_game,
                performers=best_performers,
                start_time=current_time,
                notes=f"Game {game_num + 1} of {game_count}"
            )
            schedule.append(scheduled_game)
            
            # Update tracking
            current_time += best_game.duration_minutes + 2  # 2 min buffer between games
            used_performers.extend(best_performers)
            used_categories.append(best_game.category)
        
        return schedule
    
    def format_schedule(self, schedule: List[ScheduledGame], output_format: str = "text") -> str:
        """Format schedule for output"""
        if output_format == "json":
            return self._format_json(schedule)
        elif output_format == "markdown":
            return self._format_markdown(schedule)
        else:
            return self._format_text(schedule)
    
    def _format_text(self, schedule: List[ScheduledGame]) -> str:
        """Format schedule as plain text"""
        output = ["IMPROV COMEDY SHOW SCHEDULE", "=" * 35, ""]
        
        total_time = 0
        for i, game in enumerate(schedule, 1):
            start_mins = game.start_time
            start_time = f"{start_mins // 60:02d}:{start_mins % 60:02d}"
            
            output.extend([
                f"Game {i}: {game.game.name}",
                f"Time: {start_time} ({game.game.duration_minutes} minutes)",
                f"Category: {game.game.category.title()}",
                f"Difficulty: {game.game.difficulty.title()}",
                f"Performers: {', '.join(p.name for p in game.performers)}",
                f"Description: {game.game.description}",
                ""
            ])
            total_time += game.game.duration_minutes
        
        output.extend([
            f"Total show time: {total_time} minutes",
            f"Number of games: {len(schedule)}",
            f"Performers used: {len(set(p.name for game in schedule for p in game.performers))}"
        ])
        
        return "\n".join(output)
    
    def _format_markdown(self, schedule: List[ScheduledGame]) -> str:
        """Format schedule as Markdown"""
        output = ["# Improv Comedy Show Schedule", ""]
        
        for i, game in enumerate(schedule, 1):
            start_mins = game.start_time
            start_time = f"{start_mins // 60:02d}:{start_mins % 60:02d}"
            
            output.extend([
                f"## Game {i}: {game.game.name}",
                f"**Time:** {start_time} ({game.game.duration_minutes} minutes)  ",
                f"**Category:** {game.game.category.title()}  ",
                f"**Difficulty:** {game.game.difficulty.title()}  ",
                f"**Performers:** {', '.join(p.name for p in game.performers)}  ",
                "",
                f"*{game.game.description}*",
                ""
            ])
        
        return "\n".join(output)
    
    def _format_json(self, schedule: List[ScheduledGame]) -> str:
        """Format schedule as JSON"""
        schedule_data = []
        for game in schedule:
            schedule_data.append({
                "game_name": game.game.name,
                "start_time": game.start_time,
                "duration": game.game.duration_minutes,
                "category": game.game.category,
                "difficulty": game.game.difficulty,
                "performers": [p.name for p in game.performers],
                "description": game.game.description,
                "notes": game.notes
            })
        
        return json.dumps({
            "schedule": schedule_data,
            "summary": {
                "total_games": len(schedule),
                "total_duration": sum(g.game.duration_minutes for g in schedule),
                "unique_performers": len(set(p.name for game in schedule for p in game.performers))
            }
        }, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate improv comedy show schedules")
    parser.add_argument("--games", default="data/games.json", help="Games JSON file")
    parser.add_argument("--performers", default="data/performers.json", help="Performers JSON file")
    parser.add_argument("--duration", type=int, default=60, help="Show duration in minutes")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text", help="Output format")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--availability", choices=["high", "medium", "low"], help="Minimum performer availability")
    
    args = parser.parse_args()
    
    try:
        scheduler = ImprovScheduler(args.games, args.performers)
        available_performers = scheduler.get_available_performers(args.availability)
        
        if not available_performers:
            print("No performers available with the specified criteria", file=sys.stderr)
            return 1
        
        schedule = scheduler.create_schedule(
            show_duration=args.duration,
            available_performers=available_performers
        )
        
        if not schedule:
            print("Could not create a schedule with the given constraints", file=sys.stderr)
            return 1
        
        formatted_schedule = scheduler.format_schedule(schedule, args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(formatted_schedule)
            print(f"Schedule saved to {args.output}")
        else:
            print(formatted_schedule)
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())