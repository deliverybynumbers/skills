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
# Note: Some skills are level-specific (e.g., senior leadership skills for levels 6-7)
ROLE_SKILLS = {
    "software-engineer": {
        "base": ["SWDN", "PROG", "ARCH", "DBAD", "DEPL"],  # Levels 2-5
        "senior": ["SLEN", "DLMG"],  # Add for levels 6-7 (lifecycle engineering, development management)
        "strategic": ["STPL"],  # Add for level 7 (enterprise architecture)
    },
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

# Level-specific scope summaries and descriptions by career path
ENGINEERING_LEVEL_DESCRIPTIONS = {
    1: {
        "scope_summary": "A new engineer at the start of their career, focussed on expanding their knowledge and skill set to further increase their impact within a team.",
        "description": "Associate Engineers are at the first stage of their software engineering career. They're contributing to the team's goals through executing on well-defined tasks, with support from more experienced engineers. As someone early in their career, they're focussed on increasing their Software Engineering skill set and knowledge at a high pace. So that they can start to deliver tasks with less support and progress towards \"Engineer\"."
    },
    2: {
        "scope_summary": "An engineer with high potential, developing the fundamentals they need to be successful in their team.",
        "description": "Engineers are in the earlier stages of their software engineering career. They're working on well-defined tasks and are supported by the team when stuck. They're expected to ask lots of questions. As someone progresses toward \"Senior Engineer\" they should start to gain confidence to pick up larger or less well-defined tasks with less required support."
    },
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

MANAGEMENT_LEVEL_DESCRIPTIONS = {
    4: {
        "scope_summary": "A people leader who guides and enables engineering teams while delivering significant management contributions.",
        "description": "Engineering Managers combine strong technical understanding with leadership capabilities. They enable their teams to succeed while managing people, processes, and resources effectively."
    },
    5: {
        "scope_summary": "A senior people leader who influences engineering management practices across the organisation.",
        "description": "Senior Engineering Managers are recognised leaders who influence engineering management practices, team structures, and people development approaches across the organisation."
    },
    6: {
        "scope_summary": "An exceptional people leader recognised for outstanding contributions to engineering management excellence.",
        "description": "Directors of Engineering are exceptional people leaders recognised for their outstanding contributions to engineering management excellence, organisational culture, and strategic impact."
    },
    7: {
        "scope_summary": "The senior people leader responsible for setting engineering management strategy and direction.",
        "description": "The VP of Engineering sets engineering management strategy and direction for the organisation, inspiring and mobilising teams to achieve engineering excellence through effective people leadership."
    }
}

PRODUCT_LEVEL_DESCRIPTIONS = {
    3: {
        "scope_summary": "An experienced product professional who works independently on complex product tasks and contributes significantly to product success.",
        "description": "Business Analysts demonstrate strong analytical skills and work independently on complex product problems. They contribute to product success through their expertise in requirements, business modelling, and collaborative approach."
    },
    4: {
        "scope_summary": "A product leader who guides and enables product development while delivering significant product contributions.",
        "description": "Product Managers combine strong product skills with leadership capabilities. They enable product teams to succeed while continuing to make significant contributions to product strategy and delivery."
    },
    5: {
        "scope_summary": "A senior product expert who influences product practices across the organisation.",
        "description": "Senior Product Managers are recognised product experts who influence product practices, standards, and approaches across the organisation."
    },
    6: {
        "scope_summary": "An exceptional product leader recognised for outstanding contributions to product excellence.",
        "description": "Directors of Product are exceptional product leaders recognised for their outstanding contributions to product excellence and organisational impact."
    },
    7: {
        "scope_summary": "The senior product leader responsible for setting product strategy and direction.",
        "description": "The VP of Product sets product strategy and direction for the organisation, inspiring and mobilising teams to achieve product excellence."
    }
}

PROGRAMMES_LEVEL_DESCRIPTIONS = {
    2: {
        "scope_summary": "A programme professional with high potential, developing the fundamentals they need to be successful in programme delivery.",
        "description": "Project Assistants are in the earlier stages of their programme management career. They're working on well-defined tasks and are supported by the team when stuck. They're expected to ask lots of questions. As someone progresses toward \"Project Manager\" they should start to gain confidence to pick up larger or less well-defined tasks with less required support."
    },
    3: {
        "scope_summary": "An experienced programme professional who works independently on complex project tasks and contributes significantly to project success.",
        "description": "Project Managers demonstrate strong project management skills and work independently on complex project problems. They contribute to project success through their expertise in planning, coordination, and collaborative approach."
    },
    4: {
        "scope_summary": "A programme leader who guides and enables programme delivery while delivering significant programme contributions.",
        "description": "Programme Managers combine strong programme management skills with leadership capabilities. They enable programme teams to succeed while continuing to make significant contributions to programme strategy and delivery."
    },
    5: {
        "scope_summary": "A senior programme expert who influences programme practices across the organisation.",
        "description": "Senior Programme Managers are recognised programme experts who influence programme practices, standards, and approaches across the organisation."
    },
    6: {
        "scope_summary": "An exceptional programme leader recognised for outstanding contributions to programme excellence.",
        "description": "Directors of Programmes are exceptional programme leaders recognised for their outstanding contributions to programme excellence and organisational impact."
    }
}

def get_level_description(level: int, role_path: str) -> Dict[str, str]:
    """Get level-specific description based on career path."""
    # Select the appropriate description dictionary based on career path
    if role_path == "engineering":
        descriptions = ENGINEERING_LEVEL_DESCRIPTIONS
    elif role_path == "management":
        descriptions = MANAGEMENT_LEVEL_DESCRIPTIONS
    elif role_path == "product":
        descriptions = PRODUCT_LEVEL_DESCRIPTIONS
    elif role_path == "programmes":
        descriptions = PROGRAMMES_LEVEL_DESCRIPTIONS
    else:
        # Fallback for unknown paths
        return {
            "scope_summary": f"Level {level} role in the {role_path.title()} career path.",
            "description": f"This role represents Level {level} in the {role_path.title()} career path."
        }
    
    # Return the description if it exists, otherwise provide a fallback
    if level in descriptions:
        return descriptions[level]
    
    # Fallback for levels not defined in the path-specific descriptions
    return {
        "scope_summary": f"Level {level} role in the {role_path.title()} career path.",
        "description": f"This role represents Level {level} in the {role_path.title()} career path."
    }


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

        # Skip skills that don't have a description at this level
        if not level_desc:
            print(f"Info: Skill {skill_code} ({skill.name}) not applicable at level {level}, skipping", file=sys.stderr)
            continue

        content += f"### {skill.name} ({skill_code})\n\n"

        if skill.url:
            content += f"**SFIA Reference:** [{skill_code}]({skill.url})\n\n"

        content += f"**Category:** {skill.category} | **Subcategory:** {skill.subcategory}\n\n"

        content += f"**Overall Description:**\n\n"
        content += f"{skill.overall_description}\n\n"

        if skill.guidance_notes:
            content += f"**Guidance Notes:**\n\n"
            content += f"{skill.guidance_notes}\n\n"

        content += f"**Level {level} Attainment:**\n\n"
        content += f"{level_desc}\n\n"

        content += "---\n\n"

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
        role_skills_def = ROLE_SKILLS[engineer_type]

        for level in range(1, 8):
            # Handle level-specific skills for software engineers
            if isinstance(role_skills_def, dict):
                role_skills = role_skills_def["base"].copy()
                if level >= 6:
                    role_skills.extend(role_skills_def["senior"])
                if level >= 7:
                    role_skills.extend(role_skills_def["strategic"])
            else:
                role_skills = role_skills_def

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
    role_skills_def = ROLE_SKILLS["people-management"]
    role_skills = role_skills_def if isinstance(role_skills_def, list) else role_skills_def["base"]
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
    role_skills_def = ROLE_SKILLS["product-management"]
    role_skills = role_skills_def if isinstance(role_skills_def, list) else role_skills_def["base"]
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
