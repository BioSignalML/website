# BioSignalML Block Stream Format

A message protocol used to transport BioSignalML data blocks over a WebSockets stream.

## Block stream

A *block stream* is a sequence of *blocks*.

## Block

A *block* is a sequence of 8-bit bytes. Each block:

* is of some type, given by a single, alphabetic character;
* has a header, consisting of set of *(name, value)* pairs in JSON format, and with the allowed *names* and
*values* are specific to the block type; 
* has some (possibly empty) content; 
* includes an optional checksum.

The structure of a general block is defined using Extended Backus-Naur Form (EBNF) and
regular expression notation as follows:

```
<block>    ::= '#' <type> <version> <header> <length> <LF>
                   <content> '##' <checksum>? <LF>

<type>     ::= [a-zA-Z]        /* A single, case-significant letter.       */
<version>  ::= <INTEGER> 'V'   /* The version of the protocol.             */

<header>   ::= <jsonlen> <json>
<jsonlen>  ::= <INTEGER>       /* The number of bytes of JSON that follow. */
<json>     ::= '{' ... '}'     /* A well-formed JSON object.               */

<length>   ::= <INTEGER>       /* The length of the content part.          */
<content>  ::= [#x00-#xFF]*    /* A sequence of bytes.                     */

<checksum> ::= [0-9a-fA-F]{40} /* An optional, 40 character SHA1 hex       */
                               /* digest of the block, including opening   */
                               /* '#' and closing '##' characters.         */
<INTEGER>  ::= [0-9]+
<LF>       ::= #x0A
```
<figcaption>Structure of a message block defined using EBNF.</figcaption>


## Block types

A BioSignalML block stream makes use of three block types as specified here.
Details of their header fields are in the following sections.

```
<type>         ::=  <data_request> | <data> | <error>

<data_request> ::= 'd'
<data>         ::= 'D'
<error>        ::= 'E'
```
<figcaption>Block types used by BioSignalML.</figcaption>

### Data request

A request for time-series data for a recording or a list of signals.
Data is returned in *data* blocks. A request block has the following
header fields and no content.

uri
: (string or list of strings) -- The URI of a recording or URI(s) of
signal(s). **REQUIRED**.

<dd>A single URI can be that of a recording or signal; all URIs in a list
must refer to signals. If the URI is that of a recording then data for
all signals in the recording is returned. Several data blocks may be
generated to span the requested duration; when the request is for
multiple signals or for a recording, each signal's data will be in one
or more separate blocks.</dd>

start
: (float) -- The time, in seconds from the start of the signal's
recording. The first sample point returned should not be before this
time.

<dd><strong>REQUIRED</strong> when multiple signals or when no offset is given.</dd>

duration
: (float) -- The duration, in seconds, of time-series data to return. A
value of -1 means to return all sample points from the start time or
offset until time-series' end. 

<dd><strong>REQUIRED</strong> when multiple signals or if no *count* is given.</dd>

offset
: (integer) -- The index in the signal's time-series of the first sample
point in the result.

<dd><strong>REQUIRED</strong> when *start* is not specified; can only be used when requesting
data from a single signal.</dd>

count
: (integer) -- The number of sample points to return in the result. A
value of -1 means to get all samples, from the start position until the
end of the time-series.

<dd><strong>REQUIRED</strong> when *duration* is not specified; can only be used when
requesting data from a single signal.</dd>

maxsize
: (integer) -- The maximum number of sample values to return in a data block. **OPTIONAL**.

<dd>If unspecified, the data source will determine the maximum. If *maxsize*
is given, the data source may elect to impose a smaller value.</dd>

dtype
: (string) -- The required numeric type for data points, in the format
*\<f4* as defined and used by numpy's array interface. **OPTIONAL**.

ctype
: (string) -- The required numeric type for samples, in the form *\<f4*
as defined and used by numpy's array interface. **OPTIONAL**.


The time of the first sample point in the resulting time-series will not
be before *start*; that of the last sample point will be before *start +
duration*. If the signal's data finishes before the requested duration a
shorter time-series will be returned; if the period spanned in a signal
contains discontinuous segments they will be returned as separate
blocks.

### Data block

Contains time-series data for a segment of a signal as an array of
sample values, optionally preceded by an array of sample times. Sample
values are either all scalars or all 1-D arrays, each with the same
bounds.

A data block's header has the following fields:

uri
: (string) -- The URI of the signal whose data is in the block. **REQUIRED**.

start
: (float) -- The time in seconds, from the start of the signal's
recording, of the first sample value. **REQUIRED**.

offset
: (integer) -- The index of the first sample value in the signal's
time-series. **REQUIRED**.

count
: (integer) -- The number of sample values in the data block. **REQUIRED**.

dims
: (integer), default = 1 -- The number of data points in a single sample
value. **OPTIONAL**.

dtype
: (string) -- The numeric type of a single data point in a sample value,
in the form *\<f4* as defined and used by numpy's array interface. **REQUIRED**.

rate
: (double) -- The rate, in Hertz, of sample values.

<dd><strong>REQUIRED</strong> if no *ctype* is given, otherwise MUST NOT be given.</dd>

ctype
: (string) -- The numeric type of a sample time, in the form *\<f4* as
defined and used by numpy's array interface.

<dd><strong>REQUIRED</strong> if no *rate* is given, otherwise MUST NOT be given.</dd>

A data block's content consists of *count* binary numbers of type
*ctype* (when *ctype* is specified), followed by *count\*dims* binary
numbers of type *dtype*.

### Error block

An error response -- the block's content contains an error message as
text; its header will contain the field **type**, with its value the
type character of the request block which caused the error, along with
all header fields from the original request.

## Version

The initial version of the Block Stream Format is ``1`` and is placed in a
block's preamble immediately after the block type.

It is expected that later versions, while possibly introducing new
features, will maintain backwards compatibility with prior versions.
