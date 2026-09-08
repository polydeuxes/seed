# Movement source and destination coordinate report 001

## Problem

Active Movement law ended with a negative list:

```text
source and destination coordinates
have no earlier or later occurrence order
```

That wording said what the coordinates were not while leaving their positive
relation role implicit.

## Positive coordinate

Movement already preserves one exact source-to-destination relation. Its
ordered coordinates are now explicit:

```text
first coordinates     exact source coordinates
second coordinates    exact destination coordinates
```

Witness grammar projects the same ordered pair under
`source_to_destination_coordinates`.

## Distinction

`first` and `second` are qualified by the relation-coordinate domain. They do
not borrow the earlier/later occurrence-order domain.

```text
first relation coordinates     source
second relation coordinates    destination
earlier occurrence             not inferred
later occurrence               not inferred
```

The positive ordered endpoints are sufficient. Active law no longer needs a
blacklist of temporal interpretations.

## Disposition

Keep source and destination as the exact ordered coordinates of the Movement
relation. Remove the negative earlier/later sentence.

No new occurrence, result, relation, or identity is introduced.
