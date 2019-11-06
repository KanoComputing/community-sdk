# CSharp SDK

This is an implementation of the SDK to communicate with the Motion Sensor Kit using CSharp.

When integrating to your own project remember to add this to the Capabilities section of your package manifest

```xml
<DeviceCapability Name="serialcommunication">
    <Device Id="vidpid:2341 814E">
    <Function Type="name:serialPort"/>
    </Device>
</DeviceCapability>
```

Check out the project `MotionSensorDemo` in the Solution.

Usage:

```csharp
namespace MotionSensorDemo
{
    public sealed partial class MainPage : Page
    {
        public MainPage()
        {
            this.InitializeComponent();
            InitMotion();
        }

        async void InitMotion()
        {
            // Get the first available sensor
            MotionSensor m = await MotionSensor.Create();

            // Listen to changes
            m.ProximityChanged += HandleProximityEvent;

            // Start the read loop. Callm.StopLoop() to stop
            m.StartLoop();
        }

        void HandleProximityEvent(object sender, ProximityEventArgs e)
        {
            // The distance value is a number between 0 and 255
            Value.Text = e.Proximity.ToString();
        }
    }
}
```

## Integration

You can build the KanoDevicesproject and integrate the final .dll in your projects
