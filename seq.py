"""
@package wotc.mtgo.gre.grp.common.seq
"""

# Permit an unlimited number of public methods and allow use of '*'.
# pylint: disable=R0904,W0142

import operator
import functools
import itertools


class Op(object):
    """
    Functional operators useful when working with sequences
    """

    and_ = operator.and_
    or_ = operator.or_

    @classmethod
    def identity(cls, obj):
        """
        The identity function
        """
        return obj


    @classmethod
    def value(cls, value):
        """
        Returns a function that translates any argument to the supplied value
        """
        def inner(arg):
            return value
        return inner


    @classmethod
    def is_none(cls, obj):
        """
        Whether an object is None
        """
        return obj is None


    @classmethod
    def is_not_none(cls, obj):
        """
        Whether an object is not None
        """
        return obj is not None


    @classmethod
    def swap(cls, function):
        """
        Returns a function that evaluates another function with its arguments swapped
        """
        def inner(lhs, rhs):
            return function(rhs, lhs)
        return inner


    @classmethod
    def compose(cls, function1, function2):
        """
        Compose a function applying two other functions in reverse order
        """
        def inner(*args, **keyword_args):
            return function1(function2(*args, **keyword_args))
        return inner


    @classmethod
    def and_then(cls, function1, function2):
        """
        Compose a function applying two other functions in order
        """
        return cls.compose(function2, function1)


    @classmethod
    def attr(cls, attr):
        """
        Given an attribute, returns a function that gets that attribute from an object
        """
        return operator.attrgetter(attr)


    @classmethod
    def value(cls, value):
        """
        Give a value, returns a function that always returns that value
        """
        return lambda item: value


    @classmethod
    def attr_of(cls, obj):
        """
        Given an object, returns a function that gets an attribute from that object
        """
        return cls._apply_lhs_argument(getattr, obj)


    @classmethod
    def item(cls, index):
        """
        Given an item, returns a function that gets that item from an object
        """
        return operator.itemgetter(index)


    @classmethod
    def item_of(cls, obj):
        """
        Given an object, returns a function that gets an item from that object
        """
        return cls._apply_lhs_argument(operator.getitem, obj)


    @classmethod
    def contains(cls, item):
        """
        Given an item, return a predicate that tests if that item is contained in a sequence
        """
        return cls._apply_rhs_argument(operator.contains, item)


    @classmethod
    def contained_in(cls, seq):
        """
        Given an sequence, return a predicate that tests if an item is contained in that sequence
        """
        return cls._apply_lhs_argument(operator.contains, seq)


    @classmethod
    def equals(cls, obj):
        """
        Returns a predicate that tests whether an object is equal to the specified object
        """
        return cls._apply_lhs_argument(operator.eq, obj)


    @classmethod
    def not_equals(cls, obj):
        """
        Returns a predicate that tests whether an object is not equal to the specified object
        """
        return cls._apply_lhs_argument(operator.ne, obj)


    @classmethod
    def is_instance(cls, classinfo):
        """
        Returns a predicate that tests whether an object is an instance of the specified type
        """
        return cls._apply_rhs_argument(isinstance, classinfo)


    @classmethod
    def lhs(cls, lhs, _rhs):
        """
        A binary operator that returns its first argument
        """
        return lhs


    @classmethod
    def rhs(cls, _lhs, rhs):
        """
        A binary operator that returns its second argument
        """
        return rhs


    @classmethod
    def compare_and_choose(cls, compare, key):
        """
        Compare two items and return 5y3
        """
        if key is None:
            if compare == operator.le:
                return min
            elif compare == operator.ge:
                return max
            else:
                raise ValueError("unexpected operator")
        def inner(lhs, rhs):
            return lhs if compare(key(lhs), key(rhs)) else rhs
        return inner


    @classmethod
    def _apply_lhs_argument(cls, binary_operator, lhs):
        """
        Returns the unary operator resulting from applying a binary operator
        with the first argument equal to 'lhs'
        """
        return functools.partial(binary_operator, lhs)


    @classmethod
    def _apply_rhs_argument(cls, binary_operator, rhs):
        """
        Returns the unary operator resulting from applying a binary operator
        with the second argument equal to 'rhs'
        """
        def inner(lhs):
            return binary_operator(lhs, rhs)
        return inner


class Seq(object):
    """
    Fluent inteface to itertools in the style of LINQ
    """

    def __init__(self, iterable):
        """
        Constructor a sequence from an iterable
        """
        self._iterable = iterable

    def __iter__(self):
        """
        Gets the iterator for this object
        """
        return iter(self._iterable)


    empty = None


    @classmethod
    def from_items(cls, *args):
        """
        Return a sequence of the specified items
        """
        return cls(args)


    @classmethod
    def chain(cls, *args):
        """
        Return a sequence of the items in the specified sub-sequences
        """
        return cls(itertools.chain(*args))


    @classmethod
    def from_repeat(cls, item, count=None):
        """
        Repeat the specified item as a sequence
        """
        if count is None:
            return cls(itertools.repeat(item))
        else:
            return cls(itertools.repeat(item, count))


    @classmethod
    def from_range(cls, *args, **keyword_args):
        """
        Returns a sequence of consecutive integers
        """
        return cls(range(*args, **keyword_args))


    @classmethod
    def from_count(cls, start=0, step=1):
        """
        Return an infinte sequence of consecutive integers

        Start the sequence with a starting value if it is provided.
        """
        return cls(itertools.count(start, step))


    @classmethod
    def prepend(cls, item, sequence):
        """
        Prepend an item to a sequence
        """
        return cls(itertools.chain([item], sequence))


    @classmethod
    def append(cls, item, sequence):
        """
        Append an item to a sequence
        """
        return cls(itertools.chain(sequence, [item]))


    def cycle(self):
        """
        Cycle through a sequence repeatedly
        """
        return itertools.cycle(self._iterable)


    def first(self, predicate=None):
        """
        Return the first item in a sequence

        @param predicate Optional predicate used as a filter
        """
        return next(iter(self._iterable_or_filter(predicate)))


    def first_or_default(self, predicate=None, default=None):
        """
        Return the first item in a sequence or a default value if empty

        If function is provided, use it as a filtering predicate.
        """
        return next(iter(self._iterable_or_filter(predicate)), default)


    def first_not_none(self):
        """
        Return the first item in a sequence that is not None
        """
        return self.first_or_default(Op.identity)


    def last(self, predicate=None):
        """
        Return the last item in a sequence

        If function is provided, use it as a filtering predicate.
        """
        return functools.reduce(Op.rhs, self._iterable_or_filter(predicate))


    def last_or_default(self, predicate=None, default=None):
        """
        Return the last item in a sequence or a default value if empty

        If function is provided, use it as a filtering predicate.
        """
        return functools.reduce(Op.rhs, self._iterable_or_filter(predicate), default)


    def count(self, predicate=None):
        """
        Count the number of items in a sequence

        If function is provided, use it as a filtering predicate.
        """
        return sum(1 for i in self._iterable_or_filter(predicate))


    def enumerate(self, start=0):
        """
        Enumerate items in a sequence

        Maps a sequence to tuples of sequence number of item starting at start
        """
        return Seq(enumerate(self._iterable, start=start))


    def sum(self, function=None):
        """
        Sum items in a sequence

        If function is provided, use it to map items to sum over.
        """
        return sum(self._iterable_or_map(function))


    def min(self, key=None):
        """
        Return the item from a sequence whose value is the smallest

        If key function is provided, compare values extracted with it.
        """
        if key is None:
            return min(self._iterable)
        return functools.reduce(Op.compare_and_choose(operator.le, key), self._iterable)


    def max(self, key=None):
        """
        Return the item from a sequence whose key value is the largest

        If key function is provided, compare values extracted with it.
        """
        if key is None:
            return max(self._iterable)
        return functools.reduce(Op.compare_and_choose(operator.ge, key), self._iterable)


    def all(self, predicate=None):
        """
        True if all items in a sequence evaluate to true

        If predicate is provided, use its value instead.
        """
        return all(self._iterable_or_map(predicate))


    def any(self, predicate=None):
        """
        True if any of the items in a sequence evaluate to true

        If predicate is provided, use its value instead.
        """
        return any(self._iterable_or_map(predicate))


    def fold(self, function):
        """
        Apply function to pairs of elements in a sequence
        """
        return functools.reduce(function, self._iterable)


    def fold_left(self, start, function):
        """
        Apply function to pairs of elements in a sequence from the left

        Return 'start' if the sequence is empty.
        """
        return functools.reduce(function, self._iterable, start)


    def fold_right(self, start, function):
        """
        Apply function to pairs of elements in a sequence from the right

        Return 'start' if the sequence is empty.
        """
        return functools.reduce(Op.swap(function), reversed(list(self._iterable)), start)


    def items_of(self, dict):
        """
        """
        return Seq(map(lambda key: (key, dict[key]), self._iterable))


    def foreach(self, function):
        """
        Evaluate function for each item in a sequence
        """
        for item in self._iterable:
            function(item)


    def foreach_star(self, function):
        """
        Evaluate function for each item in a sequence
        """
        for item in self._iterable:
            function(*item)


    def concat(self, other):
        """
        Concatenate one sequence with another
        """
        return Seq(itertools.chain(self._iterable, other))


    def reverse(self):
        """
        Reverse the items in a sequence
        """
        return Seq(reversed(list(self._iterable)))


    def flatten(self):
        """
        Flatten sequence of subsequences into a single sequence
        in all the results
        """
        return Seq(itertools.chain.from_iterable(self._iterable))


    def slice(self, *args, **keyword_args):
        """
        Apply slice operator to each item in a sequence
        """
        return Seq(itertools.islice(self._iterable, *args, **keyword_args))


    def map(self, function):
        """
        Map function over items from a sequence
        """
        return Seq(map(function, self._iterable))


    def map_tuple(self, *functions):
        """
        Map functions over items from a sequence creating a sequence of tuples
        """
        return Seq(map(lambda item: tuple(map(lambda function: function(item), functions)), self._iterable))


    def map_star(self, function):
        """
        Map function over items from a sequence converting item subsequence to arguments
        """
        return Seq(itertools.starmap(function, self._iterable))


    def map_many(self, function):
        """
        Map function over items and produce a single sequence from the items
        in all the results
        """
        return Seq(itertools.chain.from_iterable(map(function, self._iterable)))


    def map_star_many(self, function):
        """
        Map function over items from a sequence converting item subsequence to arguments
        and produce a single sequence from the items in all the results
        """
        return Seq(itertools.chain.from_iterable(itertools.starmap(function, self._iterable)))


    def group_by(self, key=Op.identity, function=None):
        """
        Group adjacent items with consecutive keys into subsequences
        """
        def select_items(key, items):
            return (key, Seq(items))
        def select_items_with_key(key, items):
            return (key, Seq(map(function, items)))
        selector = select_items if function is None else select_items_with_key
        return Seq(itertools.starmap(selector, itertools.groupby(self._iterable, key)))


    def filter(self, predicate):
        """
        Filter items from a sequence accepting items satisfying predicate
        """
        return Seq(filter(predicate, self._iterable))


    def filter_not(self, predicate):
        """
        Filter items from a sequence rejecting items satisfying predicate
        """
        return Seq(itertools.filterfalse(predicate, self._iterable))


    def filter_star(self, predicate):
        """
        Filter items from a sequence accepting items satisfying predicate
        using item subsequence as arguments
        """
        def function(item):
            if predicate(*item):
                yield item
        return Seq(itertools.chain.from_iterable(map(function, self._iterable)))


    def filter_star_not(self, predicate):
        """
        Filter items from a sequence rejecting items satisfying predicate
        using item subsequence as arguments
        """
        def function(item):
            if not predicate(*item):
                yield item
        return Seq(itertools.chain.from_iterable(map(function, self._iterable)))


    def drop(self, count):
        """
        Drop first 'count' items from a sequence
        """
        return Seq(itertools.islice(self._iterable, count, None))


    def take(self, count):
        """
        Take first 'count' items from a sequence
        """
        return Seq(itertools.islice(self._iterable, count))


    def drop_while(self, function):
        """
        Take items from a sequence while predicate is true
        """
        return Seq(itertools.dropwhile(function, self._iterable))


    def take_while(self, function):
        """
        Take item from a sequence while predicate is true
        """
        return Seq(itertools.takewhile(function, self._iterable))


    def zip(self, other, function=None):
        """
        Zip sequence with another into tuples

        If a function is provided, call that function with the sequence items as arguments.
        """
        if function is None:
            return Seq(zip(self._iterable, other))
        else:
            return Seq(itertools.starmap(function, zip(self._iterable, other)))


    def zip_from_each(self, function=None):
        """
        Zips subsequences of a sequence into tuples

        If a function is provided, call that function with the sequence
        items as arguments.
        """
        if function is None:
            return Seq(zip(*self._iterable))
        else:
            return Seq(map(function, *self._iterable))


    def sort(self, key=None, reverse=False):
        """
        Sort a sequence

        If a function is provided, use its value as the sort key.
        """
        return Seq(sorted(self._iterable, key=key, reverse=reverse))


    def distinct(self):
        """
        Produce a sequence of distinct elements from a sequence
        """

        def inner(iterable):
            items = set()
            for item in iterable:
                if item not in items:
                    yield item
                    items.add(item)

        return Seq(inner(self._iterable))


    def totuple(self):
        """
        Convert a sequence to a tuple
        """
        return tuple(self._iterable)


    def tolist(self):
        """
        Convert a sequence to a list
        """
        return list(self._iterable)


    def todict(self, function=None):
        """
        Convert a sequence of subsequence pairs to a dictionary
        """
        if function:
            keys = list(self._iterable)
            return dict(zip(keys, map(function, keys)))
        else:
            return dict(self._iterable)


    def toset(self):
        """
        Convert a sequence to a set
        """
        return set(self._iterable)


    def tocollection(self, collection):
        """
        Convert a sequence to a set
        """
        return collection(self._iterable)


    def persist(self):
        """
        Persist a sequence so that it may be iterated multiple times

        This can be useful while debugging to prevent the iterable from
        being consume.
        """
        return Seq(list(self._iterable))


    def _iterable_or_map(self, function):
        if function is None:
            return self._iterable
        else:
            return map(function, self._iterable)


    def _iterable_or_filter(self, predicate):
        if predicate is None:
            return self._iterable
        else:
            return filter(predicate, self._iterable)


Seq.empty = Seq([])
