# FMORM

A fluent, Eloquent-inspired SQL query builder for FileMaker Pro, implemented entirely as Custom Functions on top of `ExecuteSQL`.

---


## Quick Start

FMORM helps solve the pain point of writing clean SQL for FileMaker. 
Its functions guide you through incrementally building your query, 
resulting in much more readable code. 
It enforces `?` variable bindings also, which is a good security practice.

> #### * Prerequisite Note
> Since we'll be iteratively building our query, this documentation will make heavy use of the [Let()](https://help.claris.com/en/pro-help/content/let.html) function (built-in to FileMaker).


### Building A Query

All query-related functions from FRMORM will have names prefixed with `Query`.
They'll all take a `query` parameter too -- which is what lets us build as we go.

#### Initialization
You'll always start with a [QueryNew](docs/functions.md#QueryNew_cf) call. 

```ecmascript 6
Let
(
[
_query = QueryNew_cf ( FMORM::__kptID )
];

// ...

)
```

This tells the query builder which table you want to build a query from.
It also serves double-duty by initializing your query object with a `SELECT *`.
That means if you wanted to, you could run your query already!

#### Expanding The Query
You'll most likely want to add your own `SELECT` statement into your query too -- so that you're not doing a `SELECT *`.
This is accomplished by chaining [QuerySelect](docs/functions.md#QuerySelect_cf) into your query.

Providing it with a list of fieldnames like so is recommended:

```ecmascript 6
Let
(
[
_query = QueryNew_cf ( FMORM::__kptID ) ;
_query = QuerySelect_cf ( _query ; List 
    (
    GetFieldName ( FMORM::PrimaryKey ) ; 
    GetFieldName ( FMORM::CreationTimestamp ) 
    ) 
) 
];
// ...
)
```


> ## *
> 
> There is a lot of SQL functionality available by making use of the functions.  Most of them are pretty sensibly named too.
> 
> See [docs/functions.md](docs/functions.md) for the full function reference with parameter details and examples.

#### Common Parameter Patterns
Many of the system's parameters are actually references to fields, or tables.
Field references can be passed directly to those (no `GetFieldName()` wrapper required). 

The exception being where multiple columns are required (See [QuerySelect_cf](docs/functions.md#QuerySelect_cf) *already covered above*).

Following these principles will lead to concise code and will even survive field renaming

Example using QueryWhere without needing to specify GetFieldName around the column name.
```ecmascript 6
Let
(
[
_query = QueryNew_cf ( FMORM::__kptID ) ;
_query = QuerySelect_cf ( _query ; List 
    ( 
    GetFieldName ( FMORM::PrimaryKey ) ; 
    GetFieldName ( FMORM::CreationTimestamp ) 
    ) 
) ;
_query = QueryWhere_cf ( _query ; FMORM::CreationTimestamp ; "<" ; Get ( CurrentTimestamp ) )
];
QueryToSQL_cf ( _query )
)
```

### Debugging
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


### Executing The Query

When you're done building your query, the functions with names prefixed `QueryGet` will:
1) assemble your query
2) handle `?` variable binding
3) execute the query

#### QueryGet_cf
`QueryGet_cf` will execute your SQL similarly to how an actual ExecuteSQL call would perform -- allowing you to specify delimiters.

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
> Developer Note: In case you want a specific value from your JSON results using a function that maintains proper field references, 
> a utility function [JSONGetElementLikeField_cf](docs/functions.md#JSONGetElementLikeField_cf) has also been provided.

---


### Under-The-Hood

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


## Function Reference

See [docs/functions.md](docs/functions.md) for the full function reference with parameter details and examples.
