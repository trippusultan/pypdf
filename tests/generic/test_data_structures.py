"""Test for TreeObject.insert_child KeyError fix (#3727)."""

from pypdf import PdfWriter
from pypdf.generic import NameObject, TextStringObject, TreeObject


def test_treeobject_insert_child_no_keyerror_on_missing_next_key() -> None:
    """Test that insert_child does not raise KeyError on freshly-created children.

    When inserting a child before a node that has no /Prev key (i.e. the TreeObject
    has exactly one existing child), the except branch of insert_child previously
    called ``del child_obj["/Next"]`` which raised KeyError because a fresh child has
    no /Next key yet. The fix uses ``child_obj.pop(NameObject("/Next"), None)`` so
    the KeyError is not raised.

    Reproduces: py-pdf/pypdf#3727
    """
    writer = PdfWriter()
    tree = TreeObject()
    writer._add_object(tree)

    child1 = TreeObject()
    child1[NameObject("/Foo")] = TextStringObject("existing")
    writer._add_object(child1)

    child2 = TreeObject()
    child2[NameObject("/Bar")] = TextStringObject("new")

    # Inserting before the only existing child exercises the except branch;
    # this must not raise KeyError.
    tree.insert_child(child2, before=child1, pdf=writer)
