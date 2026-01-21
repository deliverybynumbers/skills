#!/usr/bin/env python3
"""
Parse SFIA CSV file and extract skill definitions by code and level.
"""

import sys
import pandas as pd
from pathlib import Path
from typing import Dict, Optional


class SFIASkill:
    """Represents a SFIA skill with its definitions at different levels."""
    
    def __init__(self, code: str, name: str, url: str, category: str, 
                 subcategory: str, overall_description: str, guidance_notes: str):
        self.code = code
        self.name = name
        self.url = url
        self.category = category
        self.subcategory = subcategory
        self.overall_description = overall_description
        self.guidance_notes = guidance_notes
        self.level_descriptions: Dict[int, str] = {}
    
    def add_level_description(self, level: int, description: str):
        """Add a level-specific description."""
        if description and pd.notna(description) and str(description).strip():
            self.level_descriptions[level] = str(description).strip()
    
    def get_level_description(self, level: int) -> Optional[str]:
        """Get the description for a specific level."""
        return self.level_descriptions.get(level)


def parse_sfia_csv(csv_path: Path) -> Dict[str, SFIASkill]:
    """
    Parse the SFIA CSV file and return a dictionary mapping skill codes to SFIASkill objects.
    
    The CSV format has:
    - Columns 0-7: Level indicators (empty or level number)
    - Column 8: Code
    - Column 9: URL
    - Column 10: Skill name
    - Column 11: Category
    - Column 12: Subcategory
    - Column 13: Overall description
    - Column 14: Guidance notes
    - Columns 15-21: Level 1-7 descriptions
    """
    skills: Dict[str, SFIASkill] = {}
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    df = None
    
    for encoding in encodings:
        try:
            # Read CSV, handling multi-line fields
            df = pd.read_csv(
                csv_path,
                encoding=encoding,
                quotechar='"',
                skipinitialspace=True,
                on_bad_lines='skip'
            )
            break
        except (UnicodeDecodeError, pd.errors.ParserError) as e:
            continue
    
    if df is None:
        raise ValueError(f"Could not parse CSV file with any encoding: {encodings}")
    
    # Get column names
    cols = df.columns.tolist()
    
    # Expected column positions (0-indexed)
    code_col = 8
    url_col = 9
    name_col = 10
    category_col = 11
    subcategory_col = 12
    overall_desc_col = 13
    guidance_col = 14
    level_desc_start = 15  # Level 1 description starts here
    
    # Process each row
    for idx, row in df.iterrows():
        # Skip rows without a code
        if code_col >= len(cols) or pd.isna(row.iloc[code_col]):
            continue
        
        code = str(row.iloc[code_col]).strip()
        if not code:
            continue
        
        # Extract basic info
        name = str(row.iloc[name_col]).strip() if name_col < len(cols) and pd.notna(row.iloc[name_col]) else ""
        url = str(row.iloc[url_col]).strip() if url_col < len(cols) and pd.notna(row.iloc[url_col]) else ""
        category = str(row.iloc[category_col]).strip() if category_col < len(cols) and pd.notna(row.iloc[category_col]) else ""
        subcategory = str(row.iloc[subcategory_col]).strip() if subcategory_col < len(cols) and pd.notna(row.iloc[subcategory_col]) else ""
        overall_description = str(row.iloc[overall_desc_col]).strip() if overall_desc_col < len(cols) and pd.notna(row.iloc[overall_desc_col]) else ""
        guidance_notes = str(row.iloc[guidance_col]).strip() if guidance_col < len(cols) and pd.notna(row.iloc[guidance_col]) else ""
        
        # Create skill object
        skill = SFIASkill(
            code=code,
            name=name,
            url=url,
            category=category,
            subcategory=subcategory,
            overall_description=overall_description,
            guidance_notes=guidance_notes
        )
        
        # Extract level descriptions (columns 15-21 for levels 1-7)
        for level in range(1, 8):
            col_idx = level_desc_start + (level - 1)
            if col_idx < len(cols):
                level_desc = row.iloc[col_idx]
                if pd.notna(level_desc):
                    skill.add_level_description(level, str(level_desc))
        
        skills[code] = skill
    
    return skills


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    csv_path = repo_root / "input" / "sfia-9_current-standard_en_250129(Skills).csv"
    
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Parsing SFIA CSV from {csv_path}...")
    skills = parse_sfia_csv(csv_path)
    
    print(f"Parsed {len(skills)} skills")
    
    # Print some examples
    example_codes = ["SWDN", "PROG", "ARCH", "ETMG", "PROD"]
    print("\nExample skills:")
    for code in example_codes:
        if code in skills:
            skill = skills[code]
            print(f"\n{code} - {skill.name}")
            print(f"  Levels: {sorted(skill.level_descriptions.keys())}")
            desc_preview = skill.overall_description[:100] if skill.overall_description else ""
            print(f"  Description: {desc_preview}...")
    
    return skills


if __name__ == "__main__":
    main()
