# 🏆 Sports Tournament Scheduler

A sports tournament scheduling and optimization system that generates match schedules and improves them using **Genetic Algorithms** and **Memetic Algorithms**.

The system allows users to configure teams, venues, available dates, time slots, and scheduling constraints, then compare different optimization approaches through an interactive dashboard.

## ✨ Features

- **Automated Match Scheduling** — Generate tournament fixtures and assign matches to available venues, dates, and time slots.
- **Baseline Scheduling** — Generate an initial schedule to use as a reference for optimization.
- **Genetic Algorithm (GA)** — Improve schedules through selection, crossover, mutation, and elitism.
- **Memetic Algorithm (MA)** — Enhance evolutionary optimization by incorporating local search.
- **Algorithm Comparison** — Compare Baseline, Genetic Algorithm, and Memetic Algorithm results.
- **Custom Scheduling Constraints** — Configure constraints related to:
  - Team conflicts
  - Venue conflicts
  - Minimum rest periods between matches
  - Game balance between teams
- **Configurable Parameters** — Adjust population size, generations, mutation rate, and minimum rest hours.
- **Interactive Dashboard** — Visualize schedule results, fitness scores, optimization performance, and scheduling metrics.
- **Schedule Analytics** — Analyze conflicts, unscheduled matches, rest violations, and game balance.
- **Schedule Export** — Export generated schedules for further use.

## 🧠 Optimization Algorithms

### 1. Baseline Scheduler

Generates an initial feasible schedule using the scheduling logic without evolutionary optimization. It serves as the reference for evaluating the optimization algorithms.

### 2. Genetic Algorithm (GA)

Uses evolutionary computation to improve tournament schedules through:

- Population initialization
- Fitness evaluation
- Tournament selection
- Crossover
- Mutation
- Elitism

### 3. Memetic Algorithm (MA)

Combines the Genetic Algorithm's evolutionary process with local search to further improve candidate schedules.

The application allows users to run either algorithm individually or compare both approaches.

## 📊 Evaluation Metrics

Schedules are evaluated using:

| Metric | Description |
|---|---|
| Fitness Score | Overall schedule quality according to the configured fitness function |
| Team Conflicts | Matches assigned to overlapping times for the same team |
| Venue Conflicts | Multiple matches assigned to the same venue and time |
| Unscheduled Matches | Matches that could not be assigned |
| Rest Violations | Violations of the minimum rest period between matches |
| Game Balance | Measures the distribution of matches played among teams |
| Execution Time | Time required by each scheduling approach |

## 🖥️ Dashboard

The application provides an interactive dashboard for:

- Configuring tournament data
- Setting optimization parameters
- Enabling or disabling scheduling constraints
- Running scheduling algorithms
- Comparing algorithm performance
- Viewing fitness scores and analytics
- Exploring the generated schedule

## 🛠️ Tech Stack

- **Python** — Core programming language
- **Streamlit** — Interactive web application
- **Pandas** — Data manipulation and schedule analysis
- **Plotly** — Interactive data visualizations
- **Genetic Algorithms** — Evolutionary schedule optimization
- **Memetic Algorithms** — Evolution combined with local search

## 📁 Project Structure

```text
sports-tournament-scheduler/
│
├── app.py
├── integration.py
├── sports_tournament_scheduler/
│   ├── constraints.py
│   ├── fitness.py
│   ├── genetic_algorithm.py
│   ├── memetic_algorithm.py
│   ├── genetic_operators.py
│   ├── match_generator.py
│   ├── scheduler.py
│   └── ...
│
├── README.md
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/janaadarwish/sports-tournament-scheduler.git
```

### 2. Navigate to the Project Directory

```bash
cd sports-tournament-scheduler
```

### 3. Install Dependencies

```bash
pip install streamlit pandas plotly
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser. If it doesn't, Streamlit will provide a local URL in your terminal.

## ⚙️ Configuration

The scheduler supports configurable optimization settings, including:

| Parameter | Description |
|---|---|
| Teams | Participating teams |
| Venues | Available tournament venues |
| Tournament Dates | Available tournament days |
| Time Slots | Match times available on each day |
| Population Size | Number of candidate schedules in the population |
| Generations | Number of evolutionary iterations |
| Mutation Rate | Probability of mutation |
| Minimum Rest Hours | Minimum rest period between matches |
| Optimization Method | Genetic Algorithm, Memetic Algorithm, or Both |
| Constraints | Enable or disable scheduling constraints |

## 🎯 Project Goal

The goal of this project is to explore how evolutionary optimization techniques can be applied to real-world scheduling problems, producing better tournament schedules while considering multiple constraints and comparing the effectiveness of different optimization strategies.

---

**Developed as a Python optimization project focused on evolutionary algorithms, scheduling, and interactive data visualization.**
