# ParcelPilot Ops Copilot

ParcelPilot Ops Copilot is an AI-powered operations assistant designed to help logistics teams investigate shipment issues, retrieve relevant operational information, and take informed actions through a conversational interface.

## Hosted Application

https://parcelpilot-ops-copilot-1.onrender.com

## Repository

https://github.com/AdakMahato/parcelpilot-ops-copilot

## Overview

The application provides a conversational interface for logistics operations. Users can ask questions about shipment and operational data, retrieve supporting information from available documents and structured data, and perform supported operational actions through the application.

The system is designed around three principles:

- Ground responses in available operational data
- Provide relevant supporting information before taking actions
- Keep operational actions explicit and user-confirmed

## Key Features

### Operations Assistant

Users can interact with the system using natural language to investigate operational questions and retrieve relevant information.

### Structured Data Access

The application can work with structured operational data to answer questions involving shipments, parcels, customers, and related operational information.

### Document Retrieval

Relevant documents can be retrieved and used as supporting context when answering operational questions.

### Action Confirmation

Actions are separated from information retrieval. Before a supported action is executed, the user is given an opportunity to confirm it.

### Operations Dashboard

The application provides a dashboard-oriented interface for viewing operational information and interacting with the assistant.

## Architecture

The application consists of a Next.js frontend and an API-driven application layer.

### Agent Design

The agent follows a tool-oriented workflow:

1. Receive the user's operational request
2. Determine what information is required
3. Retrieve relevant structured or document-based information
4. Combine the retrieved context
5. Generate a grounded response
6. Request confirmation before executing supported actions

The design intentionally separates information retrieval from operational actions so that actions are not performed implicitly from a conversational request.

### Tool Design

Tools are organized around specific operational capabilities rather than exposing unrestricted system access.

Typical tool categories include:

- Structured data lookup
- Document retrieval
- Dashboard information retrieval
- Operational action execution
- Action confirmation

This makes the system easier to reason about and reduces the risk of unintended operations.

### Document and Structured Data Handling

Structured operational data is handled separately from document-based information.

Structured data is used for deterministic queries such as shipment, parcel, and operational records.

Documents are retrieved when additional contextual information is required. Retrieved information is then provided to the assistant as context for generating the response.

### Source Reliability and Conflict Handling

Structured operational data is treated as the preferred source for deterministic operational facts.

When multiple sources provide information, the system prioritizes the source that is most directly relevant to the requested fact. Document information is used as supporting context rather than silently overriding structured operational records.

When information cannot be reliably established, the assistant should communicate the limitation instead of presenting an unsupported answer as fact.

## Product Note

### Additional Client Problem

In addition to answering operational questions, the solution focuses on reducing the friction involved in investigating shipment issues.

Operations teams often need to move between structured shipment information, operational documentation, and actions. The assistant brings these workflows together into a single conversational interface.

### What I Would Build Next

For a production version of ParcelPilot, I would consider adding:

- Shipment exception detection
- Proactive alerts for delayed or high-risk shipments
- Customer communication workflows
- Role-based access control
- Audit logs for operational actions
- More granular shipment analytics
- Integration with additional logistics systems

### Intentionally Left Out

To keep the submission focused, I intentionally left out:

- Large-scale production infrastructure
- Complex authentication and authorization systems
- Extensive third-party logistics integrations
- Fully automated operational actions without confirmation
- Advanced real-time event streaming

These features would be appropriate for a production deployment but were outside the scope of this assessment.

### Success Metric

The primary product metric I would use is:

**Average time required for an operations user to resolve a shipment issue.**

A successful product should reduce the time required to find the relevant information, understand the situation, and complete the appropriate operational action.

## Technical Trade-offs

The solution prioritizes clarity, reliability, and explainability over maximum system complexity.

A tool-based architecture provides clearer boundaries between retrieval and actions, while explicit confirmation reduces the risk of unintended operational changes.

The current implementation is intentionally lightweight so that the core workflow can be demonstrated without introducing unnecessary infrastructure.

## Running Locally

### Frontend

```bash
cd frontend
npm install
npm run dev
ls
