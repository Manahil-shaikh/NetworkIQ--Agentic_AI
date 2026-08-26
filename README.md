# NetworkIQ--Agentic_AI
This is a small prototype for agentic AI project for learning
Agentic AI-powered Telecom Network Intelligence System

NetworkIQ is a production-oriented Agentic AI prototype for investigating telecom network performance using LangGraph, LangChain, Ollama, and Qwen 2.5 1.5B.

The system combines LLM-driven tool calling with deterministic telecom KPI analysis to retrieve network data, detect anomalies, perform root-cause analysis, and generate remediation recommendations.

Project goal: demonstrate practical Agentic AI engineering applied to a real telecom network-operations use case while remaining completely local and free to run.

Architecture
                         User Query
                             │
                             ▼
                    ┌─────────────────┐
                    │   FastAPI API   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Request Parser  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    LangGraph    │
                    │  Agent Workflow │
                    └────────┬────────┘
                             │
                             ▼
                       ┌───────────┐
                       │ Qwen 2.5  │
                       │   1.5B    │
                       └─────┬─────┘
                             │
                       Tool Calling
                             │
                             ▼
                    ┌─────────────────┐
                    │    ToolNode     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Network Data    │
                    │   Repository    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ KPI Analysis &  │
                    │ Anomaly Engine  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Root Cause      │
                    │    Analysis     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Recommendation  │
                    └────────┬────────┘
                             │
                             ▼
                       Final Response
Agentic Workflow

NetworkIQ implements an LLM-driven tool-calling loop using LangGraph:

START
  │
  ▼
Call LLM
  │
  ▼
Tool required?
 ┌┴───────────────┐
 │                │
Yes               No
 │                │
 ▼                ▼
ToolNode       Network Analysis
 │                │
 └──► LLM         ▼
             Root Cause Analysis
                    │
                    ▼
              Recommendation
                    │
                    ▼
                   END

The LLM is responsible for reasoning and tool selection, while deterministic Python components handle telecom-specific calculations.

Key Features
Agentic tool calling using LangChain
LangGraph state-based orchestration
LLM → Tool → LLM agent loop
Telecom KPI retrieval
Deterministic KPI anomaly detection
Historical incident retrieval
Root-cause analysis
Evidence-based recommendations
Natural-language request parsing
FastAPI REST API
Local inference using Ollama
Qwen 2.5 1.5B support for resource-constrained systems
Docker-ready deployment architecture
Synthetic telecom network dataset for experimentation
