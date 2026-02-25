# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **cross-border e-commerce product selection intelligent agent skills** development project. The goal is to build Claude Code skills that help identify profitable products from Amazon to sell on Temu and 4supply.com (Loktek's B2B platform).

### Business Logic

The skills need to implement a 3-step product selection process:

1. **Amazon Analysis**: Identify trending products from Amazon Movers & Shakers
2. **Market Gap Analysis**: Check if products have potential on Temu/4supply.com with low competition
3. **Sourcing Analysis**: Find suppliers on 1688.com at competitive prices

### Profit Calculation Formula (V4.1 Model)

```
Net Profit = (Temu Lowest Price * 0.45 * 7.2) - (1688 Cost + ¥3.50)
```

**Hard Rule**: Net profit must exceed ¥5.00, or the product is rejected.

## Skill Architecture

The requirements should be broken down into **independent, single-responsibility skills**:

### Core Skills to Develop

1. **amazon-trending-products**: Fetch and analyze Amazon Movers & Shakers data
2. **temu-market-research**: Analyze Temu market competition and pricing
3. **supply-market-research**: Analyze 4supply.com market data
4. **sourcing-1688**: Search and price products on 1688.com
5. **profit-calculator**: Calculate profit margins using V4.1 model
6. **product-selection-agent**: Orchestrate the full workflow and generate reports

## Development Workflow

### Research Existing Skills First

Before implementing new skills, check these skill repositories:

```bash
# Official Claude Code skills
open https://github.com/anthropics/skills

# Third-party skill marketplaces
open https://skillsmp.com/
open https://skills.sh/
open https://skills.302.ai/zh
open https://github.com/iOfficeAI/AionUi/tree/main
```

### Skill Development Standards

Skills must follow Claude Code's official skill development protocol:

1. Use the Skill tool to create new skills
2. Follow the `skill-creator` skill guidelines
3. Ensure skills can be automatically invoked by Claude Code
4. Include proper documentation and examples in each skill

### Local Development Commands

```bash
# Install Claude Code (if not already installed)
npm install -g @anthropic-ai/claude-code

# Launch Claude Code in this directory
claude

# Use the skill-creator skill for guidance on creating skills
/skill-creator

# Find existing skills that might match your needs
/skill find-skills
```

## Delivery Requirements

### GitHub Repository

- **Repo URL**: `https://github.com/global-ecom-skills/global-ecom-skills`
- **Branch naming convention**: `{skill-name}-{candidate-full-name-pinyin}`
- Do NOT push to `main` branch until skill is enterprise-ready
- Create your own branch following the naming convention

### Command-Line Installation

Skills must be installable via command line (similar to `npx skills add`):

```bash
# Example installation format (reference: skills.sh)
npx skills add <skill-name>
```

### Video Demonstration

Required deliverables include:
1. Skills testing demonstration
2. Complete product frontend/backend testing demonstration
3. Recorded video of skills in action

## Key Constraints

1. **No High-Certification Products**: Avoid products requiring extensive certifications
2. **Minimum Profit Margin**: Net profit must exceed ¥5.00 per unit
3. **Bundle/Premium/Lightweight Strategy**: Use one of the three differentiation strategies
4. **1688 Sourcing**: All products must be sourceable from 1688.com

## Questions and Clarifications

If you encounter unclear requirements during development:

1. Check the `requirement.md` file for original Chinese requirements
2. Review the profit calculation model (V4.1) carefully
3. Consider the business context: cross-border e-commerce from China to global markets

## External References

- **Temu**: Chinese cross-border e-commerce platform (PDD Holdings)
- **4supply.com**: Loktek's B2B platform (https://www.4supply.com/home)
- **1688.com**: Chinese wholesale marketplace (Alibaba Group)
- **Amazon Movers & Shakers**: Amazon's trending products page
