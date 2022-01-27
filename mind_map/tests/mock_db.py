from tests.mock_models import Node

MOCK_DB_NODES = [
    None,
    Node(slug='spork', text='/spork', id=1, parent_id=None),
    Node(slug='spoon', text='/spork/spoon', id=2, parent_id=1),
    Node(slug='teacup', text='/teacup', id=3, parent_id=None),
    Node(slug='fork', text='/spork/fork', id=4, parent_id=1),
    Node(slug='fork', text='/spork/fork/fork', id=5, parent_id=4),
    None,
    None,
    None,
    Node(slug='knife', text='/spork/fork/fork/knife', id=9, parent_id=5),
    None,
    Node(slug='spoon', text='/spork/fork/spoon', id=11, parent_id=4),
    Node(slug='spatula', text='/spatula (1/2)', id=12, parent_id=None),
    Node(slug='spatula', text='/spatula (2/2)', id=13, parent_id=None)
    ]
