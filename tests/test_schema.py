from unittest.mock import Mock

from django.db.models import Manager, QuerySet

from hatchway.schema import DjangoGetterDict


def test_getitem():
    # Test getting an attribute from the Django object
    class MockObj:
        foo = 'bar'

    getter_dict = DjangoGetterDict(MockObj())
    assert getter_dict['foo'] == 'bar'

    # Test getting an attribute using Django's template Variable
    class MockObj:
        foo = 'bar'

    getter_dict = DjangoGetterDict(MockObj())
    assert getter_dict['foo'] == 'bar'

    # Test getting a non-existent attribute
    class MockObj:
        pass

    getter_dict = DjangoGetterDict(MockObj())
    try:
        getter_dict['foo']
    except KeyError:
        assert True
    else:
        assert False


def test_get():
    # Test getting an existing attribute
    class MockObj:
        foo = 'bar'

    getter_dict = DjangoGetterDict(MockObj())
    assert getter_dict.get('foo') == 'bar'

    # Test getting a non-existent attribute with a default value
    class MockObj:
        pass

    getter_dict = DjangoGetterDict(MockObj())
    assert getter_dict.get('foo', 'default') == 'default'


def test_convert_result():
    # Test converting a Manager object to a list
    class MockObj:
        manager = Mock(spec=Manager)
        manager.all.return_value = ['foo', 'bar']

    getter_dict = DjangoGetterDict(MockObj())
    assert getter_dict._convert_result(MockObj.manager) == ['foo', 'bar']

    # Test converting a QuerySet object to a list
    queryset_mock = Mock(spec=QuerySet)
    queryset_mock.__origin__ = QuerySet
    queryset_mock.__args__ = (str,)
    queryset_mock.__iter__ = lambda self: iter(['foo', 'bar'])

    class MockObj:
        queryset = queryset_mock

    getter_dict = DjangoGetterDict(MockObj())
    assert getter_dict._convert_result(MockObj.queryset) == ['foo', 'bar']

    # Test converting a callable object to its result
    class MockObj:
        def func(self):
            return 'foo'

    getter_dict = DjangoGetterDict(MockObj())
    print(getter_dict._convert_result(MockObj().func))
    assert getter_dict._convert_result(MockObj().func) == 'foo'
