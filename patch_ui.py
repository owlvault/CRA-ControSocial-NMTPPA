import os
import glob

# Files to patch
target_files = glob.glob("pages/*.py") + ["Home.py"]

for filepath in target_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Don't patch twice
    if "import menu" in content or "menu.render_menu()" in content:
        continue
        
    lines = content.split('\n')
    
    # Inject right after st.set_page_config
    injected = False
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if "st.set_page_config" in line and not injected:
            new_lines.append("import menu")
            new_lines.append("menu.render_menu()")
            injected = True
            
    # If no set_page_config found (unlikely), inject after imports
    if not injected:
        for i, line in enumerate(new_lines):
            if line.startswith("import streamlit"):
                new_lines.insert(i+1, "import menu\nmenu.render_menu()")
                break
                
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
print("Paths patched successfully.")
