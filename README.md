# FMORM

A fluent, Eloquent-inspired SQL query builder for FileMaker Pro, implemented entirely as Custom Functions on top of `ExecuteSQL`.

---



## Quick start

FMORM helps solve the pain point of writing SQL for FileMaker. You incrementally build up your query using chained custom function calls, resulting in much more readable code. It also automatically enforces `?` substitution, which is good security practice.

### Building a query

```
Let
(
[
_query = QueryNew_cf ( "FMORM" ) ;
_query = QuerySelect_cf ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere_cf ( _query ; "FMORM.CreationTimestamp" ; "<" ; Get ( CurrentTimestamp ) )
];
QueryToSQL_cf ( _query )
)
```

Use `QueryToSQL_cf` at any point to inspect the SQL that would be produced without executing it (very useful during development):

```
SELECT "FMORM"."PrimaryKey", "FMORM"."CreationTimestamp" FROM FMORM WHERE FMORM.CreationTimestamp < ?
```

### Under the hood

Each builder function is accumulating state into a JSON object. You can inspect it at any time with `JSONFormatElements`:

```
Let
(
[
_query = QueryNew_cf ( "FMORM" ) ;
_query = QuerySelect_cf ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere_cf ( _query ; "FMORM.CreationTimestamp" ; "<" ; Get ( CurrentTimestamp ) )
];
JSONFormatElements ( _query )
)
```

```json
{
    "bindingCount" : 1,
    "bindings" : [ "2026-03-09 11:21:04 AM" ],
    "groupByCount" : 0,
    "groupBys" : [],
    "havingCount" : 0,
    "havings" : [],
    "joinCount" : 0,
    "joins" : [],
    "limit" : "",
    "offset" : "",
    "orderByCount" : 0,
    "orderBys" : [],
    "selects" : "\"FMORM\".\"PrimaryKey\", \"FMORM\".\"CreationTimestamp\"",
    "table" : "FMORM",
    "whereCount" : 1,
    "wheres" :
    [
        {
            "boolean" : "and",
            "column" : "FMORM.CreationTimestamp",
            "operator" : "<",
            "type" : "basic"
        }
    ]
}
```

### Executing the query

When you're done building, use `QueryGet_cf` to execute it. It handles the `?` substitutions and returns the `ExecuteSQL` result:

```
Let
(
[
_query = QueryNew_cf ( "FMORM" ) ;
_query = QuerySelect_cf ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere_cf ( _query ; "FMORM.CreationTimestamp" ; "<" ; Get ( CurrentTimestamp ) )
];
QueryGet_cf ( _query ; "" ; "¶" )
)
```

```
C6131AAC-F09C-DD44-975D-5E33494E6176,2026-03-09 09:56:34
```

---


## Function reference

See [docs/functions.md](docs/functions.md) for the full function reference with parameter details and examples.
