# Task Management Rules

## Task Status Tracking

### Status Indicators
- `[ ]` - Not started
- `[🔄]` - In progress  
- `[✅]` - Completed
- `[❌]` - Blocked/Failed
- `[⏸️]` - Paused
- `[🔍]` - Under review

### Task Update Process

1. **Before Starting Work**
   - Update task status to `[🔄]` in development-tasks.md
   - Add start date and assignee if applicable

2. **During Development**
   - Keep status as `[🔄]` 
   - Add progress notes if needed

3. **After Completion**
   - Update status to `[✅]` in development-tasks.md
   - Move completed task to completed-tasks.md with details
   - Update any dependent tasks

4. **If Blocked**
   - Update status to `[❌]` 
   - Add reason for blocking
   - Identify resolution steps

### Task Priority Levels
- `🔥` - Critical/Urgent
- `⭐` - High Priority
- `📋` - Normal Priority
- `💡` - Nice to Have

### Task Dependencies
- Use `→` to show dependencies: `Task A → Task B`
- Block dependent tasks until prerequisites complete
- Update dependency chain when tasks complete

### Progress Reporting
- Weekly progress updates in completed-tasks.md
- Phase completion percentage tracking
- Milestone achievement documentation

### Task Assignment Format
```markdown
- [🔄] Task Name (Priority: ⭐, Assignee: @username, Started: 2024-01-15)
  - Dependencies: Task X → This Task
  - Notes: Implementation details
  - Blockers: None
```

## Current Task Management Commands

### Check Next Tasks
Review development-tasks.md for `[ ]` status items in current phase

### Update Task Status  
Modify status indicator and add progress notes

### Complete Task
1. Change status to `[✅]` in development-tasks.md
2. Add detailed completion info to completed-tasks.md
3. Update progress metrics

### Review Progress
Compare completed vs remaining tasks for phase completion percentage

## Automation Rules

- Always update task status when starting/completing work
- Maintain both development-tasks.md and completed-tasks.md
- Track dependencies and update dependent tasks
- Document blockers and resolution steps
- Keep progress metrics current