import math

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry, Path
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

from breadcrumb.trail import Crumb, Trail


def yaw_from_quaternion(q):
    # Identity quaternion (0, 0, 0, 1) means no rotation: you were already facing it.
    siny = 2.0 * (q.w * q.z + q.x * q.y)
    cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny, cosy)


class TrailNode(Node):
    def __init__(self):
        super().__init__('breadcrumb')
        self.declare_parameter('drop_distance', 0.5)
        self.declare_parameter('drop_angle', 0.35)
        self.declare_parameter('max_crumbs', 2048)
        self.declare_parameter('frame_id', 'odom')

        self.trail = Trail(
            drop_distance=self.get_parameter('drop_distance').value,
            drop_angle=self.get_parameter('drop_angle').value,
            max_crumbs=self.get_parameter('max_crumbs').value,
        )
        self.frame_id = self.get_parameter('frame_id').value

        self.create_subscription(Odometry, 'odom', self._on_odom, 10)
        self.trail_pub = self.create_publisher(Path, '~/trail', 10)
        self.home_pub = self.create_publisher(Path, '~/path_home', 10)
        self.create_service(Trigger, '~/return_home', self._on_return_home)
        self.create_service(Trigger, '~/clear', self._on_clear)

    def _on_odom(self, msg):
        p = msg.pose.pose
        crumb = Crumb(
            x=p.position.x,
            y=p.position.y,
            yaw=yaw_from_quaternion(p.orientation),
            stamp=msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
        )
        if self.trail.offer(crumb):
            self.trail_pub.publish(self._to_path(self.trail.path_home()[::-1]))

    def _on_return_home(self, request, response):
        if not len(self.trail):
            response.success = False
            response.message = 'No trail recorded'
            return response
        self.home_pub.publish(self._to_path(self.trail.path_home()))
        response.success = True
        response.message = f'Returning home along {len(self.trail)} crumbs'
        return response

    def _on_clear(self, request, response):
        self.trail.clear()
        response.success = True
        response.message = 'Trail cleared'
        return response

    def _to_path(self, crumbs):
        path = Path()
        path.header.frame_id = self.frame_id
        path.header.stamp = self.get_clock().now().to_msg()
        for c in crumbs:
            ps = PoseStamped()
            ps.header.frame_id = self.frame_id
            ps.pose.position.x = c.x
            ps.pose.position.y = c.y
            ps.pose.orientation.z = math.sin(c.yaw / 2.0)
            ps.pose.orientation.w = math.cos(c.yaw / 2.0)
            path.poses.append(ps)
        return path


def main(args=None):
    rclpy.init(args=args)
    node = TrailNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
