# Phase 1: Basic Agentic Loop

## Overview
Build a single agent with ReAct-style reasoning loop (Think → Act → Observe → Repeat).

## Setup
- [ ] Create src/agents/__init__.py with base agent class structure
- [ ] Create tests/agents/__init__.py
- [ ] Verify pytest runs successfully with no tests

## Core Agent Loop
- [ ] Test: Agent initializes with OpenAI client
- [ ] Test: Agent receives a message and returns a response
- [ ] Test: Agent can call a tool and observe the result
- [ ] Test: Agent loops until it decides to stop (max iterations safety)
- [ ] Test: Agent maintains conversation history within a session

## Basic Tools
- [ ] Test: search_web tool interface returns expected structure
- [ ] Test: save_note tool writes content to specified path
- [ ] Test: Agent selects appropriate tool based on user query

## ReAct Implementation
- [ ] Test: Agent produces "Thought" before taking action
- [ ] Test: Agent produces "Observation" after tool execution
- [ ] Test: Agent produces final "Answer" when task complete

## Integration
- [ ] Test: End-to-end flow - user asks question, agent thinks, acts, responds
- [ ] Manual verification: Run agent interactively in terminal

## Documentation
- [ ] Update CLAUDE.md with testing patterns established
- [ ] Update phase-1-log.md with implementation summary
- [ ] Add docstrings to all public functions