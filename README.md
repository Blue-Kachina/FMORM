# FMORM

A fluent, Eloquent-inspired SQL query builder for FileMaker Pro, implemented entirely as Custom Functions on top of `ExecuteSQL`.

---



## Quick start

FMORM helps solve the pain point of writing SQL for FileMaker. You incrementally build up your query using chained custom function calls, resulting in much more readable code. It also automatically enforces `?` substitution, which is a good security practice.

### Building a query
All query-related functions from FRMORM will begin with `Query`.
They'll all take a `query` parameter too -- which is what let's us build as we go.
You'll always start with a `QueryNew` call which tells the query builder which table you want to build a query from.

Many of the system's parameters are references to fields, or tables.
For those ones, field references can be passed directly to most functions — no `GetFieldName()` wrapper required. 
The exception being `QuerySelect_cf`, where the `columns` parameter requires `GetFieldName()` (for a single field) 
or 
`List()` + `GetFieldName()` (for multiple fields). 
Passing field references directly is concise and will even survive field renaming

```
Let
(
[
// Direct field references — concise, no wrapper needed
_query = QueryNew_cf ( FMORM::__kptID ) ;
_query = QuerySelect_cf ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere_cf ( _query ; FMORM::CreationTimestamp ; "<" ; Get ( CurrentTimestamp ) )
];
QueryToSQL_cf ( _query )
)
```

Use `QueryToSQL_cf` at any point to inspect the SQL that would be produced without executing it (very useful during development/debugging). 

```
SELECT
    "FMORM"."PrimaryKey",
    "FMORM"."CreationTimestamp"
FROM
    "FMORM"
WHERE
    "FMORM"."CreationTimestamp" < ?
```


### Executing the query

When you're done building your query, the `QueryGet` series of functions will return your results for you. 

#### QueryGet_cf
`QueryGet_cf` will execute your SQL similarly to how an actual ExecuteSQL call would perform -- allowing you to specify delimiters. 
It will handle the `?` replacements for you.

```
Let
(
[
_query = QueryNew_cf ( GetFieldName ( FMORM::__kptID ) ) ;
_query = QuerySelect_cf ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere_cf ( _query ; GetFieldName ( FMORM::CreationTimestamp ) ; "<" ; Get ( CurrentTimestamp ) )
];
QueryGet_cf ( _query ; "," ; "¶" )
)
```

```
C6131AAC-F09C-DD44-975D-5E33494E6176,2026-03-09 09:56:34
```

#### QueryGetResultsAsJson_cf
Alternatively if you'd rather get JSON results, use `QueryGetResultsAsJson_cf` instead.
It will return a JSON array of objects with properties named like their corresponding fields

```
Let
(
[
_query = QueryNew_cf ( GetFieldName ( FMORM::__kptID ) ) ;
_query = QuerySelect_cf ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere_cf ( _query ; GetFieldName ( FMORM::CreationTimestamp ) ; "<" ; Get ( CurrentTimestamp ) )
];
QueryGetResultsAsJson_cf ( _query )
)
```

```json
[
    { "PrimaryKey": "C6131AAC-F09C-DD44-975D-5E33494E6176", "CreationTimestamp": "2026-03-09 09:56:34" }
]
```

> ## *
> Developer Note: A utility function [JSONGetElementLikeField_cf](docs/functions.md#JSONGetElementLikeField_cf) has also been provided.  
> It can help you get the value out of JSON results while still staying reference-safe

---


### Under the hood

Under-the-hood a complex JSON object is being maintained in order to keep a definition of what your query is.
Every one of the `Query` functions alters that JSON object in a meaningful way.
When one of the `QueryGet` functions is invoked, the actual query gets assembled based on how you've defined it.

You can take a look at the JSON at any time, but keep in mind that it's not intended for manual editing

```
Let
(
[
_query = QueryNew_cf ( GetFieldName ( FMORM::__kptID ) ) ;
_query = QuerySelect_cf ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere_cf ( _query ; GetFieldName ( FMORM::CreationTimestamp ) ; "<" ; Get ( CurrentTimestamp ) )
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
    "selectKeys" : "PrimaryKey\rCreationTimestamp",
    "selects" : "\"FMORM\".\"PrimaryKey\", \"FMORM\".\"CreationTimestamp\"",
    "table" : "\"FMORM\"",
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

---


## Function reference

See [docs/functions.md](docs/functions.md) for the full function reference with parameter details and examples.
