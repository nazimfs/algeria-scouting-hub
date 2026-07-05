# Enterprise Data Dictionary

## Purpose

This document defines every business entity managed by Algeria Scouting Hub.

It serves as the single reference for:

- SQLAlchemy models
- PostgreSQL schema
- REST API
- ETL pipelines
- Data Warehouse
- Business Rules

The Data Dictionary is considered the official specification of the data model.

---

# Classification

Each entity belongs to one category.

| Category | Description |
|----------|-------------|
| Master Data | Stable business entities |
| Relationship | Links between Master Data |
| Transaction | Business events |
| Fact | Quantitative measurements |
| Intelligence | AI & Scouting |
| Integration | External systems |

---

# Entity : Player

## Classification

Master Data

## Description

Represents the unique identity of a football player.

One real player must exist only once inside the platform.

Player does not contain volatile information.

## Primary Key

player_id (UUID)

## Attributes

| Name | Type | Nullable | Description |
|------|------|----------|-------------|
| player_id | UUID | No | Internal identifier |
| first_name | String | No | First name |
| last_name | String | No | Last name |
| display_name | String | No | Display name |
| birth_date | Date | No | Date of birth |
| birth_city | FK | Yes | Birth city |
| birth_country_id | FK | No | Birth country |
| height_cm | Integer | Yes | Height |
| weight_kg | Integer | Yes | Weight |
| preferred_foot | FK | Yes | Preferred foot |
| photo_url | String | Yes | Official picture |
| created_at | Timestamp | No | Creation date |
| updated_at | Timestamp | No | Last update |

## Relationships

Player

↓

PlayerNationality

↓

PlayerClub

↓

PlayerStats

↓

Transfer

↓

Injury

↓

EligibilityAssessment

↓

ScoutingReport

## Business Rules

- Never duplicated
- Never deleted
- Never linked to only one source
- Club history stored elsewhere
- Statistics stored elsewhere

---

# Entity : Club

## Classification

Master Data

## Description

Represents a football club.

## Primary Key

club_id (UUID)

## Attributes

- official_name
- short_name
- country
- stadium
- foundation_year
- website
- logo_url

## Relationships

ClubCompetition

PlayerClub

CoachClub

---

# Entity : Competition

## Classification

Master Data

Examples

Premier League

Ligue 1

CAF Champions League

UEFA Champions League

---

# Entity : Country

Represents sovereign countries.

ISO-3166 standard.

---

# Entity : Nationality

Represents citizenship.

One player

↓

Many nationalities

---

# Entity : Position

Represents football positions.

Examples

Goalkeeper

Centre Back

Left Back

Defensive Midfielder

Attacking Midfielder

Right Winger

Striker

---

# Entity : Season

Football season.

Example

2025/2026

---

# Entity : Coach

Football coach.

---

# Entity : Agent

FIFA licensed football agent.

---

# Entity : Stadium

Football stadium.

---

# Entity : DataSource

Represents external providers.

Examples

FBref

Transfermarkt

Wikipedia

Sofascore

Fotmob

FIFA

CAF

FAF

---

# Relationship Entities

PlayerClub

PlayerNationality

PlayerPosition

PlayerAgent

CompetitionSeason

ClubCompetition

---

# Transaction Entities

Transfer

Contract

MarketValue

Match

InternationalAppearance

CallUp

Injury

---

# Fact Entities

PlayerStats

GoalkeepingStats

PassingStats

DefensiveStats

PhysicalStats

ShootingStats

TeamStats

---

# Intelligence Entities

EligibilityAssessment

EligibilityEvidence

ScoutingReport

Watchlist

Recommendation

Alert

PlayerRating

AIAnalysis

---

# Integration Entities

PlayerSource

ClubSource

CompetitionSource

ImportLog

ScrapingJob

MatchingEngine

SourceFile
