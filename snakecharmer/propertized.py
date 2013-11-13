'''
Propertized allows you to create a class with properties that have metadata

For instance, let's say you are building an API with model-like objects for different vehicles.  
The object instance should store the data for each vehicle.  But you want the model itself to 
store various meta data about each property so that you can automatically build API docs.

class Vehicle(Propertized):
    manufacturer = Prop(label='Manufacturer', 
    horse_power = Prop(label='Horsepower', type=int, help_text='The power of the vehicle's engine')
    weight = Prop(label='Weight', type=int, help_text='The weight in pounds of the vehicle')
    max_speed = Prop(label='Max speed', type=int, help_text='The maximum speed, in MPH')

Now I can create an instance of the class:

ford_prefect = Vehicle(manufacturer='Ford', horse_power=120, weight=4000, max_speed=95)
>>> print ford_prefect.horse_power
-> 120
ford_prefect.horse_power = 110
>>> print ford_prefect.horse_power
-> 110

I can also programmatically get the metadata about the class properties.  I could use
this to generate documentation, so that I have one canonical represenation of my model.

doc_builder = []
for prop in Vehicle.list_class_props():
   doc_builder.append("""\
Field: %(label)s
Type: %(type)s
Description: %(help_text)s
""" % prop.__dict__)

print 'API Documentation:\n' + '\n'.join(doc_builder)



'''

import inspect



class Prop(property):
    """
    Use in conjunction with Propertized to create class attributes with fixed, associated, metadata
    """
    def __init__(self, default=None, label='', help_text='', stored_in_attr=None, **kwargs):
        this_prop = self
        self.default = default
        self.label = label
        self.help_text = help_text
        self.__dict__.update(kwargs)
        def fget(self):
            if stored_in_attr:
                val = getattr(self, stored_in_attr)[this_prop.attr_name]
            else:
                val = getattr(self, '_' + this_prop.attr_name, None)
            if val == None:
                if default != None:
                    if isinstance(default, type):
                        val = default()
                    else:
                        val = default

            return val
        def fset(self, value):
            if stored_in_attr:
                getattr(self, stored_in_attr)[this_prop.attr_name] = value
            else:
                setattr(self, '_' + this_prop.attr_name, value)
        super(Prop, self).__init__(fget=fget, fset=fset)


class Propertized(object):
    def __new__(typ, *args, **kwargs):
        obj = object.__new__(typ, *args, **kwargs)
        for attr_name in dir(obj.__class__):
            val = getattr(obj.__class__, attr_name)
            if isinstance(val, Prop):
                val.attr_name = attr_name
        return obj

    def __init__(self, *args, **kwargs):
        self._hydrate_from_kwargs(**kwargs)

    def _hydrate_from_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError("Class " + self.__class__.__name__ + " does not have attribute " + key)
    def __repr__(self):
        
        return '%s(**%s)' % (self.__class__.__name__, repr(self.as_dict()))

    def as_dict(self):
        d = {}
        for prop in self.list_class_props():
            d[prop.attr_name] = getattr(self, prop.attr_name, None)
        return d

    def list_class_props(self):
        props = []
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
            try:
                attr = getattr(self.__class__, attr_name)
            except:
                continue
            if inspect.ismethod(attr):
                continue

            if isinstance(attr, Prop):
                props.append(attr)
        return props
