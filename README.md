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

`QuerySelect_cf` is **additive** — the first call replaces the default `SELECT *`, and each subsequent call appends more columns to the list. Raw SQL expressions (aggregates, `CASE` expressions, etc.) pass through unchanged since no `::` is present, so no separate "raw" variant is needed.

```ecmascript 6
_query = QuerySelect_cf ( _query ; GetFieldName ( FMORM::PrimaryKey ) ) ;
_query = QuerySelect_cf ( _query ; "COUNT(*) AS total" )
// → SELECT "FMORM"."PrimaryKey", COUNT(*) AS total
```

#### WHERE Clauses

All major WHERE variants are supported. Functions are additive and may be chained freely:

```ecmascript 6
_query = QueryWhere_cf          ( _query ; CONTACT::status ; "=" ; "Active" )
_query = QueryOrWhere_cf        ( _query ; CONTACT::status ; "=" ; "Prospect" )
_query = QueryWhereIn_cf        ( _query ; CONTACT::type ; "customer¶partner" )
_query = QueryWhereNotIn_cf     ( _query ; CONTACT::status ; "Archived¶Deleted" )
_query = QueryWhereBetween_cf   ( _query ; INVOICE::amount ; 100 ; 500 )
_query = QueryWhereNull_cf      ( _query ; CONTACT::deletedAt )
_query = QueryWhereNotNull_cf   ( _query ; CONTACT::emailWork )
_query = QueryWhereColumn_cf    ( _query ; INVOICE::contactId ; "=" ; CONTACT::id )
_query = QueryWhereRaw_cf       ( _query ; "MONTH(\"INVOICE\".\"date\") = 3" ; "" )
```

**Grouped conditions** (parenthesised AND/OR blocks) use `QueryWhereGroup_cf`:

```ecmascript 6
// Build the inner group: (status = ? OR priority = ?)
_g = QueryNew_cf     ( "CONTACT" ) ;
_g = QueryWhere_cf   ( _g ; CONTACT::status ; "=" ; "Active" ) ;
_g = QueryOrWhere_cf ( _g ; CONTACT::priority ; "=" ; "High" ) ;

// Attach as AND (…) to the main query
_query = QueryWhere_cf      ( _query ; CONTACT::region ; "=" ; "West" ) ;
_query = QueryWhereGroup_cf ( _query ; _g )
// → WHERE "CONTACT"."region" = ? AND ("CONTACT"."status" = ? OR "CONTACT"."priority" = ?)
```

#### Subqueries

Multiple subquery patterns are supported. All accept a fully-assembled fmorm query object and handle binding merging automatically. Requires FileMaker 17+.

- **[QueryWhereInSubquery_cf](docs/functions.md#querywhereinsubquery_cf)** — `WHERE column IN (SELECT …)`
- **[QueryWhereNotInSubquery_cf](docs/functions.md#querywherenotinsubquery_cf)** — `WHERE column NOT IN (SELECT …)`
- **[QueryWhereExists_cf](docs/functions.md#querywhereexists_cf)** — `WHERE EXISTS (SELECT …)`
- **[QueryWhereNotExists_cf](docs/functions.md#querywherenotexists_cf)** — `WHERE NOT EXISTS (SELECT …)`
- **[QuerySelectSub_cf](docs/functions.md#queryselectsub_cf)** — `(SELECT …) AS alias` in the SELECT list
- **[QueryJoinSub_cf](docs/functions.md#queryjoinsub_cf)** / **[QueryLeftJoinSub_cf](docs/functions.md#queryleftjoinsub_cf)** — `JOIN (SELECT …) AS alias ON …`
- **[QueryFromSubquery_cf](docs/functions.md#queryfromsubquery_cf)** — `FROM (SELECT …) alias` (derived table, FM 19.x+)

```ecmascript 6
// Subquery: IDs of active contacts
_inner = QueryNew_cf ( "CONTACT" ) ;
_inner = QuerySelect_cf ( _inner ; "CONTACT.id" ) ;
_inner = QueryWhere_cf  ( _inner ; CONTACT::status ; "=" ; "Active" ) ;

// Outer query: invoices for those contacts
_query = QueryNew_cf ( "INVOICE" ) ;
_query = QueryWhereInSubquery_cf ( _query ; INVOICE::contactID ; _inner )
// → WHERE "INVOICE"."contactID" IN (SELECT CONTACT.id FROM "CONTACT" WHERE …)
```

#### Aggregate Execution

`QueryCount_cf`, `QuerySum_cf`, `QueryAvg_cf`, `QueryMax_cf`, and `QueryMin_cf` execute directly and return a scalar value without modifying the query object:

```ecmascript 6
_query = QueryNew_cf   ( "INVOICE" ) ;
_query = QueryWhere_cf ( _query ; INVOICE::status ; "=" ; "Paid" ) ;

_count = QueryCount_cf ( _query )            // → 42
_total = QuerySum_cf   ( _query ; INVOICE::amount )   // → 18500
_avg   = QueryAvg_cf   ( _query ; INVOICE::amount )   // → 440.47
```

#### Conditional Building

`QueryWhen_cf` applies a modification only when a condition is true:

```ecmascript 6
_query = QueryWhen_cf (
    _query ;
    not IsEmpty ( $$filterStatus ) ;
    QueryWhere_cf ( _query ; CONTACT::status ; "=" ; $$filterStatus )
)
```

> ## *
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
