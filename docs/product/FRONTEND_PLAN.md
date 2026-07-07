API

External clients can interact with HomeSteadOS through the FastAPI HTTP API.

Main API areas:

System status
System mode
System snapshot
Devices
Rooms
Actions
Text commands
Scenes
Shortcuts
Automations
Audit log
Command history
Behaviour insights
v1.0 Design Principles
Local first
Privacy first
Safety before convenience
AI should propose actions, not directly control devices
All control paths should use structured Actions
Services should not bypass the Safety Engine
Runtime state should be inspectable through safe read-only services
Features should be testable and explainable
Explicitly Out of Scope for v1.0

The following are intentionally not part of v1.0:

Full AI planner
Voice control
Mobile app
User accounts
Role-based permissions
Database persistence
Complex automation condition logic
Scheduling engine
Real-time Home Assistant state sync
MQTT integration
Cloud deployment
Notifications
Advanced analytics
Machine learning