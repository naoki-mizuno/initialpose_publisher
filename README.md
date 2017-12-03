# initialpose_publisher

Publeshes the /initiapose (or any other topic name specified) by getting the
pose from `map` to `base_link` transform.

This script was written to provide the starting position for the local
planner, which needs the current robot position (i.e. `base_link`) as the
starting point.

## Parameters

- `map_frame_id`: the parent frame
- `base_frame_id`: the child frame
- `topic_name`: the topic name to publish to
- `hz`: the rate to publish the topic

## Subscribed topics

None

## Published topics

- `initialpose`: mainly used by rviz, but the subscriber can be arbitrary

## License

MIT License

## Author

Naoki Mizuno
