import os

static_path = os.path.join(".", "src", "static")
template_from = os.path.join(static_path, "template", "basetemp.html")

op_first_section = "\n---\n"
op_second_section = "\n----\n"
op_index_fragment = "\n<!-- -->\n"
op_animate_pattern = "\n<--[.?]-->\n"