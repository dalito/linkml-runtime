import unittest

from jsonasobj2 import JsonObj

from tests.test_utils.input.inlined_as_list import E, EInst


class InlinedAsListTestcase(unittest.TestCase):
    """Test the various YAML forms for inlined_as_list entries"""

    def test_list_variations(self):
        v = E()
        self.assertEqual(v.ev, [], "No entries, period")
        v = E({})
        self.assertEqual(v.ev, [], "Default is empty dictionary")
        v = E([])
        self.assertEqual(v.ev, [], "Empty list becomes empty dictionary")
        v = E(JsonObj())
        self.assertEqual(v.ev, [], "Empty JsonObj becomes empty dictionary")
        # Form 5 -- list of keys
        v1 = JsonObj(["k1", "k2"])
        v = E(v1)
        self.assertEqual(v.ev, [EInst(s1="k1", s2=None, s3=None), EInst(s1="k2", s2=None, s3=None)])
        # Form 4: -- list of key/object pairs
        v = E([{"k1": {"s1": "k1", "s2": "v21", "s3": "v23"}}, {"k2": {"s2": "v22", "s3": "v23"}}, {"k3": {}}])
        self.assertEqual(
            v.ev,
            [EInst(s1="k1", s2="v21", s3="v23"), EInst(s1="k2", s2="v22", s3="v23"), EInst(s1="k3", s2=None, s3=None)],
            "List of key value constructors",
        )

        with self.assertRaises(ValueError) as e:
            E([{"k1": None}, {"k1": "v2"}])
        self.assertIn("k1: duplicate key", str(e.exception))
        with self.assertRaises(ValueError) as e:
            E([{"k1": {"s1": "k2"}}])
        self.assertIn("Slot: ev - attribute s1 value (k2) does not match key (k1)", str(e.exception))

        # Form 5 variations
        v = E([{"k1": EInst(s1="k1", s2="v21", s3="v23")}, {"k2": JsonObj({"s2": "v22", "s3": "v23"})}, {"k3": None}])
        self.assertEqual(
            v.ev,
            [EInst(s1="k1", s2="v21", s3="v23"), EInst(s1="k2", s2="v22", s3="v23"), EInst(s1="k3", s2=None, s3=None)],
        )

        # More Form 5 variations
        v = E(["k1", "k2", {"k3": "v3"}, ["k4", "v4"], {"s1": "k5", "s2": "v52"}])
        self.assertEqual(
            v.ev,
            [
                EInst(s1="k1", s2=None, s3=None),
                EInst(s1="k2", s2=None, s3=None),
                EInst(s1="k3", s2="v3", s3=None),
                EInst(s1="k4", s2="v4", s3=None),
                EInst(s1="k5", s2="v52", s3=None),
            ],
            "Key value tuples",
        )

        # Form 6 - list of positional object values
        v = E([["k1", "v12", "v13"], ["k2", "v22"], ["k3"]])
        self.assertEqual(
            v.ev,
            [EInst(s1="k1", s2="v12", s3="v13"), EInst(s1="k2", s2="v22", s3=None), EInst(s1="k3", s2=None, s3=None)],
            "Positional objects",
        )

        # Form 7 - list of kv dictionaries
        v = E([{"s1": "v11", "s2": "v12"}, {"s1": "v21", "s2": "v22", "s3": "v23"}])
        self.assertEqual(
            v.ev, [EInst(s1="v11", s2="v12", s3=None), EInst(s1="v21", s2="v22", s3="v23")], "List of dictionaries"
        )

    def test_dict_variations(self):
        """Test various forms of inlined as list entries"""
        # Form 1: key / object
        v = E(
            {
                "k1": EInst(s1="k1", s2="v21", s3="v23"),
                "k2": JsonObj({"s2": "v22", "s3": "v23"}),
                "k3": {"s2": "v32", "s3": "v33"},
                "k4": {"s1": "k4"},
            }
        )
        self.assertEqual(
            v.ev,
            [
                EInst(s1="k1", s2="v21", s3="v23"),
                EInst(s1="k2", s2="v22", s3="v23"),
                EInst(s1="k3", s2="v32", s3="v33"),
                EInst(s1="k4", s2=None, s3=None),
            ],
            "Dictionary of key/object entries",
        )

        # Form 2: key/value tuples (only works when at most two values are required
        v = E(ev={"k1": "v11", "k2": "v21", "k3": {}})
        self.assertEqual(
            v.ev,
            [EInst(s1="k1", s2="v11", s3=None), EInst(s1="k2", s2="v21", s3=None), EInst(s1="k3", s2=None, s3=None)],
            "Dictionary of two-key entries",
        )

        # Form 3: Basic single object (differentiated from form2 by the presence of the key name
        v = E({"s1": "k1"})
        self.assertEqual(v.ev, [EInst(s1="k1", s2=None, s3=None)], "Single entry dictionary")
        v = E({"s1": "k1", "s2": "v12"})
        self.assertEqual(v.ev, [EInst(s1="k1", s2="v12", s3=None)], "Single entry dictionary")


if __name__ == "__main__":
    unittest.main()
