import yaml
from pathlib import Path
from jsonschema import validate,FormatChecker,ValidationError

schema_str = """
type: object
properties:
  title:    {'type': 'string'}
  excerpt: {'type': 'string'}
  tags: {'type': 'array', 'items': { 'type': 'string' } }
  data:
    type: array
    items:
      type: object
      properties:
        title:  {'type': 'string'}
        author: {'type': 'string'}
        date:   {'type': 'string', 'format': 'date'}
        tags:   {'type': 'array', 'items': {'type': 'string'} }
        details: 
          type: array
          items:
            type: object
            properties:
              text:   {'type': 'string'}
              author: {'type': 'string'}
              date:   {'type': 'string', 'format': 'date'}
              url:    {'type': 'string'}
              backup: {'type': 'string'}
        visuals:
          type: array
          items:
            type: object
            properties:
              alt: {'type': 'string'}
              url: {'type': 'string'}
              backup: {'type': 'string'}
            required: ['url']
      required: ['title']
required: ['data']
"""

if __name__=="__main__":
    schema = yaml.load(schema_str,Loader=yaml.BaseLoader)
    for path_yml in Path("reviews").glob("*/*.yml"):
        with open(str(path_yml),"r") as file_yml:
            yml = yaml.load(file_yml,Loader=yaml.BaseLoader)
        try:
            validate(yml,schema,format_checker=FormatChecker())
        except ValidationError as e:
            raise Exception(f"In {path_yml}:\n{str(e)}")
    
    print("All YAML files under reviews/ have passed basic syntax check.")
