import os
import glob
import re

# Files to patch
target_files = glob.glob("pages/*.py") + ["Home.py"]

for filepath in target_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean previous injection entirely
    content = content.replace("import menu\nmenu.render_menu()", "")
    content = content.replace("import menu\nmenu.render_menu()\n", "")
    content = content.replace("import menu", "")
    content = content.replace("menu.render_menu()", "")
    
    # We want to inject it RIGHT AFTER the closing parenthesis of st.set_page_config
    # st.set_page_config( ... )
    
    # A regex to find the end of st.set_page_config
    if "st.set_page_config" in content:
        # Use regex to find the whole match of st.set_page_config( ... )
        import re
        # Find the text "st.set_page_config("
        idx = content.find("st.set_page_config(")
        if idx != -1:
            # count parens
            paren_count = 0
            end_idx = -1
            for i in range(idx + len("st.set_page_config("), len(content)):
                if content[i] == '(':
                    paren_count += 1
                elif content[i] == ')':
                    if paren_count == 0:
                        end_idx = i
                        break
                    else:
                        paren_count -= 1
            if end_idx != -1:
                # Add it right after the closing parenthesis + newline
                new_content = content[:end_idx+1] + "\nimport menu\nmenu.render_menu()\n" + content[end_idx+1:]
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
