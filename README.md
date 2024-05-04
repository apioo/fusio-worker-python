
# Fusio-Worker-Python

A Fusio worker implementation to execute Python code.
More information about the Worker system at our documentation:
https://docs.fusio-project.org/docs/use_cases/api_gateway/worker

## Example

The following example shows an action written in Python which gets data
from a database and returns a response

```python
def handle(request, context, connector, response, dispatcher, logger):
    connection = connector.get_connection('app')

    cursor = connection.cursor()
    cursor.execute("""SELECT name, description FROM app_product_0""")
    result = cursor.fetchall()
    cursor.close()

    entries = []
    for row in result:
        entries.append({
            'name': row[0],
            'description': row[1],
        })

    return response.build(200, None, {
        'foo': 'bar',
        'entries': entries
    })

```

## Types

This table contains an overview which connection types are implemented
and which implementation is used:

| Type                                                   | Implementation      |
|--------------------------------------------------------|---------------------|
| `Fusio.Adapter.Sql.Connection.Sql`                     | `PyMySQL / pymongo` |
| `Fusio.Adapter.Sql.Connection.SqlAdvanced`             | `PyMySQL / pymongo` |
| `Fusio.Adapter.Http.Connection.Http`                   | `http.client`       |
| `Fusio.Adapter.Mongodb.Connection.MongoDB`             | `pymongo`           |
| `Fusio.Adapter.Elasticsearch.Connection.Elasticsearch` | `elasticsearch`     |

