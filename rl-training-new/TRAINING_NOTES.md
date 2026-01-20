# Training Progress Notes

## Session 1: Sparse Rewards (Failed)
- **Duration:** 410K timesteps
- **Result:** 0 wins, 100% topped out
- **Episode length:** ~1 step average
- **Problem:** No learning signal - agent never cleared viruses to get reward
- **Archived:** logs/archive_sparse_rewards/

## Session 2: Dense Color Matching Rewards (Current)
- **Started:** 2026-01-18 04:03
- **Improvements:**
  - Dense rewards for 2/3/4+ color matches
  - Virus match bonus (+3.0 if match contains virus)
  - Curriculum learning: dampens match rewards as agent improves
  - Random P1 opponent for competitive pressure

### Future Improvements (Backlog)

**Combo rewards** (suggested by user):
- Reward chain reactions (clearing triggers falling → another clear)
- Higher value than single clears
- Encourages strategic stacking
- Implementation: Track consecutive virus_count decreases within N frames
- **Priority:** Medium (wait until basic clearing works)

**Other potential improvements:**
- Survival time bonus (reward staying alive longer)
- Pill rotation penalty (discourage excessive rotation)
- Column balance reward (avoid single tall column)
- Opponent-relative rewards (distance from P1's virus count)

