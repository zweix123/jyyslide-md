import os

static_path = os.path.join(".", "src", "static")
backup_path = os.path.join(".", "src", "backup")
template_from = os.path.join(backup_path, "template", "basetemp.html")
authortemp_from = os.path.join(backup_path, "template", "authortemp.html")

op_first_section = "\n---\n"
op_second_section = "\n----\n"
op_index_fragment = "\n<!-- -->\n"
op_animate_pattern = r"\n<--\[.?\]-->\n"
