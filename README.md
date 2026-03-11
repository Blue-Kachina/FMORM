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
You'll always start with a [QueryNew](docs/functions.md#QueryNew) call. 

```ecmascript 6
Let
(
[
_query = QueryNew ( FMORM::__kptID )
];

// ...

)
```

This tells the query builder which table you want to build a query from.
It also serves double-duty by initializing your query object with a `SELECT *`.
That means if you wanted to, you could run your query already!

#### Expanding The Query
You'll most likely want to add your own `SELECT` statement into your query too -- so that you're not doing a `SELECT *`.
This is accomplished by chaining [QuerySelect](docs/functions.md#QuerySelect) into your query.

Providing it with a list of fieldnames like so is recommended:

```ecmascript 6
Let
(
[
_query = QueryNew ( FMORM::__kptID ) ;
_query = QuerySelect ( _query ; List
    (
    GetFieldName ( FMORM::PrimaryKey ) ;
    GetFieldName ( FMORM::CreationTimestamp )
    )
)
];
// ...
)
```

`QuerySelect` is **additive** — the first call replaces the default `SELECT *`, and each subsequent call appends more columns to the list. Raw SQL expressions (aggregates, `CASE` expressions, etc.) pass through unchanged since no `::` is present, so no separate "raw" variant is needed.

```ecmascript 6
_query = QuerySelect ( _query ; GetFieldName ( FMORM::PrimaryKey ) ) ;
_query = QuerySelect ( _query ; "COUNT(*) AS total" )
// → SELECT "FMORM"."PrimaryKey", COUNT(*) AS total
```

#### WHERE Clauses

All major WHERE variants are supported. Functions are additive and may be chained freely:

```ecmascript 6
_query = QueryWhere          ( _query ; CONTACT::status ; "=" ; "Active" )
_query = QueryOrWhere        ( _query ; CONTACT::status ; "=" ; "Prospect" )
_query = QueryWhereIn        ( _query ; CONTACT::type ; "customer¶partner" )
_query = QueryWhereNotIn     ( _query ; CONTACT::status ; "Archived¶Deleted" )
_query = QueryWhereBetween   ( _query ; INVOICE::amount ; 100 ; 500 )
_query = QueryWhereNull      ( _query ; CONTACT::deletedAt )
_query = QueryWhereNotNull   ( _query ; CONTACT::emailWork )
_query = QueryWhereColumn    ( _query ; INVOICE::contactId ; "=" ; CONTACT::id )
_query = QueryWhereRaw       ( _query ; "MONTH(\"INVOICE\".\"date\") = 3" ; "" )
```

**Grouped conditions** (parenthesised AND/OR blocks) use `QueryWhereGroup`:

```ecmascript 6
// Build the inner group: (status = ? OR priority = ?)
_g = QueryNew     ( "CONTACT" ) ;
_g = QueryWhere   ( _g ; CONTACT::status ; "=" ; "Active" ) ;
_g = QueryOrWhere ( _g ; CONTACT::priority ; "=" ; "High" ) ;

// Attach as AND (…) to the main query
_query = QueryWhere      ( _query ; CONTACT::region ; "=" ; "West" ) ;
_query = QueryWhereGroup ( _query ; _g )
// → WHERE "CONTACT"."region" = ? AND ("CONTACT"."status" = ? OR "CONTACT"."priority" = ?)
```

#### Subqueries

Multiple subquery patterns are supported. All accept a fully-assembled fmorm query object and handle binding merging automatically. Requires FileMaker 17+.

- **[QueryWhereInSubquery](docs/functions.md#querywhereinsubquery)** — `WHERE column IN (SELECT …)`
- **[QueryWhereNotInSubquery](docs/functions.md#querywherenotinsubquery)** — `WHERE column NOT IN (SELECT …)`
- **[QueryWhereExists](docs/functions.md#querywhereexists)** — `WHERE EXISTS (SELECT …)`
- **[QueryWhereNotExists](docs/functions.md#querywherenotexists)** — `WHERE NOT EXISTS (SELECT …)`
- **[QuerySelectSub](docs/functions.md#queryselectsub)** — `(SELECT …) AS alias` in the SELECT list
- **[QueryJoinSub](docs/functions.md#queryjoinsub)** / **[QueryLeftJoinSub](docs/functions.md#queryleftjoinsub)** — `JOIN (SELECT …) AS alias ON …`
- **[QueryFromSubquery](docs/functions.md#queryfromsubquery)** — `FROM (SELECT …) alias` (derived table, FM 19.x+)

```ecmascript 6
// Subquery: IDs of active contacts
_inner = QueryNew ( "CONTACT" ) ;
_inner = QuerySelect ( _inner ; "CONTACT.id" ) ;
_inner = QueryWhere  ( _inner ; CONTACT::status ; "=" ; "Active" ) ;

// Outer query: invoices for those contacts
_query = QueryNew ( "INVOICE" ) ;
_query = QueryWhereInSubquery ( _query ; INVOICE::contactID ; _inner )
// → WHERE "INVOICE"."contactID" IN (SELECT CONTACT.id FROM "CONTACT" WHERE …)
```

#### Aggregate Execution

`QueryCount`, `QuerySum`, `QueryAvg`, `QueryMax`, and `QueryMin` execute directly and return a scalar value without modifying the query object:

```ecmascript 6
_query = QueryNew   ( "INVOICE" ) ;
_query = QueryWhere ( _query ; INVOICE::status ; "=" ; "Paid" ) ;

_count = QueryCount ( _query )            // → 42
_total = QuerySum   ( _query ; INVOICE::amount )   // → 18500
_avg   = QueryAvg   ( _query ; INVOICE::amount )   // → 440.47
```

#### Conditional Building

`QueryWhen` applies a modification only when a condition is true:

```ecmascript 6
_query = QueryWhen (
    _query ;
    not IsEmpty ( $$filterStatus ) ;
    QueryWhere ( _query ; CONTACT::status ; "=" ; $$filterStatus )
)
```

> ## *
>
> See [docs/functions.md](docs/functions.md) for the full function reference with parameter details and examples.

#### Common Parameter Patterns
Many of the system's parameters are actually references to fields, or tables.
Field references can be passed directly to those (no `GetFieldName()` wrapper required). 

The exception being where multiple columns are required (See [QuerySelect](docs/functions.md#QuerySelect) *already covered above*).

Following these principles will lead to concise code and will even survive field renaming

Example using QueryWhere without needing to specify GetFieldName around the column name.
```ecmascript 6
Let
(
[
_query = QueryNew ( FMORM::__kptID ) ;
_query = QuerySelect ( _query ; List 
    ( 
    GetFieldName ( FMORM::PrimaryKey ) ; 
    GetFieldName ( FMORM::CreationTimestamp ) 
    ) 
) ;
_query = QueryWhere ( _query ; FMORM::CreationTimestamp ; "<" ; Get ( CurrentTimestamp ) )
];
QueryToSQL ( _query )
)
```

### Debugging
Use `QueryToSQL` at any point to inspect the SQL that would be produced without executing it (very useful during development/debugging). 

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

#### QueryGet
`QueryGet` will execute your SQL similarly to how an actual ExecuteSQL call would perform -- allowing you to specify delimiters.

```
Let
(
[
_query = QueryNew ( GetFieldName ( FMORM::__kptID ) ) ;
_query = QuerySelect ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere ( _query ; GetFieldName ( FMORM::CreationTimestamp ) ; "<" ; Get ( CurrentTimestamp ) )
];
QueryGet ( _query ; "," ; "¶" )
)
```

```
C6131AAC-F09C-DD44-975D-5E33494E6176,2026-03-09 09:56:34
```

#### QueryGetResultsAsJson
Alternatively if you'd rather get JSON results, use `QueryGetResultsAsJson` instead.
It will return a JSON array of objects with properties named like their corresponding fields

```
Let
(
[
_query = QueryNew ( GetFieldName ( FMORM::__kptID ) ) ;
_query = QuerySelect ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere ( _query ; GetFieldName ( FMORM::CreationTimestamp ) ; "<" ; Get ( CurrentTimestamp ) )
];
QueryGetResultsAsJson ( _query )
)
```

```json
[
    { "PrimaryKey": "C6131AAC-F09C-DD44-975D-5E33494E6176", "CreationTimestamp": "2026-03-09 09:56:34" }
]
```

> ## *
> Developer Note: In case you want a specific value from your JSON results using a function that maintains proper field references, 
> a utility function [JSONGetElementNamedLikeField](docs/functions.md#JSONGetElementNamedLikeField) has also been provided.

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
_query = QueryNew ( GetFieldName ( FMORM::__kptID ) ) ;
_query = QuerySelect ( _query ; List ( GetFieldName ( FMORM::PrimaryKey ) ; GetFieldName ( FMORM::CreationTimestamp ) ) ) ;
_query = QueryWhere ( _query ; GetFieldName ( FMORM::CreationTimestamp ) ; "<" ; Get ( CurrentTimestamp ) )
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
