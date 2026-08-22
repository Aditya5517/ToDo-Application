def extra_spaces(value):
  """
  This function takes the input parameter as string and only removes the extra spaces and returns it
 Argument : String
    """
  result= " ".join(value.split())
  return result

def remove(value):
  """
  This function takes the input string and remove all the spaces in the string.
   Argument : String
  """
  answer  = value.replace(" ","")
  return answer