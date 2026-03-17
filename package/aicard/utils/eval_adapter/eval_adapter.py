from pathlib import Path
from jinja2 import Template
def eval_adapter(data:dict)->str:
    """Converts input from aicard-eval pacage to html for model card

    Args:
        data (dict): The output of the aicard-eval run as dict

    Returns:
        str: A standardized html formated string
    """
    BASE_DIR = Path(__file__).parent
    template_path = BASE_DIR / "template.html"
    with open(template_path) as f:
        template_str = f.read()
    template = Template(template_str)
    html_out = template.render(**data).replace('\n', '')
    
    return html_out