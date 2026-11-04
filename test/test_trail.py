from breadcrumb.trail import Crumb, Trail


def test_first_crumb_always_stored():
    t = Trail()
    assert t.offer(Crumb(0.0, 0.0, 0.0, 0.0))
    assert t.first == Crumb(0.0, 0.0, 0.0, 0.0)


def test_close_crumb_rejected():
    t = Trail(drop_distance=0.5)
    t.offer(Crumb(0.0, 0.0, 0.0, 0.0))
    assert not t.offer(Crumb(0.1, 0.0, 0.0, 1.0))


def test_heading_change_forces_crumb():
    t = Trail(drop_distance=10.0, drop_angle=0.3)
    t.offer(Crumb(0.0, 0.0, 0.0, 0.0))
    assert t.offer(Crumb(0.0, 0.0, 0.5, 1.0))


def test_path_home_ends_at_start():
    t = Trail(drop_distance=0.5)
    for i in range(5):
        t.offer(Crumb(float(i), 0.0, 0.0, float(i)))
    assert t.path_home()[-1] == t.first


def test_ring_buffer_drops_oldest():
    t = Trail(drop_distance=0.5, max_crumbs=3)
    for i in range(5):
        t.offer(Crumb(float(i), 0.0, 0.0, float(i)))
    assert len(t) == 3
    assert t.first.x == 2.0
