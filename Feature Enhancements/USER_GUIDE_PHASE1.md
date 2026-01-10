# Zambia Mining Intelligence Platform - Phase 1 User Guide

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Understanding the Metrics](#understanding-the-metrics)
4. [Feature Guide](#feature-guide)
5. [Interpreting the Analysis](#interpreting-the-analysis)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Overview

The Zambia Mining Intelligence Platform is a comprehensive data analysis tool designed to help identify, evaluate, and prioritize mining opportunities across Zambia. Phase 1 provides three core analytical capabilities:

### Core Capabilities
- **Resource Density Analysis** - Identify high-value mining sites
- **Geological Vein Mapping** - Visualize mineral belt patterns and trends
- **Accessibility Assessment** - Evaluate infrastructure and site access

### Dataset
- **369 validated mining sites** across Zambia
- **9 provinces** and **62+ districts** covered
- **100% data quality** - all critical fields complete and verified

---

## Getting Started

### Accessing the Platform

1. **Open the application** in your web browser
2. **Enter password**: `Claire&Goska` (or your custom password)
3. **Select a view mode** from the sidebar

### Navigation Structure

The platform has **4 main views**:
- 📊 **Overview** - Portfolio summary and key insights
- 🗺️ **Site Explorer** - Interactive map with filtering
- 💎 **Geological Analysis** - Vein mapping and geological patterns
- 🚗 **Accessibility** - Infrastructure and access evaluation

---

## Understanding the Metrics

### Density Score (0-100)

The **Density Score** measures the overall resource quality and development potential of a mining site.

#### Components:
| Component | Weight | What It Measures |
|-----------|--------|------------------|
| **Reserve Presence** | 40 points | Whether the site has documented mineral reserves |
| **Activity Status** | 30 points | Current operational status (Active = highest) |
| **Multi-Commodity** | 15 points | Presence of additional commodities (diversification) |
| **Geological Data** | 15 points | Quality of geological classification |

#### Interpretation:

**80-100: Very High Density** 🟣
- Prime development targets
- Well-documented reserves
- Active or recently active operations
- Strong geological data
- **Action**: Priority investigation

**60-79: High Density** 🔴
- Strong prospects
- Good documentation
- Likely active or feasible
- **Action**: Detailed evaluation

**40-59: Medium Density** 🟡
- Moderate potential
- May require more investigation
- Some data gaps possible
- **Action**: Secondary priority

**20-39: Low Density** 🟢
- Limited information or reserves
- May be early-stage exploration
- **Action**: Monitor for updates

**0-19: Very Low Density** 🔵
- Minimal data available
- Inactive or unknown status
- **Action**: Low priority

#### Example:
```
Site: Konkola Deep Mine
- Reserve: Yes (40 pts) ✓
- Status: Active (30 pts) ✓
- Multi-commodity: Copper + Cobalt (10 pts) ✓
- Geology: Well-documented (15 pts) ✓
Total Density Score: 95/100 (Very High)
```

---

### Accessibility Score (0-100)

The **Accessibility Score** measures how easily a site can be accessed and developed based on infrastructure and location.

#### Components:
| Component | Weight | What It Measures |
|-----------|--------|------------------|
| **Distance from Chingola** | 40 points | Proximity to your base operations (closer = better) |
| **Travel Time** | 30 points | Estimated road travel time from Chingola |
| **District Development** | 20 points | Infrastructure level in the district (# of sites = proxy) |
| **Province Infrastructure** | 10 points | Overall provincial infrastructure rating |

#### Interpretation:

**80-100: Excellent Access** 🟢
- Close to major roads/towns
- Short travel time from base
- Well-developed district
- **Advantages**: Lower logistics costs, easier site visits, faster mobilization
- **Example Districts**: Chingola, Kitwe, Lusaka areas

**60-79: Good Access** 🔵
- Reasonable distance from base
- Established road access
- Moderate infrastructure
- **Advantages**: Manageable logistics, regular access possible
- **Example Districts**: Kabwe, Mkushi

**40-59: Fair Access** 🟡
- Remote but reachable
- May require infrastructure investment
- Limited nearby facilities
- **Considerations**: Higher logistics costs, seasonal access issues
- **Example Districts**: Kasempa, Solwezi periphery

**0-39: Poor Access** 🔴
- Very remote locations
- Limited or poor road access
- Minimal nearby infrastructure
- **Considerations**: Significant infrastructure investment needed, high operating costs
- **Example Districts**: Remote parts of North-Western, Luapula provinces

#### Why It Matters:
- **Operating Costs**: Sites with poor access can cost 30-50% more to operate
- **Development Timeline**: Better access = faster project development
- **Risk**: Remote sites face supply chain vulnerabilities

---

### Resource Quality vs Accessibility Matrix

This is the **most important visualization** for prioritizing opportunities. It plots Density Score (Y-axis) against Accessibility Score (X-axis), creating four strategic quadrants.

```
                    High Density (80-100)
                           ↑
         Infrastructure    |    Priority
            Needed         |    Targets
         (High Value,      |    (High Value,
          Low Access)      |     High Access)
                           |
    ─────────────────────────────────────→
    Low Access (0-40)      |    High Access (80-100)
                           |
           Low             |    Quick
         Priority          |    Wins
         (Low Value,       |    (Accessible,
          Low Access)      |     Lower Value)
                           |
                    Low Density (0-40)
```

### Quadrant Strategies:

#### 🎯 **Priority Targets** (Top-Right: High Density + High Access)
- **Density**: 60-100
- **Access**: 60-100
- **Characteristics**:
  - Best opportunities for immediate development
  - Well-documented reserves
  - Good infrastructure
  - Lower risk profile
- **Strategy**: 
  - Detailed feasibility studies
  - Prioritize for acquisition/development
  - Fast-track evaluation
- **Typical Sites**: Active Copperbelt mines, Lusaka Province prospects

#### ⚠️ **Infrastructure Needed** (Top-Left: High Density + Low Access)
- **Density**: 60-100
- **Access**: 0-60
- **Characteristics**:
  - Significant mineral potential
  - Remote or underdeveloped areas
  - Requires infrastructure investment
  - Higher risk, higher reward
- **Strategy**:
  - Long-term development planning
  - Infrastructure cost-benefit analysis
  - Partnership opportunities (shared infrastructure)
  - Consider for bulk development projects
- **Considerations**:
  - Build access roads?
  - Power line extensions?
  - Water source development?
  - Hub-and-spoke approach?

#### ⚡ **Quick Wins** (Bottom-Right: Low Density + High Access)
- **Density**: 0-60
- **Access**: 60-100
- **Characteristics**:
  - Easy to access but lower documented value
  - May be early-stage exploration
  - Lower investment required
  - Good for small-scale operations
- **Strategy**:
  - Small-scale mining opportunities
  - Exploration drilling to upgrade resource
  - Low-cost entry points
  - Testing ground for methods

#### ⬜ **Low Priority** (Bottom-Left: Low Density + Low Access)
- **Density**: 0-60
- **Access**: 0-60
- **Characteristics**:
  - Limited information
  - Remote locations
  - Highest risk profile
- **Strategy**:
  - Monitor for future development
  - Wait for infrastructure improvements
  - Consider only if regional development occurs

---

### Geological Belt Analysis

Understanding mineral belts helps identify exploration targets and predict where similar deposits might occur.

#### Belt Metrics Explained:

**Sites in Belt**
- Number of deposits aligned along the trend
- More sites = more confidence in belt existence
- Example: Copper Belt has 112+ sites

**Belt Bearing (0-360°)**
- Compass direction of the mineral trend
- 0° = North, 90° = East, 180° = South, 270° = West
- Example: Copper Belt trends at ~45° (Northeast)
- **Use**: Predict where to explore along trend

**Belt Length**
- Physical extent of the mineral trend (in km)
- Longer belts = larger exploration potential
- Example: Copper Belt extends ~180 km
- **Use**: Define exploration area

**Linearity (0-100%)**
- How well deposits align in a straight line
- 70-100% = Strong linear pattern (well-defined belt)
- 40-70% = Moderate pattern (some alignment)
- 0-40% = Scattered deposits
- **Use**: Confidence in belt existence and trend prediction

#### Interpreting Trend Lines on Maps:

**Strong Linear Belt (Linearity >70%)**
```
Site ─────── Site ─────── Site ─────── Site
         ↗ 45° bearing
    [Clear trend line visible on map]
```
- **Meaning**: Geologically controlled deposits
- **Action**: Explore along trend line, especially gaps between sites

**Moderate Pattern (Linearity 40-70%)**
```
    Site         Site
         Site  
    Site         Site
       [Trend line with some scatter]
```
- **Meaning**: Geological control present but complex
- **Action**: Focus on clusters, investigate geological controls

---

## Feature Guide

### 📊 Overview Dashboard

**Purpose**: Get a quick snapshot of your entire mining portfolio

**Key Metrics Displayed:**
- Total Sites (filtered count)
- Active Sites (% of total)
- Average Density Score (portfolio quality)
- Average Access Score (portfolio accessibility)

**Charts:**
1. **Commodity Distribution** (Bar Chart)
   - Shows top 10 commodities by site count
   - Identify your commodity concentration
   - Example: If 60% Copper, portfolio is copper-focused

2. **Geographic Distribution** (Pie Chart)
   - Sites by province
   - Identify geographic concentration
   - Example: 40% in Copperbelt = focused on established mining region

3. **Top Districts** (Horizontal Bar Chart)
   - Districts with most sites
   - Identify mining hubs
   - Districts like Mkushi (116 sites) indicate major opportunities

4. **Resource Quality vs Accessibility** (Scatter Plot)
   - **Most important chart!**
   - Each dot = one mining site
   - Color = commodity type
   - Position = strategic priority
   - Use quadrants (explained above) to identify targets

**How to Use:**
1. Start here every session to understand current filtered data
2. Check if filters are working (compare total sites to expectations)
3. Identify which quadrant has most opportunities
4. Note commodity and geographic concentrations

---

### 🗺️ Site Explorer

**Purpose**: Interactively explore and filter mining sites on a map

#### Map Controls:

**Color By** (Choose what colors represent):
- **Density Category**: See resource quality (Very Low → Very High)
- **Access Category**: See infrastructure quality (Poor → Excellent)
- **Primary Commodity**: See commodity distribution
- **Status**: See operational status
- **Province**: See geographic groupings

**Size By** (Choose what size represents):
- **Density Score**: Bigger = higher resource quality
- **Accessibility Score**: Bigger = better access
- **Uniform**: All same size (cleaner map)

#### Understanding the Map:

**Red Star** = Chingola Base (your operations center)
- Use this to visually estimate distances
- Sites near the star = closer to base

**Markers**:
- Click any marker for details
- Hover to see quick info
- Size indicates importance (if size mode selected)

**Clusters** (if enabled):
- Groups of nearby sites
- Indicates resource concentrations
- High-value clusters = development hubs

#### How to Use:

**Find Priority Targets:**
1. Color By: "Density Category"
2. Size By: "Density Score"  
3. Look for large purple/red markers (Very High/High density)
4. Click markers near Chingola (red star) = best priorities

**Assess Accessibility:**
1. Color By: "Access Category"
2. Green markers = Excellent access
3. Red markers = Poor access
4. Cross-reference with density to find priority targets

**Explore Commodities:**
1. Color By: "Primary Commodity"
2. Filter to specific commodity (sidebar)
3. See spatial distribution
4. Identify commodity clusters

---

### 💎 Geological Analysis

**Purpose**: Understand geological patterns and mineral belt structures

#### Two Tabs:

**1. Site Distribution**
- Shows all sites colored by commodity
- Marker size = Density Score
- Use to see overall commodity distribution
- Identify multi-commodity zones

**2. Geological Patterns** ⭐
- Shows sites colored by geology type
- **Trend lines** show mineral belt directions
- **Most useful for exploration planning**

#### Reading Trend Lines:

**Red Line** = Copper Belt trend
**Gold Line** = Gold belt trend  
**Orange Line** = Iron belt trend

**What Trend Lines Tell You:**
1. **Direction**: Which way the mineralization extends
2. **Extent**: How far the belt continues
3. **Gaps**: Unexplored areas along trend (opportunities!)

**Example - Copper Belt:**
```
     Kitwe ●──────●──────●──────● Mufulira
              ↗ 45° NE trend
    [Red line shows ~180km belt extent]
```

**Exploration Strategy:**
- Sites along trend line = higher success probability
- Gaps in coverage = exploration targets
- Extensions beyond known deposits = frontier opportunities

#### Belt Metrics Section:

Located below the map, shows 4 key numbers:

**Sites in Belt**: Total deposits in alignment
- More sites = more confidence
- Example: 112 sites confirms strong belt

**Belt Bearing**: Direction in degrees
- 0° = North, 90° = East, 180° = South, 270° = West
- Example: 45° = Northeast trend
- Use for directional drilling, claim staking

**Belt Length**: Physical extent in km
- Defines exploration area
- Example: 180 km = extensive belt system

**Linearity**: Pattern strength (%)
- >70% = Strong, predictable pattern
- 40-70% = Moderate, some scatter
- <40% = Weak pattern, scattered deposits

#### Expandable Sections:

**📊 Detailed Belt Analysis**
- Narrative description of belt characteristics
- Statistical details
- Pattern interpretation
- Click to expand for full technical description

**🧪 Geological Formation Details**
- Table of geology types
- Site counts per formation
- Spatial extent data
- Top commodity per geology type

---

### 🚗 Accessibility Analysis

**Purpose**: Evaluate infrastructure and site accessibility for operational planning

#### Accessibility Map:

**Color Coding:**
- 🟢 Green = Excellent (80-100 score)
- 🔵 Blue = Good (60-79 score)
- 🟡 Amber = Fair (40-59 score)
- 🔴 Red = Poor (0-39 score)

**Marker Size** = Accessibility Score (bigger = better access)

**Red Star** = Chingola Base (distance reference)

#### Regional Statistics:

**Top Provinces by Accessibility**
- Shows average access scores by province
- Identifies best-developed regions
- Example: Copperbelt (avg 90) vs North-Western (avg 35)

**Top Districts by Accessibility**
- District-level access rankings
- Find local infrastructure hubs
- Example: Kitwe, Chingola districts = excellent

#### Infrastructure Gaps Table:

**Critical Feature for Planning!**

Shows high-value sites (Density >60) with poor access (<60).

**Columns:**
- **Property Name**: Site identifier
- **Province/District**: Location
- **Commodity**: What's there
- **Density Score**: Resource value (60-100)
- **Accessibility Score**: Current access (0-60)
- **Access Gap**: How much improvement needed
- **Infrastructure Priority**: Combined score (higher = more urgent)

**How to Use:**
1. Sort by Infrastructure Priority (highest first)
2. These are sites worth infrastructure investment
3. Consider:
   - Is access improvement feasible?
   - Are multiple sites nearby (shared infrastructure)?
   - What's the payback period?

**Example Decision:**
```
Site: ABC Mine
Density: 85 (Very High)
Access: 35 (Poor)
Gap: 25 points
Priority: 2,125

Analysis:
- High-value target
- Currently difficult to reach
- Build access road? Cost: $500K
- Expected return: $50M reserve value
- Decision: INVEST in infrastructure
```

---

## Interpreting the Analysis

### Step-by-Step Analysis Workflow

#### 1. Portfolio Overview (5 minutes)
```
Start: Overview Dashboard
↓
Check: Total sites, Active %
↓
Review: Commodity distribution
↓
Study: Resource Quality vs Accessibility chart
↓
Identify: Which quadrant has most sites?
```

**Deliverable**: Understanding of portfolio composition

#### 2. Priority Target Identification (10 minutes)
```
Go to: Overview → Resource Quality chart
↓
Look for: Green quadrant (Priority Targets)
↓
Count: How many high-density + high-access sites?
↓
Switch to: Site Explorer
↓
Filter: Density Mode = "Top Sites" (20)
Filter: Min Accessibility = 60
↓
Result: Your top 20 priority targets
```

**Deliverable**: List of immediate opportunities

#### 3. Geological Exploration Planning (15 minutes)
```
Go to: Geological Analysis
↓
Select: Your target commodity (e.g., Copper)
↓
Tab: Geological Patterns
↓
Observe: Trend line direction and length
↓
Note: Belt bearing (e.g., 45° NE)
↓
Identify: Gaps along trend line
↓
Expand: Detailed Belt Analysis
```

**Deliverable**: Exploration target zones

#### 4. Infrastructure Investment Assessment (10 minutes)
```
Go to: Accessibility tab
↓
Scroll to: Infrastructure Gaps table
↓
Sort by: Infrastructure Priority (descending)
↓
For each high-priority site:
  - Check location on map
  - Note nearby sites (shared infrastructure?)
  - Estimate access improvement cost
↓
Calculate: Cost vs potential value
```

**Deliverable**: Infrastructure investment recommendations

---

### Real-World Scenarios

#### Scenario 1: Finding Your Next Acquisition Target

**Goal**: Identify best site for immediate development

**Steps:**
1. **Overview** → Check Resource Quality vs Accessibility
   - Focus on green quadrant (Priority Targets)
   
2. **Site Explorer** → Apply filters:
   - Commodity: Your focus (e.g., Copper)
   - Display Mode: "Top Sites" (10)
   - Min Accessibility: 70
   
3. **For each site** → Evaluate:
   - Density Score >80? (Strong reserves)
   - Active or Feasibility status? (De-risked)
   - Province: Copperbelt/Central? (Established region)
   
4. **Geological Analysis** → Verify:
   - On known belt trend? (Lower exploration risk)
   - Similar geology to producing mines?
   
5. **Result**: Shortlist of 3-5 best targets for detailed due diligence

---

#### Scenario 2: Regional Development Strategy

**Goal**: Plan infrastructure for multiple sites in one region

**Steps:**
1. **Site Explorer** → Filter:
   - Province: Select target province
   - Density Mode: "Top Sites" (50)
   - Enable: "Show Density Clusters"
   
2. **Identify** → Major clusters:
   - Look for groups of 10+ sites within 20km
   - Check average density scores
   
3. **Accessibility** → Infrastructure assessment:
   - Check regional accessibility statistics
   - Review infrastructure gaps in that region
   
4. **Calculate** → Hub-and-spoke potential:
   - Central hub location (best access)
   - Spoke roads to satellite sites
   - Shared facilities (water, power, processing)
   
5. **Result**: Multi-site development plan with shared infrastructure

---

#### Scenario 3: Exploration Program Design

**Goal**: Identify where to stake new claims

**Steps:**
1. **Geological Analysis** → Select commodity
   - Tab: Geological Patterns
   - Enable: Show Trend Lines
   
2. **Study** → Belt characteristics:
   - Note bearing (e.g., 45° NE)
   - Measure belt length (e.g., 180 km)
   - Check linearity (>70% = strong)
   
3. **Identify** → Gaps:
   - Find 10-20km sections without sites
   - Look for trend line extensions beyond known deposits
   
4. **Expand** → Detailed Belt Analysis:
   - Review geological controls
   - Check similar geology types
   
5. **Overlay** → Accessibility:
   - Check if gap areas are accessible
   - Balance exploration potential vs access costs
   
6. **Result**: Prioritized exploration target coordinates

---

#### Scenario 4: Portfolio Optimization

**Goal**: Divest poor performers, focus on winners

**Steps:**
1. **Overview** → Resource Quality chart:
   - Identify sites in "Low Priority" quadrant (bottom-left)
   - Note count and commodity types
   
2. **Site Explorer** → Review bottom sites:
   - Display Mode: "Bottom Sites" (20)
   - Check status (many will be Inactive/Dormant)
   
3. **For each low performer** → Assess:
   - Density Score <40? (Weak documentation)
   - Accessibility Score <40? (Hard to reach)
   - Status: Inactive? (No current operations)
   
4. **Decision Framework**:
   - Can data be improved? (Exploration work?)
   - Is access improvable? (Infrastructure projects?)
   - Is there strategic value? (Future belt extension?)
   - If all "No" → Divest candidate
   
5. **Result**: List of assets to divest or dormant holdings to abandon

---

## Best Practices

### Filtering Strategy

**Start Broad, Then Narrow:**
```
1. All Sites (369) → Understand full dataset
2. Filter by Commodity → Focus your sector
3. Apply Density filter → Quality threshold  
4. Add Accessibility filter → Operational feasibility
5. Province/District filter → Regional focus
```

**Don't Over-Filter:**
- Too many filters = may miss opportunities
- Always check "Total Sites" after filtering
- If <10 sites, you've filtered too much

### Using Multiple Views Together

**Power Combination:**
```
Overview (Identify quadrant)
    ↓
Site Explorer (See spatial distribution)
    ↓
Geological (Understand belt context)
    ↓
Accessibility (Evaluate logistics)
    ↓
Back to Overview (Verify findings)
```

### Density Thresholds by Strategy

**Conservative Strategy:** Density >70
- Focus on proven resources
- Lower risk, lower return
- Good for: Public companies, risk-averse investors

**Balanced Strategy:** Density >50
- Mix of proven and potential
- Moderate risk/return
- Good for: Most operators

**Aggressive Strategy:** Density >40
- Include early-stage prospects
- Higher risk, higher upside
- Good for: Exploration companies, risk capital

### Documentation Tips

**For Each Priority Target:**
1. Screenshot the site on map
2. Note all 4 metrics (Density, Access, Province, Commodity)
3. Save belt bearing if on known trend
4. Export site list (use Streamlit data export)
5. Create evaluation folder per site

---

## Troubleshooting

### Common Issues

**"No data showing on map"**
- Check if filters are too restrictive
- Reset filters (reload page)
- Verify commodity selection ("All" shows everything)

**"Trend lines not visible"**
- Ensure "Show Trend Lines" is checked ✓
- Select specific commodity (trend lines only for main commodities)
- Zoom out to see full extent
- Check you're on "Geological Patterns" tab

**"Legend text too small"**
- This has been fixed in latest version
- Reload page / clear cache
- Update to latest app version

**"Map loads slowly"**
- Reduce number of sites displayed
- Filter to specific province/district
- Disable cluster visualization
- Close other browser tabs

**"Infrastructure gaps table is empty"**
- No sites meet criteria (Density >60 + Access <60)
- Adjust density filter in sidebar
- Try "All" sites mode instead of "Top Sites"

### Performance Tips

**For Large Datasets:**
1. Filter by Province first (reduces processing)
2. Use "Top Sites" mode (20-50 sites)
3. Disable clusters if not needed
4. One map view at a time

**For Presentations:**
1. Pre-filter to target sites
2. Zoom to area of interest
3. Use "Uniform" size for cleaner look
4. Take screenshots for reports

---

## Glossary

**Active Site**: Currently operational mining site
**Bearing**: Compass direction (0° = North, 90° = East, etc.)
**Belt**: Linear alignment of mineral deposits
**Cluster**: Group of nearby mining sites (typically <20km apart)
**Density Score**: Composite metric of resource quality (0-100)
**Linearity**: Measure of how straight a mineral belt is (%)
**Priority Target**: High density + high accessibility site
**Quadrant**: One of four strategic zones in Resource Quality chart
**Trend Line**: Geological direction of mineral belt
**Vein**: Mineral-bearing geological structure

---

## Quick Reference Card

### Key Metrics Cheat Sheet

| Metric | Range | Excellent | Good | Fair | Poor |
|--------|-------|-----------|------|------|------|
| Density Score | 0-100 | 80+ | 60-79 | 40-59 | <40 |
| Accessibility | 0-100 | 80+ | 60-79 | 40-59 | <40 |
| Linearity | 0-100% | 70%+ | 50-69% | 30-49% | <30% |

### Strategic Priority Matrix

| Density | Access | Priority | Action |
|---------|--------|----------|--------|
| High (>60) | High (>60) | ⭐⭐⭐⭐⭐ | ACQUIRE NOW |
| High (>60) | Low (<60) | ⭐⭐⭐⭐ | PLAN INFRASTRUCTURE |
| Low (<60) | High (>60) | ⭐⭐⭐ | EXPLORE / SMALL SCALE |
| Low (<60) | Low (<60) | ⭐ | MONITOR ONLY |

---

## Contact & Support

For questions, issues, or feature requests regarding the Zambia Mining Intelligence Platform, please contact your system administrator.

**Version**: Phase 1.0  
**Last Updated**: January 2026  
**Dataset**: 369 sites, 100% validated

---

*This guide covers Phase 1 features. Phase 2 will add reserve quantification, LME price integration, and valuation capabilities.*
