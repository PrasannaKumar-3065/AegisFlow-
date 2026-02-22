import json
import os

BASE_DIR = os.getcwd()

# Configuration
INPUT_PATH   = os.path.join(BASE_DIR, "..", "datasets", "L2_dataset_v2.jsonl")
input_file = os.path.join(BASE_DIR, "datasets", "L3", "L3_dataser_v1.jsonl")
output_file = os.path.join(BASE_DIR, "datasets", "L3", "L3_dataser_v1_f.jsonl")
split_marker = "L1 INTENT:"

print(f"🔄 processing {input_file}...")

valid_count = 0
skipped_count = 0

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:
    
    for line_num, line in enumerate(infile):
        try:
            data = json.loads(line)
            raw_prompt = data.get('prompt', '')
            completion = data.get('completion', '')
            
            # Split the prompt into System Instruction and User Input
            if split_marker in raw_prompt:
                parts = raw_prompt.split(split_marker, 1)
                system_instruction = parts[0].strip()
                user_input = split_marker + parts[1] # Keep the marker in user input for context
            else:
                # Fallback if marker is missing (though validation showed 100% have it)
                system_instruction = "You are L3, the Content Planner. Enrich the L2 structure with semantic blueprints."
                user_input = raw_prompt
            
            # Construct the Chat Format
            chat_row = {
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": completion}
                ]
            }
            
            outfile.write(json.dumps(chat_row) + "\n")
            valid_count += 1
            
        except json.JSONDecodeError:
            print(f"⚠️ Skipping line {line_num+1}: Invalid JSON")
            skipped_count += 1

print(f"✅ Conversion Complete!")
print(f"   - Input Lines: {line_num + 1}")
print(f"   - Valid Output: {valid_count}")
print(f"   - Saved to: {output_file}")