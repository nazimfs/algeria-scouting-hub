# Domain Model

## Purpose

This document defines the business domain of Algeria Scouting Hub.

The objective is to describe the real-world concepts handled by the platform independently from any technical implementation.

This document serves as the foundation for:

- Database Design
- SQLAlchemy Models
- REST API
- ETL Pipelines
- Data Warehouse
- Business Rules

---

# Core Business Domains

The platform is divided into seven business domains.

---

## 1. Master Data

Master Data represents stable business entities.

These entities are considered the official reference of the platform.

Entities:

- Player
- Club
- Competition
- Season
- Country
- Nationality
- Position
- Coach
- Agent
- Stadium
- DataSource

---

## 2. Relationships

Relationship entities connect Master Data together.

Examples:

- PlayerClub
- PlayerNationality
- PlayerPosition
- PlayerAgent
- CompetitionSeason
- ClubCompetition

---

## 3. Football Events

Events describe something that happened during a player's career.

Examples:

- Transfer
- Injury
- Match
- Contract
- International Call-up
- Market Value Update

---

## 4. Performance

Performance entities describe measurable football statistics.

Examples:

- PlayerStats
- GoalkeepingStats
- PassingStats
- ShootingStats
- DefensiveStats
- PhysicalStats

---

## 5. International Football

This domain manages international eligibility.

Examples:

- NationalTeam
- EligibilityRule
- EligibilityAssessment
- InternationalAppearance
- EligibilityEvidence

---

## 6. Scouting

This domain contains business intelligence produced by the platform.

Examples:

- ScoutingReport
- PlayerRating
- Watchlist
- Recommendation
- Alert

---

## 7. Data Ingestion

This domain manages external data providers.

Examples:

- DataSource
- SourcePlayer
- SourceClub
- SourceCompetition
- ScrapingJob
- ImportLog
- MatchingEngine

---

# Aggregate Root

The primary Aggregate Root of the platform is:

Player

Every important business process revolves around a player.

The player itself remains stable while relationships, events and statistics evolve over time.

---

# Business Philosophy

The platform follows Domain Driven Design principles.

Business concepts always come before technical implementation.

The database is only one possible implementation of the domain model.

The domain model is the true source of business knowledge.

---

# Guiding Principles

- Business before Technology
- Single Source of Truth
- Explicit Relationships
- Historical Tracking
- Explainable Decisions
- Scalability by Design
- Source Independence
