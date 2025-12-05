import yaml
from pathlib import Path
from jsonschema import validate,FormatChecker,ValidationError

schema_str = """
type: object
properties:
  title:    {'type': 'string', 'minLength': 1}
  excerpt:  {'type': 'string', 'minLength': 1}
  tags:     {'type': 'array', 'items': { 'type': 'string', 'minLength': 1} }
  data:
    type: array
    items:
      type: object
      minItems: 1
      properties:
        title:  {'type': 'string', 'minLength': 1}
        author: {'type': 'string', 'minLength': 1}
        date:   {'type': 'string', 'minLength': 1, 'format': 'date'}
        tags:   {'type': 'array', 'items': {'type': 'string', 'minLength': 1} }
        details: 
          type: array
          items:
            type: object
            minItems: 1
            properties:
              text:   {'type': 'string', 'minLength': 1}
              author: {'type': 'string', 'minLength': 1}
              date:   {'type': 'string', 'minLength': 1, 'format': 'date'}
              url:    {'type': 'string', 'minLength': 1}
              backup: {'type': 'string', 'minLength': 1}
            required: ['text']
        visuals:
          type: array
          minItems: 1
          items:
            type: object
            properties:
              alt:    {'type': 'string', 'minLength': 1}
              url:    {'type': 'string', 'minLength': 1}
              backup: {'type': 'string', 'minLength': 1}
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
