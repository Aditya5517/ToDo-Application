def is_empty (value):
  """
  This function takes the input and validates if the input value is empty or not.It returns Boolean value True or False. 
  argument:
  """
  if not value :
    return True
  elif not value.strip():
    return True 
  else:
    return False
  
def is_integer(value):
  """This function takes the value and validates if the input value is a Integer or not it return Boolean value.
  """
  return value.isdigit()
      
def is_string(value):
  """This funtion takes input in the parameter and validates that the value is String or not it returns Boolean value.
  """
  return type(value)==str
