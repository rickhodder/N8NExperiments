# Example Usage for N8N Experiments

## Experiment 1: Telegram to Blog Entry

### Example Input (Telegram Message)
```
"Artificial Intelligence is transforming the way we approach software development through automated code generation and intelligent debugging tools."
```

### Expected Output
```markdown
# Exploring Artificial Intelligence Software Development: A Deep Dive into Modern Innovation

# Introduction

In today's rapidly evolving technological landscape, new ideas and concepts emerge daily that have the potential to reshape our understanding and approach to complex challenges. Artificial Intelligence is transforming the way we approach software development through automated code generation and intelligent debugging tools.

This blog post will explore this fascinating topic in detail, examining its implications, potential applications, and the broader context within which it operates.

## Article Outline

1. **Background and Context**
   - Current state of the field
   - Key challenges and opportunities

2. **Core Concepts**
   - Detailed exploration of the main idea
   - Technical considerations

3. **Real-World Applications**
   - Practical implementations
   - Case studies and examples

4. **Future Implications**
   - Potential developments
   - Long-term impact

5. **Conclusion**
   - Key takeaways
   - Next steps for exploration

---

*This blog entry was generated from a Telegram message on 12/21/2024*
```

## Experiment 2: Improv Comedy Show Scheduler

### Example API Request
```bash
curl -X POST http://your-n8n-instance/webhook/schedule-show \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 60,
    "availability": "high",
    "format": "json",
    "gameCount": 8
  }'
```

### Example Command Line Usage
```bash
# Generate a 45-minute show schedule
python3 scripts/scheduler.py --duration 45 --format markdown --output show-schedule.md

# Create a schedule with only high-availability performers
python3 scripts/scheduler.py --availability high --format json

# Quick 30-minute show
python3 scripts/scheduler.py --duration 30
```

### Example Output (Markdown Format)
```markdown
# Improv Comedy Show Schedule

## Game 1: Party Host
**Time:** 00:00 (4 minutes)  
**Category:** Character  
**Difficulty:** Easy  
**Performers:** Jordan Martinez, Morgan Davis, Alex Thompson, Casey Brown  

*One player hosts a party while others arrive with specific quirks or characteristics*

## Game 2: Questions Only
**Time:** 00:06 (3 minutes)  
**Category:** Verbal  
**Difficulty:** Medium  
**Performers:** Alex Thompson, Casey Brown  

*Players can only communicate through questions*
```

## Integration Examples

### Using with Other Tools

1. **Slack Integration**: Trigger the Telegram workflow from Slack messages
2. **Google Calendar**: Export improv schedules to calendar events
3. **Email Automation**: Send generated blog drafts via email
4. **Webhook Chains**: Combine both workflows for content and event management