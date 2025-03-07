import os
import re
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_version(filename):
    match = re.match(r'(\d+)\.(\d+)\.(\d+)', os.path.basename(filename))
    if match:
        return tuple(map(int, match.groups()))
    return (0, 0, 0)

def find_latest_ini():
    prusa_dir = Path('PrusaResearch')
    ini_files = [f for f in prusa_dir.glob('*.ini') if re.match(r'\d+\.\d+\.\d+\.ini$', f.name)]
    latest = max(ini_files, key=lambda x: parse_version(x))
    logging.info(f'Found latest ini file: {latest}')
    return latest

def strip_comments(text):
    # Strip comments while preserving empty lines and color-related comments
    lines = []
    for line in text.splitlines():
        if 'colour' in line.lower():
            # Preserve lines containing 'color' as is
            lines.append(line.rstrip())
            continue
            
        # Find position of first # that isn't escaped
        comment_pos = -1
        i = 0
        while i < len(line):
            if line[i] == '#' and (i == 0 or line[i-1] != '\\'):
                comment_pos = i
                break
            i += 1
            
        if comment_pos != -1:
            # Take only the part before the comment and strip whitespace
            stripped_line = line[:comment_pos].rstrip()
            lines.append(stripped_line)
        else:
            # No comment found, preserve the line as is
            lines.append(line.rstrip())
            
    return '\n'.join(lines)

def process_files():
    logging.info('Starting file processing')
    Path('build').mkdir(exist_ok=True)
    logging.info('Created build directory')
    
    latest_ini = find_latest_ini()
    with open(latest_ini, 'r', encoding='utf-8') as f:
        content = f.read()
    logging.info(f'Read content from {latest_ini}')
    
    # First strip comments from the base content
    content = strip_comments(content)
    
    smartbox = Path('Smartbox')
    rm_files = list(smartbox.glob('*.rm.ini'))
    logging.info(f'Found {len(rm_files)} removal files')
    
    for rm_file in rm_files:
        with open(rm_file, 'r', encoding='utf-8') as f:
            rm_content = f.read()
        # Strip comments from removal content before comparison
        rm_content_stripped = strip_comments(rm_content)
        if rm_content_stripped in content:
            content = content.replace(rm_content_stripped, '')
            logging.info(f'Removed content from {rm_file}')
    
    # Find the position of [printer:*common*]
    obsolete_pos = content.find('[printer:*common*]')
    if obsolete_pos == -1:
        obsolete_pos = len(content)  # If section not found, append at end
        
    # Process addition files
    add_files = list(smartbox.glob('*.add.ini'))
    logging.info(f'Found {len(add_files)} addition files')
    
    additional_content = []
    for add_file in add_files:
        with open(add_file, 'r', encoding='utf-8') as f:
            add_content = f.read()
        # Strip comments from additional content before adding
        add_content_stripped = strip_comments(add_content)
        if add_content_stripped.strip():  # Only add if there's non-empty content
            additional_content.append(add_content_stripped)
            logging.info(f'Added content from {add_file}')
    
    # Combine all additional content with proper spacing
    if additional_content:
        combined_additions = '\n\n\n\n\n'.join(additional_content) + '\n\n\n\n\n'
        # Insert before [obsolete_presets]
        content = content[:obsolete_pos] + combined_additions + content[obsolete_pos:]
    
    # Write the final content
    with open('build/PrusaResearch.ini', 'w', encoding='utf-8') as f:
        f.write(content)
    logging.info('Wrote final output to build/PrusaResearch.ini')

if __name__ == '__main__':
    process_files()