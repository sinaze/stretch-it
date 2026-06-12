"""Class for periodic lattices."""

import numpy as np


class Periodic_Lattice(np.ndarray):
    """Creates an n-dimensional ring that joins on boundaries w/ numpy.

    Required Inputs
        array :: np.array :: n-dim numpy array to use wrap with

    Only currently supports single point selections wrapped around the boundary
    """

    def __new__(cls, input_array, lattice_spacing=None):
        """__new__ is called by numpy when and explicit constructor is used.

        obj = MySubClass(params) otherwise we must rely on __array_finalize
        """
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)

        # add the new attribute to the created instance
        obj.lattice_shape = input_array.shape
        obj.lattice_dim = len(input_array.shape)
        obj.lattice_spacing = lattice_spacing

        # Finally, we must return the newly created object:
        return obj

    def __getitem__(self, index):
        """Insert."""
        index = self.latticeWrapIdx(index)
        return super(Periodic_Lattice, self).__getitem__(index)

    def __setitem__(self, index, item):
        """Insert."""
        index = self.latticeWrapIdx(index)
        return super(Periodic_Lattice, self).__setitem__(index, item)

    def __array_finalize__(self, obj):
        """Insert.

        ndarray.__new__ passes __array_finalize__ the new object,
        of our own class (self) as well as the object from which the view has
        been taken (obj).
        See
        http://docs.scipy.org/doc/numpy/user/basics.subclassing.html#simple-example-adding-an-extra-attribute-to-ndarray
        for more info
        """
        if obj is None:
            return
        self.lattice_shape = getattr(obj, 'lattice_shape', obj.shape)
        self.lattice_dim = getattr(obj, 'lattice_dim', len(obj.shape))
        self.lattice_spacing = getattr(obj, 'lattice_spacing', None)
        pass

    def latticeWrapIdx(self, index):
        """Return periodic lattice index for a given iterable index.

        Required Inputs:
            index :: iterable :: one integer for each axis

        This is NOT compatible with slicing
        """
        # handle integer slices
        if not hasattr(index, '__iter__'):
            return index
        # must reference a scalar
        if len(index) != len(self.lattice_shape):
            return index
        # slices not supported
        if any(type(i) == slice for i in index):
            return index
        # periodic indexing of scalars
        if len(index) == len(self.lattice_shape):
            mod_index = tuple(((i % s + s) % s
                              for i, s in zip(index, self.lattice_shape)))
            return mod_index
        raise ValueError('Unexpected index: {}'.format(index))
