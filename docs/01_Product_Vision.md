# Algeria Scouting Hub

## Product Vision

### Overview

Algeria Scouting Hub is a football intelligence platform designed to centralize, consolidate, enrich and analyze player information from multiple public data sources.

The platform aims to help identify, monitor and evaluate football players who are eligible, or potentially eligible, to represent the Algerian National Team.

Rather than being a simple data scraper, Algeria Scouting Hub is designed as a complete decision-support platform for scouting and international eligibility analysis.

---

# Problem Statement

Football data is currently fragmented across multiple websites.

A scout often needs to manually consult several sources such as:

- FBref
- Transfermarkt
- Sofascore
- Wikipedia
- FIFA
- National Federations

Each website provides only a partial view of a player.

There is no unified platform capable of:

- consolidating all available information
- detecting duplicated players across sources
- tracking historical changes
- explaining international eligibility
- providing scouting insights

---

# Vision

Create the reference platform for international football scouting.

The platform should provide a single source of truth for every player by combining information from multiple trusted sources into one consolidated player profile.

---

# Objectives

The platform aims to:

- Centralize football data
- Eliminate duplicated information
- Track player careers
- Monitor player performance
- Explain FIFA eligibility rules
- Support national team scouting
- Provide advanced analytics
- Offer AI-assisted recommendations

---

# Target Users

- National Football Federations
- Professional Scouts
- Recruitment Analysts
- Football Clubs
- Sports Data Analysts
- Journalists
- Researchers

---

# Core Principles

## Data First

Data is the core asset of the platform.

Applications, APIs and dashboards are only consumers of the data.

---

## Single Source of Truth

Each real-world entity must exist only once inside the platform.

Example:

One player

↓

Many external sources

↓

One Golden Record

---

## Explainability

Every important decision should be explainable.

Example:

Why is this player eligible for Algeria?

↓

Nationality

↓

Parents

↓

Birthplace

↓

FIFA regulations

↓

Evidence

---

## Scalability

The platform must support:

- millions of players
- dozens of competitions
- multiple countries
- multiple national teams
- multiple data providers

---

# Long-Term Vision

The first version targets the Algerian National Team.

The architecture should later support any football federation simply by configuring eligibility rules.

Future examples:

- Morocco Scouting Hub
- Tunisia Scouting Hub
- Senegal Scouting Hub
- France Scouting Hub

The core platform remains identical.

Only business rules change.