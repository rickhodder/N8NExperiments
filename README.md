# N8N Experiments

Experiments with AI-powered N8N Workflows for creative automation and productivity.

## Overview

This repository contains two experimental N8N workflows that demonstrate the integration of AI, automation, and creative processes:

1. **Telegram to Blog Entry Workflow** - Converts Telegram messages into structured blog post beginnings
2. **Improv Comedy Show Scheduler** - Creates optimized performance schedules using Python algorithms

## Experiments

### Experiment 1: Telegram to Blog Entry Workflow

**Location:** `workflows/experiment-1-telegram-blog/`

**Description:** This workflow automatically processes ideas sent via Telegram and transforms them into structured blog entry beginnings with proper formatting, titles, and outlines.

**Features:**
- Text cleaning and validation
- Automatic title generation
- Blog structure creation
- Formatted output (Markdown)
- Telegram confirmation responses

**Setup:**
1. Import `telegram-blog-workflow.json` into your N8N instance
2. Configure Telegram Bot credentials
3. Send messages to your bot to generate blog entries

### Experiment 2: Improv Comedy Show Scheduler

**Location:** `workflows/experiment-2-improv-scheduler/`

**Description:** An intelligent scheduling system for improv comedy shows that matches games with performers based on experience levels, preferences, and show requirements.

**Features:**
- Comprehensive game database (12 different improv games)
- Performer profiles with skills and preferences
- Smart scheduling algorithm
- Multiple output formats (Text, JSON, Markdown)
- Configurable show parameters

**Setup:**
1. Import `improv-scheduler-workflow.json` into your N8N instance
2. Install Python dependencies: `pip install -r requirements.txt`
3. Trigger via webhook with show parameters

## Project Structure

```
workflows/
├── experiment-1-telegram-blog/
│   ├── README.md
│   └── telegram-blog-workflow.json
└── experiment-2-improv-scheduler/
    ├── README.md
    ├── improv-scheduler-workflow.json
    ├── requirements.txt
    ├── data/
    │   ├── games.json
    │   └── performers.json
    └── scripts/
        └── scheduler.py
```

## Quick Start

### Running the Improv Scheduler Locally

```bash
cd workflows/experiment-2-improv-scheduler
python3 scripts/scheduler.py --duration 60 --format markdown --output schedule.md
```

### Testing the Telegram Workflow

1. Set up a Telegram bot using @BotFather
2. Import the workflow JSON into N8N
3. Configure your bot credentials
4. Send a message like: "AI is revolutionizing healthcare through predictive analytics"

## Dependencies

- **N8N**: Version 1.0+ (for workflow execution)
- **Python**: 3.7+ (for the scheduling algorithm)
- **Telegram Bot**: For message processing workflow

## Contributing

Feel free to extend these experiments with:
- Additional improv games and performers
- Enhanced text processing algorithms
- New output formats
- Integration with other platforms

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
