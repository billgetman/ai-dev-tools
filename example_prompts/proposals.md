---
name: Generate Plan Proposals
allowed-tools: Read, Write, Bash
description: generate implementation proposal(s)
argument-hint:[prd specification] [number of proposals]
---

# Generate Plan Proposals

Generates proposal(s) to implement the provided product spec (prd).

## Variables

PRD: $1
NUMBER_OF_PROPOSALS: $2 or 3 if not provided
PROPOSAL_OUTPUT_DIR: /ai-spec/proposals/$1/
    - This is the directory where all the proposals will be saved
    - If the $1 directory does not yet exist, create one

## Workflow
- First, check to ensure 'PRD' is provided. If not, STOP immediately and ask the user to provide it
- take note of the 'PRD' and 'NUMBER_OF_PROPOSALS'
- Create the output directory: 'PROPOSAL_OUTPUT_DIR'
- Brainstorm 'NUMBER_OF_PROPOSALS' approaches to implementing 'PRD', utilizing well known constructs and best practices.
- IMPORTANT: Then generate the 'NUMBER_OF_PROPOSALS' proposals using the 'PRD' following the 'PRD_LOOP' below, looping through each branstormed approach.

<prd-loop>
- Based on the brainstormed approach, generate an implementation plan for 'PRD' with the following sections:
  - Overview: Objectives & success metrics, Scope (in/out)
  - Timeline: Key milestones & deadlines, Project phases
  - Resources: Team & roles, Budget & tools
  - Technical Approach: Architecture overview, Integration points
  - Development: Methodology (Agile/Scrum), Quality standards
- Review the plan against 'PRD' for completedness
- Save the plan to 'PROPOSAL_OUTPUT_DIR/' as a .md file
</prd-loop>

- After all images are generated, open the output directory: 'open PROPOSAL_OUTPUT_DIR/'

## Report

- Report the total number of proposals generated
- Report the full path to the output directory