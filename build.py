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

def process_files():
   logging.info('Starting file processing')
   
   Path('build').mkdir(exist_ok=True)
   logging.info('Created build directory')
   
   latest_ini = find_latest_ini()
   with open(latest_ini, 'r', encoding='utf-8') as f:
       content = f.read()
   logging.info(f'Read content from {latest_ini}')

   smartbox = Path('Smartbox')
   rm_files = list(smartbox.glob('*.rm.ini'))
   logging.info(f'Found {len(rm_files)} removal files')
   
   for rm_file in rm_files:
       with open(rm_file, 'r', encoding='utf-8') as f:
           rm_content = f.read()
           if rm_content in content:
               commented_content = '\n'.join(f'# {line}' for line in rm_content.splitlines())
               header = f'\n{"#" * 80}\n# REMOVED SECTION FROM {rm_file.name}\n{"#" * 80}\n'
               footer = f'\n{"#" * 80}\n# END REMOVED SECTION FROM {rm_file.name}\n{"#" * 80}\n'
               replacement = header + commented_content + footer
               content = content.replace(rm_content, replacement)
               logging.info(f'Commented out content from {rm_file}')

   add_files = list(smartbox.glob('*.add.ini'))
   logging.info(f'Found {len(add_files)} addition files')
   
   for add_file in add_files:
       with open(add_file, 'r', encoding='utf-8') as f:
           add_content = f.read()
           header = f'\n\n\n\n\n{"#" * 80}\n# {add_file.name}\n{"#" * 80}\n'
           content += header + add_content + '\n\n\n\n\n'
           logging.info(f'Added content from {add_file}')

   with open('build/PrusaResearch.ini', 'w', encoding='utf-8') as f:
       f.write(content)
   logging.info('Wrote final output to build/PrusaResearch.ini')

if __name__ == '__main__':
   process_files()