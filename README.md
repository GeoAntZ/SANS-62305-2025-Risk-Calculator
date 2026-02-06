# SANS-62305-2025-Risk-Calculator
Doing a lightning risk assessment according to SANS 62305-2025
lightning-risk-assessment/ 
├── main.py # Application entry point and orchestrator
├── config.yaml # Global settings (RT thresholds, file paths) 
├── requirements.txt # Project dependencies (NumPy, ReportLab, etc.) 
│ ├── data/ # Static knowledge base and lookup tables 
│ ├── standards/ 
│ │ └── iec_62305_2024.yaml # Discretized tables (A.1, B.3, C.2)  
│ ├── geo/ 
│ │ └── strike_point_density.json # Geographic NSG data  
│ └── equipment/ 
│ └── withstand_voltages.csv # UW values for various port types  
│ ├── src/ 
│ ├── core/ # Core mathematical and domain logic 
│ │ ├── models/ # Physical and abstract entity classes 
│ │ │ ├── structure.py # Geometry, base footprint, and protrusions 
│ │ │ ├── zone.py # Risk zone characteristics (floor, fire, people) 
│ │ │ ├── line.py # Incoming service sections (Source S3, S4) 
│ │ │ └── protection.py# LPS, SPD, and TWS deployment models 
│ │ │ │ │ ├── algorithms/ # Annex-specific mathematical logic 
│ │ │ ├── annex_a_dangerous_events.py # Nx calculation logic  
│ │ │ ├── annex_b_probability.py # Px logic (13 factors)  
│ │ │ ├── annex_c_loss_logic.py # Lx evaluation (L1, L2, L3)  
│ │ │ └── annex_d_spd_evaluation.py # Advanced SPD modeling  
│ │ │ │ │ └── engines/ # Synthesis and comparison modules 
│ │ ├── risk_aggregator.py # Unified Risk (R) calculation  
│ │ └── frequency_engine.py # Damage Frequency (F) calculation  
│ │ │ ├── persistence/ # Storage and project management 
│ │ ├── schema.py # Project save/load definitions (JSON/SQL) 
│ │ └── version_manager.py # Migrations between standard editions 
│ │ │ ├── ui/ # User interaction layer 
│ │ └── gui_manager.py # Input panels for Structure, Lines, and Zones 
│ │ │ └── reporting/ # Professional documentation generation 
│ ├── visualization.py # 2D/3D collection area renderings 
│ └── latex_generator.py # Automated PDF audit reports 
│ └── tests/ # Quality Assurance and Validation 
├── annex_f_benchmarks/ # Validation scripts for standard case studies  
└── unit_tests/ # Individual tests for mathematical formulas
