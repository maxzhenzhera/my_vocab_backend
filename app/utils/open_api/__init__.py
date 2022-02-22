"""
headers:
  Set-Cookie:
    description: Session cookie
    schema:
      type: string
      example: SESSIONID=abcde12345; Path=/
  "\0Set-Cookie":
    description: CSRF token
    schema:
      type: string
      example: CSRFTOKEN=fghijk678910; Path=/; HttpOnly
"""
