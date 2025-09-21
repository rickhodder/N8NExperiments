# Experiment 2: Improv Comedy Show Scheduler

## Overview
This N8N workflow creates a show schedule for improv comedy performances using:
1. A list of shortform improv comedy games (with player count requirements)
2. A list of available performers
3. Python scheduling logic to create optimized show lineups

## Features
- **Game Database**: Comprehensive list of improv games with player requirements
- **Performer Management**: Track available performers and their preferences
- **Smart Scheduling**: Python algorithm to create balanced, engaging show schedules
- **Flexible Configuration**: Adjustable show length, game variety, and performer rotation

## Setup Instructions
1. Import the `improv-scheduler-workflow.json` file into your N8N instance
2. Install required Python dependencies (see `requirements.txt`)
3. Configure the game and performer data files
4. Test the workflow to generate sample schedules

## Workflow Components
- **Data Input**: Games and performers configuration
- **Python Scheduler**: Algorithm to create optimal show schedules
- **Schedule Formatter**: Formats output for different use cases
- **Export Options**: Multiple output formats (PDF, JSON, plain text)

## Usage
Trigger the workflow to generate a new show schedule based on:
- Available performers for the show
- Desired show length and game count
- Game type preferences and variety requirements