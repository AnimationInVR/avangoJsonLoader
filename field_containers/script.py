import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

def create_new_script(json, app):
  module = json['module']
  classname = json['name']

  exec("from tmp." + module + " import " + classname)
  new_script = eval(classname + "()", globals(), locals())
  new_script.Name.value = classname

  app.add_field_container(new_script)

  for connection in json["field_connections"]:
    app.plan_field_connection(new_script.Name.value, connection["from_field"], connection["to_node"], connection["to_field"])

  for field_name in json["values"]:
    field = new_script.get_field(field_name)
    field.value = json["values"][field_name]