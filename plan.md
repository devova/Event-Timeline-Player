# Timeline Player Implementation Plan

## Phase 1: Timeline UI Components and Layout ✅
- [x] Set up Material Design 3 theme with Montserrat font and purple/gray color scheme
- [x] Create timeline visualization component with event dots
- [x] Implement horizontal timeline bar with time markers
- [x] Add timeline controls (play, pause, stop, seek slider)
- [x] Design timeline card container with proper Material elevation (1dp at rest, 8dp on hover)

## Phase 2: Multi-Timeline State Management and Playback ✅
- [x] Create state management for multiple parallel timelines
- [x] Implement timeline data structure (id, type, events with timestamps, current position)
- [x] Add playback engine that tracks current time and triggers events
- [x] Build UI for displaying multiple timelines vertically stacked
- [x] Add timeline creation form with timeline type selection (conflict_id or proposal_fkey)

## Phase 3: Event Triggering and Backend Actions ✅
- [x] Implement event triggering system when playback reaches event timestamp
- [x] Create backend event handlers for different event types
- [x] Add event visualization with different states (pending, triggered, completed)
- [x] Implement event details panel showing triggered events and their actions
- [x] Add timeline controls for each individual timeline (independent play/pause)

## Phase 4: UI Verification ✅
- [x] Test timeline creation and deletion functionality
- [x] Verify playback controls work correctly (play, pause, stop, seek)
- [x] Validate event triggering and visualization during playback
- [x] Check event details panel displays triggered events correctly

## Phase 5: Common Player Controls ✅
- [x] Remove individual timeline controls from each timeline card
- [x] Create global player controls component that affects all timelines simultaneously
- [x] Update state management to handle global play/pause/stop/seek operations
- [x] Synchronize all timelines to the same playback position
- [x] Add global time display showing current position across all timelines
- [x] Ensure all events trigger correctly across all timelines during global playback

## Phase 6: Final UI Verification ✅
- [x] Verify global controls appear at the top with proper styling
- [x] Test that all timelines stack vertically and sync during playback
- [x] Validate global seek slider affects all timelines
- [x] Check that creating new timelines works with global controls
