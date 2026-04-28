# Product Overview
Smart Marketing Agent that clusters customers without prior bias using the DBSCAN algorithm to discover natural groupings. Once these segments are identified, the system uses a language model (via OpenRouter) to draft personalized marketing copies in Chilean Spanish (Next Best Offer) for each group. The entire system is orchestrated using the Google Agent Development Kit (ADK).

# Assumptions
- Customer data is available, clean, and numerically encoded (or ready to be preprocessed) so that DBSCAN can operate on it effectively.
- The OpenRouter API is accessible and valid keys are available.
- Google ADK will be used as the framework for orchestrating the multi-agent architecture.
- The generated copies require a Chilean Spanish format appropriate for a business context (approachable, commercial tone).

# Personas
1. **Marketing Analyst / Growth Hacker (End User):** Seeks to automate the creation of personalized campaigns without having to manually segment or write hundreds of emails.
2. **Data Engineer / ML Engineer:** Responsible for maintaining the clustering logic and providing the data pipeline for the system.

# Epics

## Epic 1: Customer Segmentation with DBSCAN
### US-001: Automatic Customer Clustering
- **As a** Marketing Analyst
- **I want** the system to automatically group my customers using DBSCAN without defining the number of clusters upfront
- **So that** I can discover natural behavior segments based on real data
- **Priority:** P0
- **Dependencies:** Customer data availability
- **Acceptance Criteria (Gherkin):**
  1. Given a scaled and valid customer dataset When the system executes the clustering agent Then the DBSCAN algorithm is applied and a cluster identifier is returned for each customer.
  2. Given a dataset with outliers When DBSCAN processes the data Then it identifies anomalous or isolated customers as "noise" (cluster -1) so as not to bias the offers.

## Epic 2: Marketing Copy Generation (Next Best Offer)
### US-002: Offer Drafting in Chilean Spanish
- **As a** Marketing Analyst
- **I want** the agent to generate a persuasive "Next Best Offer" text for each cluster using Chilean Spanish slang and tone
- **So that** the campaign connects better with the local audience and increases conversion
- **Priority:** P0
- **Dependencies:** US-001, OpenRouter Integration
- **Acceptance Criteria (Gherkin):**
  1. Given a profile or centroid of a specific cluster When the agent requests a copy Then the LLM returns a marketing text offering the ideal product/service in Chilean Spanish.
  2. Given that the OpenRouter API fails or times out When attempting to generate the copy Then the system logs the error, performs exponential retries, and raises an alert if it ultimately fails.
  3. Given a cluster classified as "noise" (-1) When the agent evaluates this group Then it generates a generalized win-back copy.

## Epic 3: Architecture and Orchestration with Google ADK & OpenRouter
### US-003: Agent Orchestration with Google ADK
- **As a** ML Engineer
- **I want** the segmentation and drafting flow to be orchestrated as a multi-agent system using Google ADK
- **So that** the design is modular, scalable, and maintainable
- **Priority:** P1
- **Dependencies:** None
- **Acceptance Criteria (Gherkin):**
  1. Given the invocation of the process When the ADK coordinator is activated Then it sequentially delegates the clustering task to the Analytical Agent and then the drafting to the Generative Agent.

### US-004: LLM Integration via OpenRouter API
- **As a** ML Engineer
- **I want** the drafting agent to use the OpenRouter API
- **So that** we can dynamically route requests to different foundational models in an agnostic manner
- **Priority:** P0
- **Dependencies:** OpenRouter Account and Key
- **Acceptance Criteria (Gherkin):**
  1. Given the credentials configured securely (not in the code) When the agent requests a copy Then the HTTP request is correctly routed through OpenRouter, returning the structured copy.

# Traceability Matrix
| Feature / Step | Covered by Story IDs |
|---|---|
| cluster all customers (dbscan, optimal number) | US-001 |
| create text for each cluster as marketing copy (NBO) | US-002 |
| use chilean spanish | US-002 |
| use google adk to design the agentic system | US-003 |
| use openrouter api to llm use | US-004 |

# Open Questions
1. What specific variables will be used to calculate distances in DBSCAN (e.g., RFM: recency, frequency, monetary value)?
2. How will the DBSCAN hyperparameters (`eps` and `min_samples`) be auto-configured or defined to ensure business-sensible clusters?
3. Which foundational model (e.g., claude-3.5-sonnet, gpt-4o) will be the default in OpenRouter to ensure the best understanding of Chilean Spanish?
4. What length (characters or words) is required for the copy? (Depends on the channel: SMS, Email, Push).

# Reflective Audit
1. **Failure Point:** Static DBSCAN hyperparameter tuning fails as data varies over time, resulting in 1 macro-cluster or pure noise.
   - **Mitigation:** Include a k-NN distance calculation task prior to clustering to automatically find the elbow point that recommends the `eps` value.
2. **Failure Point:** Chilean Spanish may be exaggerated or caricatured by the LLM, losing professionalism.
   - **Mitigation:** Define a comprehensive System Prompt in the ADK agent that specifies "commercial tone, subtly local, and avoiding excessive slang".
3. **Failure Point:** Repetitive or unstable LLM generation for very similar clusters.
   - **Mitigation:** Configure a moderate `temperature` (e.g., 0.7) in OpenRouter and inject explicit, differentiating attributes for each cluster into the prompt.

# Clear answer | Confidence level | Key caveats
**Clear Answer:** The consolidated Agile backlog for the required multi-agent system has been generated, mapping the iterative clustering and NBO generation needs through Google ADK and OpenRouter.
**Confidence level:** High.
**Key caveats:** DBSCAN is highly sensitive to variable scale, therefore a `StandardScaler` or `MinMaxScaler` step will be mandatory. Additionally, the success of the Next Best Offer requires extracting the mean characteristics of each group (profiling) after clustering to provide good context to the LLM.
