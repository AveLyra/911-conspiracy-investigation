# Rendered message supplements

The chat JSON is preserved as returned by the reader. Ten additional exact message UI captures are stored here with the conversation and message IDs, capture URL, rendered text, and outerHTML.

- **6 reader-truncated assistant items**: the raw chat record retains its `truncated: true` marker; the UI capture supplies the full rendered message.
- **4 saved original-response entries**: the Sources crosswalk identifies the original response message ID, but the reader’s chat turn payload omitted that message object. Each original was opened from its Project Sources card and captured from the exact `data-chatgpt-selection-message-id` element.

## Reader-truncated items

| Thread ID | Message ID | Capture |
|---|---|---|
| `6aed3f60-dff8-83e9-b257-0cbf50fcbb3d` | `cfdca72b-d0c6-42d3-8861-bbfb0e3c1416` | [`cfdca72b-d0c6-42d3-8861-bbfb0e3c1416.json`](cfdca72b-d0c6-42d3-8861-bbfb0e3c1416.json) |
| `6aed3f60-dff8-83e9-b257-0cbf50fcbb3d` | `aeb7c236-1d10-47ca-93e6-744c1b423fd3` | [`aeb7c236-1d10-47ca-93e6-744c1b423fd3.json`](aeb7c236-1d10-47ca-93e6-744c1b423fd3.json) |
| `6aed5f05-ee50-83e9-af9a-654ee50b07ab` | `cfdead6e-39cc-5e53-abfc-c8ccf20380bc` | [`cfdead6e-39cc-5e53-abfc-c8ccf20380bc.json`](cfdead6e-39cc-5e53-abfc-c8ccf20380bc.json) |
| `6aee7413-a344-83e9-a3f0-ac8203392e27` | `66e67abe-983d-4e14-941b-9975848c9370` | [`66e67abe-983d-4e14-941b-9975848c9370.json`](66e67abe-983d-4e14-941b-9975848c9370.json) |
| `6aee73f9-c640-83ea-b6ac-f40a7ab5f86d` | `49a7361d-b71b-448f-a951-7f0f89fa6127` | [`49a7361d-b71b-448f-a951-7f0f89fa6127.json`](49a7361d-b71b-448f-a951-7f0f89fa6127.json) |
| `6aee73d6-8f14-83ea-9d63-eabd3d4fe29d` | `b9eb01db-69d8-40e2-95d2-e58fbd16ed25` | [`b9eb01db-69d8-40e2-95d2-e58fbd16ed25.json`](b9eb01db-69d8-40e2-95d2-e58fbd16ed25.json) |

## Saved responses absent from reader turn payload

| Source title | Thread ID | Message ID | Capture |
|---|---|---|---|
| Mover evidence research brief | `6aed5cff-530c-83ea-8190-98115bea8f5d` | `64875fca-00bb-5b57-be05-d16b068250ce` | [`64875fca-00bb-5b57-be05-d16b068250ce.json`](64875fca-00bb-5b57-be05-d16b068250ce.json) |
| Federal records and licensing gaps | `6aed3f60-dff8-83e9-b257-0cbf50fcbb3d` | `c7df2635-efb7-47b6-8754-79b68c0c5983` | [`c7df2635-efb7-47b6-8754-79b68c0c5983.json`](c7df2635-efb7-47b6-8754-79b68c0c5983.json) |
| Visitor Card Investigation Update | `6aed3f60-dff8-83e9-b257-0cbf50fcbb3d` | `81c2c609-43b8-498f-83a8-2f53efef2852` | [`81c2c609-43b8-498f-83a8-2f53efef2852.json`](81c2c609-43b8-498f-83a8-2f53efef2852.json) |
| Saudi Intelligence Links Corroborated | `6aed3f60-dff8-83e9-b257-0cbf50fcbb3d` | `fcd772f8-bee6-4736-a5d2-1b4c30496f3a` | [`fcd772f8-bee6-4736-a5d2-1b4c30496f3a.json`](fcd772f8-bee6-4736-a5d2-1b4c30496f3a.json) |
