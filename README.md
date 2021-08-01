
# Fusio-Worker-Python

A Fusio worker implementation to execute Python code.
More information about the worker API at:
https://www.fusio-project.org/documentation/worker

## Example

The following example shows an action written in Python which gets data
from a database and returns a response

```python
def handle(request, context, connector, response, dispatcher, logger):

    connection = connector.getConnection('my_db')

    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM app_todo""")
    result = cursor.fetchall()
    cursor.close()

    data = []
    for row in result:
        data.append({
            'id': row[0],
            'status': row[1],
            'title': row[2],
            'insert_date': str(row[3])
        })

    return response.build(200, None, {
        'foo': 'bar',
        'result': data
    })

```