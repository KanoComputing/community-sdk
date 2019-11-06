using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Windows.Devices.SerialCommunication;
using Windows.Devices.Enumeration;
using Windows.Storage.Streams;
using Windows.Data.Json;

namespace KanoDevices
{
    public class ProximityEventArgs : EventArgs
    {
        public ProximityEventArgs(int p)
        {
            Proximity = p;
        }

        public int Proximity { get; set; }
    }

    public class MotionSensor
    {
        public event EventHandler<ProximityEventArgs> ProximityChanged;
   
        private static string aqsFilter = SerialDevice.GetDeviceSelectorFromUsbVidPid(0x2341, 0x814e);

        private bool IsReading = false;

        private SerialDevice Device = null;

        public MotionSensor(SerialDevice device) {
            Device = device;
            Device.BaudRate = 115200;
        }

        public static async Task<DeviceInformationCollection> GetAll()
        {
            return await DeviceInformation.FindAllAsync(aqsFilter);
        }

        public static async Task<MotionSensor> CreateFromDeviceInformation(DeviceInformation info)
        {

            SerialDevice device = await SerialDevice.FromIdAsync(info.Id);

            return new MotionSensor(device);
        }

        public static async Task<MotionSensor> Create()
        {
            DeviceInformationCollection devices = await GetAll();

            if (devices.Count == 0)
            {
                throw new Exception("Could not find any Motion Sensor");
            }

            return await CreateFromDeviceInformation(devices[0]);
        }

        public async void StartLoop() {
            if (IsReading == true)
            {
                return;
            }
            IsReading = true;
            // Create the input stream and data reader to extract data from the sensor
            IInputStream stream = Device.InputStream;
            DataReader reader = new DataReader(stream);
            // This will store incomplete packets
            string buffer = "";
            // This will store the most recent JSON packet
            JsonObject value = new JsonObject();
            while (IsReading == true) {
                // Extract the next 32 bytes
                await reader.LoadAsync(32);
                string res = reader.ReadString(32);
                buffer += res;
                // Split by line return to see if there are any valid packets
                string[] tokens = buffer.Split('\n');
                // This willstore all incomplete packets to go back into the buffer
                List<string> outTokens = new List<string>();
                foreach (string token in tokens)
                {
                    bool success = JsonObject.TryParse(token, out value);
                    // Found a valid packet
                    if (success)
                    {
                        // Validate the proximity event
                        if (value.GetNamedString("type") == "event" && value.GetNamedString("name") == "proximity-data")
                        {
                            // Extract the Proximity data
                            JsonObject detail = value.GetNamedObject("detail");
                            OnRaiseProximityEvent(new ProximityEventArgs((int)detail.GetNamedNumber("proximity")));
                        }
                    }
                    else
                    {
                        outTokens.Add(token);
                    }
                }
                // Rebuild the buffer from the incomplete packets
                buffer = string.Join("\n", outTokens.ToArray());
            }
        }

        public void StopLoop()
        {
            IsReading = false;
        }

        protected virtual void OnRaiseProximityEvent(ProximityEventArgs e)
        {
            ProximityChanged?.Invoke(this, e);
        }
    }
}
