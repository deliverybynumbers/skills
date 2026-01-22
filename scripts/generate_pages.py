#!/usr/bin/env python3
"""
Generate markdown role pages from SFIA skill definitions.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add scripts directory to path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from parse_sfia import parse_sfia_csv, SFIASkill


# Role definitions: mapping role types to their required SFIA skill codes
ROLE_SKILLS = {
    "software-engineer": ["SWDN", "PROG", "ARCH", "DBAD", "DEPL"],
    "security-engineer": ["IRMG", "SCTY", "PENT"],
    "support-engineer": ["CSMG", "ASUP", "INCA"],
    "systems-engineer": ["SYSP", "CHMG", "ITOP", "ASMG", "DEMM", "DCMA", "USUP"],
    "qa-engineer": ["TEST", "NFTS", "QUAS", "BPTS"],
    "product-management": ["PROD", "REQM", "BSMO", "CEXP", "DEMG"],
    "people-management": ["ETMG", "POMG", "SORC", "SUPP"],
}

# Role titles by path and level
ROLE_TITLES = {
    "engineering": {
        1: "Associate {type} Engineer",
        2: "{type} Engineer",
        3: "Senior {type} Engineer",
        4: "Lead {type} Engineer",
        5: "Principal {type} Engineer",
        6: "Distinguished {type} Engineer",
        7: "Chief {type} Engineer",
    },
    "management": {
        4: "Engineering Manager",
        5: "Senior Engineering Manager",
        6: "Director of Engineering",
        7: "VP of Engineering",
    },
    "product": {
        3: "Business Analyst",
        4: "Product Manager",
        5: "Senior Product Manager",
        6: "Director of Product",
        7: "VP of Product",
    },
    "programmes": {
        2: "Project Assistant",
        3: "Project Manager",
        4: "Programme Manager",
        5: "Senior Programme Manager",
        6: "Director of Programmes",
    },
}

# Engineer type display names
ENGINEER_TYPES = {
    "software-engineer": "Software",
    "security-engineer": "Security",
    "support-engineer": "Support",
    "systems-engineer": "Systems",
    "qa-engineer": "QA",
}

# General framework guidance from the PDF
FRAMEWORK_OVERVIEW = """## Framework Overview

Our approach is built around a small number of core ideas that shape engineering progression:

- **Impact-focused**: We focus on the impact each engineer has on moving the business forward, rather than on long lists of specific skills and behaviours.
- **Scope increases with seniority**: As you grow, so does the complexity and size of the problems you are expected to solve. As the business grows, the engineering challenges should grow with it.
- **Simple and meaningful**: This framework brings the most important behaviours and expectations together in a simple way. It is not meant to cover everything an engineer might do, but to highlight the meaningful differences between levels.
- **Broad behaviours**: Behaviours are intentionally broad so they reflect the many ways engineers can contribute. Our aim is to describe the level of technical contribution and mindset we expect at each stage, not create a checklist of tasks.
- **Supporting conversations**: We want to make space for the different ways people add value. This framework exists to support 1:1s, performance reviews and development conversations, helping managers and engineers talk clearly about scope, impact and alignment with our engineering principles.
- **Practice-focused**: The framework focuses on the practice of engineering itself, not the specific tools or languages you use.

**Levels are cumulative**: Each level builds on the one before it. Engineers are expected to show the behaviours and technical habits of earlier levels as they progress.

### Impact

Impact is the primary driver for progression. Your impact reflects your sphere of influence and the contribution you make to our mission and goals. Different roles and disciplines create impact in different ways. Focusing on impact allows us to recognise engineers who move things forward (and who "get things done") without requiring them to perform specific routines.

Impact grows through a mix of building technical skill, gaining real experience, learning from that experience and pairing it with the right behaviours.

**Excellence here looks like:**

- Choosing work that meaningfully moves your team, discipline and the business forward, in line with the scope of your role.
- Identifying opportunities to improve engineering outcomes and making them clear so the team can prioritise effectively.
- Consistently getting things done, contributing to the team and earning a reputation as a reliable, high-quality engineer.

### Technical Skills

This section is about how you apply your technical ability and develop your craft. It describes the behaviours that show effective technical contribution at different levels of complexity and ambiguity.

We look at technical contribution through four lenses: quality, testability, performance and your ability to design and review systems.

**Excellence here looks like:**

- Your code and technical work are considered high quality by your peers and senior engineers.
- You can design systems that solve business problems efficiently and reduce ambiguity at both the technical and product level.
- You design with the right level of complexity, keeping things simple where possible.
- Your work is resilient, well tested and capable of scaling as the business grows.

### Behaviours

Behaviours sit alongside technical skills and impact. They cover the core habits, mindsets and ways of working we expect engineers to show.

Through your behaviour you set the tone for those around you. Great engineers role model great behaviours, and self-aware engineers know when they are setting a strong example.

Behaviours reflect consistent habits and intentional choices, rather than doing the right thing by chance or on "autopilot".

"""

# Level-specific scope summaries and descriptions (from PDF)
LEVEL_DESCRIPTIONS = {
    1: {
        "scope_summary": "A new engineer at the start of their career, focussed on expanding their knowledge and skill set to further increase their impact within a team.",
        "description": "Associate Engineers are at the first stage of their software engineering career. They're contributing to the team's goals through executing on well-defined tasks, with support from more experienced engineers. As someone early in their career, they're focussed on increasing their Software Engineering skill set and knowledge at a high pace. So that they can start to deliver tasks with less support and progress towards \"Engineer\"."
    },
    2: {
        "scope_summary": "An engineer with high potential, developing the fundamentals they need to be successful in their team.",
        "description": "Engineer engineers are in the earlier stages of their software engineering career. They're working on well-defined tasks and are supported by the team when stuck. They're expected to ask lots of questions. As someone progresses toward \"Senior Engineer\" they should start to gain confidence to pick up larger or less well-defined tasks with less required support."
    },
    # Note: The PDF only had descriptions for levels 1-2. For other levels, we'll use generic descriptions
    # that can be customized later
}

def get_level_description(level: int, role_path: str) -> Dict[str, str]:
    """Get level-specific description from PDF or generate generic one."""
    if level in LEVEL_DESCRIPTIONS:
        return LEVEL_DESCRIPTIONS[level]

    # Generic descriptions for levels not in PDF
    generic_descriptions = {
        3: {
            "scope_summary": "An experienced engineer who works independently on complex tasks and contributes significantly to team success.",
            "description": "Senior Engineers demonstrate strong technical skills and work independently on complex problems. They contribute to team success through their technical expertise and collaborative approach."
        },
        4: {
            "scope_summary": "A technical leader who guides and enables others while delivering significant technical contributions.",
            "description": "Lead Engineers combine strong technical skills with leadership capabilities. They enable others to succeed while continuing to make significant technical contributions."
        },
        5: {
            "scope_summary": "A senior technical expert who influences engineering practices across the organisation.",
            "description": "Principal Engineers are recognised technical experts who influence engineering practices, standards and approaches across the organisation."
        },
        6: {
            "scope_summary": "An exceptional technical leader recognised for outstanding contributions to engineering excellence.",
            "description": "Distinguished Engineers are exceptional technical leaders recognised for their outstanding contributions to engineering excellence and organisational impact."
        },
        7: {
            "scope_summary": "The senior technical leader responsible for setting technical strategy and direction.",
            "description": "The Chief Engineer sets technical strategy and direction for the organisation, inspiring and mobilising teams to achieve engineering excellence."
        }
    }

    return generic_descriptions.get(level, {
        "scope_summary": f"Level {level} role in the {role_path.title()} career path.",
        "description": f"This role represents Level {level} in the {role_path.title()} career path."
    })


def generate_role_page(
    role_path: str,
    role_type: str,
    level: int,
    skills: Dict[str, SFIASkill],
    role_skills: List[str],
    output_dir: Path,
) -> None:
    """Generate a markdown page for a specific role."""

    # Get role title
    if role_path == "engineering":
        engineer_type = ENGINEER_TYPES.get(role_type, role_type.title())
        title_template = ROLE_TITLES["engineering"][level]
        title = title_template.format(type=engineer_type)
    else:
        title = ROLE_TITLES[role_path][level]

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate markdown content
    content = f"# {title}\n\n"
    content += f"**Level {level}** | **Career Path:** {role_path.title()}\n\n"

    if role_path == "engineering":
        content += f"**Engineer Type:** {engineer_type}\n\n"

    content += "---\n\n"

    # Add framework overview and guidance
    content += FRAMEWORK_OVERVIEW

    # Add level-specific scope summary and description
    level_desc = get_level_description(level, role_path)
    content += "## Role Overview\n\n"
    content += f"**Scope Summary:** {level_desc['scope_summary']}\n\n"
    content += f"{level_desc['description']}\n\n"

    content += "---\n\n"
    content += "## Required SFIA Skills\n\n"
    content += "The following SFIA skills define the expected skills and behaviors for this role at this level:\n\n"

    # Add each skill
    for skill_code in role_skills:
        if skill_code not in skills:
            print(f"Warning: Skill {skill_code} not found in SFIA data", file=sys.stderr)
            continue

        skill = skills[skill_code]
        level_desc = skill.get_level_description(level)

        if not level_desc:
            # Try to find the closest available level
            available_levels = sorted(skill.level_descriptions.keys())
            if available_levels:
                # Use the highest level that's <= target level, or lowest if all are higher
                suitable_levels = [l for l in available_levels if l <= level]
                if suitable_levels:
                    level_desc = skill.get_level_description(max(suitable_levels))
                else:
                    level_desc = skill.get_level_description(min(available_levels))

        content += f"### {skill.name} ({skill_code})\n\n"

        if skill.url:
            content += f"**SFIA Reference:** [{skill_code}]({skill.url})\n\n"

        content += f"**Category:** {skill.category} | **Subcategory:** {skill.subcategory}\n\n"

        content += f"**Overall Description:**\n\n"
        content += f"{skill.overall_description}\n\n"

        if skill.guidance_notes:
            content += f"**Guidance Notes:**\n\n"
            content += f"{skill.guidance_notes}\n\n"

        if level_desc:
            content += f"**Level {level} Attainment:**\n\n"
            content += f"{level_desc}\n\n"
        else:
            content += f"*Note: Level {level} description not available for this skill.*\n\n"

        content += "---\n\n"

    # Add navigation links
    content += "## Navigation\n\n"

    # Determine valid level range for this path
    if role_path == "engineering":
        min_level, max_level = 1, 7
        level_filenames = {
            1: "level-1-associate.md",
            2: "level-2-engineer.md",
            3: "level-3-senior.md",
            4: "level-4-lead.md",
            5: "level-5-principal.md",
            6: "level-6-distinguished.md",
            7: "level-7-chief.md"
        }
    elif role_path == "management":
        min_level, max_level = 4, 7
        level_filenames = {
            4: "level-4-engineering-manager.md",
            5: "level-5-senior-engineering-manager.md",
            6: "level-6-director-of-engineering.md",
            7: "level-7-vp-of-engineering.md"
        }
    elif role_path == "product":
        min_level, max_level = 3, 7
        level_filenames = {
            3: "level-3-business-analyst.md",
            4: "level-4-product-manager.md",
            5: "level-5-senior-product-manager.md",
            6: "level-6-director-of-product.md",
            7: "level-7-vp-of-product.md"
        }
    elif role_path == "programmes":
        min_level, max_level = 2, 6
        level_filenames = {
            2: "level-2-project-assistant.md",
            3: "level-3-project-manager.md",
            4: "level-4-programme-manager.md",
            5: "level-5-senior-programme-manager.md",
            6: "level-6-director-of-programmes.md"
        }
    else:
        min_level, max_level = 1, 7
        level_filenames = {}

    nav_links = []

    # Previous level link
    if level > min_level:
        prev_level = level - 1
        prev_filename = level_filenames.get(prev_level, f"level-{prev_level}.md")
        prev_title_text = ROLE_TITLES[role_path][prev_level]
        if role_path == "engineering":
            prev_title_text = prev_title_text.format(type=engineer_type)
        nav_links.append(f"← [Previous: {prev_title_text}]({prev_filename})")

    # Next level link
    if level < max_level:
        next_level = level + 1
        next_filename = level_filenames.get(next_level, f"level-{next_level}.md")
        next_title_text = ROLE_TITLES[role_path][next_level]
        if role_path == "engineering":
            next_title_text = next_title_text.format(type=engineer_type)
        nav_links.append(f"[Next: {next_title_text}]({next_filename}) →")

    if nav_links:
        content += "**Career Path Navigation:** " + " | ".join(nav_links) + "\n\n"

    # Link back to index
    if role_path == "engineering":
        index_path = "../../../index.md"
    else:
        index_path = "../../index.md"
    content += f"**Back to:** [Home]({index_path})\n\n"

    # Write file
    filename = f"level-{level}-{role_type.replace('_', '-')}.md"
    if role_path == "engineering":
        # Special handling for engineering roles
        if level == 1:
            filename = "level-1-associate.md"
        elif level == 2:
            filename = "level-2-engineer.md"
        elif level == 3:
            filename = "level-3-senior.md"
        elif level == 4:
            filename = "level-4-lead.md"
        elif level == 5:
            filename = "level-5-principal.md"
        elif level == 6:
            filename = "level-6-distinguished.md"
        elif level == 7:
            filename = "level-7-chief.md"
    else:
        # For other paths, use descriptive names
        slug = title.lower().replace(" ", "-").replace(" of ", "-of-")
        filename = f"level-{level}-{slug}.md"

    output_file = output_dir / filename
    output_file.write_text(content, encoding='utf-8')
    print(f"Generated: {output_file}")


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    csv_path = repo_root / "input" / "sfia-9_current-standard_en_250129(Skills).csv"
    docs_dir = repo_root / "docs"

    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}", file=sys.stderr)
        sys.exit(1)

    print("Parsing SFIA CSV...")
    skills = parse_sfia_csv(csv_path)
    print(f"Parsed {len(skills)} skills\n")

    # Generate engineering role pages (levels 1-7)
    print("Generating engineering role pages...")
    for engineer_type in ["software-engineer", "security-engineer", "support-engineer",
                          "systems-engineer", "qa-engineer"]:
        role_skills = ROLE_SKILLS[engineer_type]
        for level in range(1, 8):
            output_dir = docs_dir / "roles" / "engineering" / engineer_type
            generate_role_page(
                "engineering",
                engineer_type,
                level,
                skills,
                role_skills,
                output_dir,
            )

    # Generate management role pages (levels 4-7)
    print("\nGenerating management role pages...")
    role_skills = ROLE_SKILLS["people-management"]
    for level in range(4, 8):
        output_dir = docs_dir / "roles" / "management"
        generate_role_page(
            "management",
            "engineering-manager",
            level,
            skills,
            role_skills,
            output_dir,
        )

    # Generate product role pages (levels 3-7)
    print("\nGenerating product role pages...")
    role_skills = ROLE_SKILLS["product-management"]
    for level in range(3, 8):
        output_dir = docs_dir / "roles" / "product"
        generate_role_page(
            "product",
            "product-manager",
            level,
            skills,
            role_skills,
            output_dir,
        )

    # Generate programmes role pages (levels 2-6)
    print("\nGenerating programmes role pages...")
    # Note: Programmes roles might need different skills - using a placeholder for now
    # You may want to add specific skills for programmes management
    role_skills = ["POMG"]  # Portfolio management as placeholder
    for level in range(2, 7):
        output_dir = docs_dir / "roles" / "programmes"
        generate_role_page(
            "programmes",
            "programme-manager",
            level,
            skills,
            role_skills,
            output_dir,
        )

    print("\nDone! All role pages generated.")


if __name__ == "__main__":
    main()
