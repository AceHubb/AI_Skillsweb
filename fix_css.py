
import os

file_path = r'c:\PythonApplications\AI_Skillsweb\css\style.css'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Indicies are 0-based.
# Line 53 in 1-based is index 52. 
# Line 90 in 1-based is index 89.
# We want to keep 0-51 (first 52 lines).
# We want to skip 52-89 (lines 53-90).
# We want to keep 90-end.

new_lines = lines[:52] + lines[90:]

# Append custom utilities
custom_css = """
/* Custom Utilities injected by Antigravity */
@layer utilities {
  .glass-panel {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
  }
  
  .dark .glass-panel {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .mesh-bg {
    background-color: #f8fafc;
    background-image: 
        radial-gradient(at 0% 0%, rgba(14, 165, 233, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(14, 165, 233, 0.1) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(99, 102, 241, 0.1) 0px, transparent 50%);
    background-attachment: fixed;
  }

  .text-gradient {
    background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .text-gradient-accent {
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
}
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
    f.write(custom_css)

print("style.css patched successfully.")
