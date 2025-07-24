using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO.Ports;
using System.Threading;
using System.IO;
using System.Windows.Forms.DataVisualization.Charting;

namespace GUI
{
    public partial class Form1 : Form
    {
        private int dutyCycle = 0;
        SerialPort serialPort;
        private int encoderCounts = 0;
        private int shuntVoltage = 0;
        private int currentAmps = 0;
        private int encoderDegrees = 0;
        private int curr_kp = 0;
        private int curr_ki = 0;
        string stm32_response = null;
        private CancellationTokenSource _cts = new CancellationTokenSource();



        private Series currentSeries;
        private ChartArea chartArea;
        private double timeMs = 0;
        private double sampleIntervalMs = 0.1; // 10 kHz sampling rate
        private double frequencyHz = 100;
        private double amplitude = 200;
        private int maxPoints = 400; // Show last 40 ms (at 0.1 ms per point)
        public Form1()
        {
            InitializeComponent();
            InitializeSerial();
            //PlotCurrentTrajectory();
            SetupChart();
            SetupTimer();
            //serialPort.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);
        }


        private void SetupChart()
        {
            chart_CurrentControl.Series.Clear();
            chart_CurrentControl.ChartAreas.Clear();

            chartArea = new ChartArea();
            chartArea.AxisX.Title = "Time (ms)";
            chartArea.AxisX.TitleFont = new Font(new FontFamily("Arial"), 10, FontStyle.Bold);
            chartArea.AxisY.Title = "Current (mA)";
            chartArea.AxisY.TitleFont = new Font("Arial", 10, FontStyle.Bold); // Bold Y-axis label

            chartArea.AxisX.Minimum = 0;
            chartArea.AxisX.Maximum = 40;
            chartArea.AxisY.Minimum = -amplitude * 1.2;
            chartArea.AxisY.Maximum = amplitude * 1.2;

            chartArea.AxisX.MajorGrid.Enabled = false;
            chartArea.AxisY.MajorGrid.Enabled = false;

            chart_CurrentControl.ChartAreas.Add(chartArea);

            currentSeries = new Series("Current");
            currentSeries.ChartType = SeriesChartType.Line;
            currentSeries.BorderWidth = 2;
            chart_CurrentControl.Series.Add(currentSeries);

            // Set chart title with styling
            chart_CurrentControl.Titles.Clear();
            Title chartTitle = new Title("Reference Current : 100 Hz Square Wave");
            chartTitle.Font = new Font("Arial", 12, FontStyle.Bold);
            chartTitle.Alignment = ContentAlignment.TopCenter;
            chart_CurrentControl.Titles.Add(chartTitle);

            chart_CurrentControl.DoubleBuffered(true); // Reduce flicker
        }
        private void SetupTimer()
        {
            timer_ChartUpdate.Interval = 1; // 1 ms timer tick
            timer_ChartUpdate.Tick += UpdatePlot;
            timer_ChartUpdate.Start();
        }


        private void UpdatePlot(object sender, EventArgs e)
        {
            double tSec = timeMs / 1000.0;
            double current = amplitude * Math.Sign(Math.Sin(2 * Math.PI * frequencyHz * tSec));

            currentSeries.Points.AddXY(timeMs, current);

            // Remove old points to keep the window within 40ms
            while (currentSeries.Points.Count > maxPoints)
            {
                currentSeries.Points.RemoveAt(0);
            }

            // Adjust X-axis to scroll with time
            if (timeMs > 40)
            {
                chartArea.AxisX.Minimum = timeMs - 40;
                chartArea.AxisX.Maximum = timeMs;
            }

            timeMs += sampleIntervalMs;
        }



        private void textBox1_TextChanged(object sender, EventArgs e)
        {


        }

        private void InitializeSerial()
        {
            serialPort = new SerialPort();
            serialPort.PortName = "COM9"; // Replace with your port
            serialPort.BaudRate = 115200;
            serialPort.DataBits = 8;
            serialPort.Parity = Parity.None;
            serialPort.StopBits = StopBits.One;
            serialPort.Open();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            Task.Run(() => SerialListener(_cts.Token));
        }

        private void SerialListener(CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {

                stm32_response = serialPort.ReadLine();
                serialPort.DiscardInBuffer();
                Console.WriteLine(stm32_response);

                if (stm32_response.StartsWith("ENC:") && int.TryParse(stm32_response.Substring(4), out encoderCounts))
                {
                    // Update UI (on main thread)
                    this.Invoke(new Action(() =>
                    {
                        encoderCntsTxtBox.Text = encoderCounts.ToString();
                        
                    }));
                }

                if (stm32_response.StartsWith("ENC_DEG:") && int.TryParse(stm32_response.Substring(8), out encoderDegrees))
                {
                    // Update UI (on main thread)
                    this.Invoke(new Action(() =>
                    {
                        EncoderDegsTxtBox.Text = encoderDegrees.ToString();
                       
                    }));
                }

                if (stm32_response.StartsWith("RESET_ENC_CNTS:") && int.TryParse(stm32_response.Substring(15), out encoderCounts))
                {
                    // Update UI (on main thread)
                    this.Invoke(new Action(() =>
                    {
                        //this should read encoder cnts as zero
                        encoderCntsTxtBox.Text = encoderCounts.ToString();

                    }));
                }

                if (stm32_response.StartsWith("CURR_mA:") && int.TryParse(stm32_response.Substring(8), out currentAmps))
                {
                    // Update UI (on main thread)
                    this.Invoke(new Action(() =>
                    {
                        //this should read encoder cnts as zero
                        double current_milliAmps= currentAmps * 0.1;
                        currentAmpsTxtBox.Text = current_milliAmps.ToString();

                    }));
                }

                if (stm32_response.StartsWith("ADC_CNTS:") && int.TryParse(stm32_response.Substring(9), out shuntVoltage))
                {
                    // Update UI (on main thread)
                    this.Invoke(new Action(() =>
                    {
                        //this should read encoder cnts as zero
                        double shunt_voltage_volts = shuntVoltage * 0.00001;
                        shuntVoltageTxtBox.Text = shunt_voltage_volts.ToString();

                    }));
                }



                if (stm32_response.StartsWith("PWM_REQ:"))
                {
                    if (int.TryParse(pwmTextBox.Text, out dutyCycle))
                    {
                        if (serialPort != null && serialPort.IsOpen)
                        {
                            byte[] data = BitConverter.GetBytes(dutyCycle); // little endian by default
                            serialPort.Write(data, 0, data.Length);

                            this.Invoke(new Action(() =>
                            {
                                //this should read encoder cnts as zero
                                statusTextBox.Text = "Duty Cycle set to:" + dutyCycle.ToString();

                            }));

                            // Optional: Show a message or status update
                            //MessageBox.Show("Sent: " + dutyCycle);
                        }
                        else
                        {
                            //MessageBox.Show("Serial port not open.");
                        }
                    }
                    else
                    {
                        // Invalid input
                        //MessageBox.Show("Please enter a valid number.");
                    }
                }


                if (stm32_response.StartsWith("CURR_Kp_Ki:"))
                {
                    if (serialPort != null && serialPort.IsOpen)
                    {
                        int curr_kp = int.Parse(currentKpTxtBox.Text);
                        int curr_ki = int.Parse(CurrentKiTxtBox.Text);

                        byte[] kpBytes = BitConverter.GetBytes(curr_kp); // 4 bytes
                        byte[] kiBytes = BitConverter.GetBytes(curr_ki); // 4 bytes

                        // Optional: Add a simple header (e.g., 0xAA, 0x55) to signal start
                        byte[] packet = new byte[8];
                        Array.Copy(kpBytes, 0, packet, 0, 4);
                        Array.Copy(kiBytes, 0, packet, 4, 4);

                        serialPort.Write(packet, 0, packet.Length);
                    }
                }



            }
        }

       //Send the desired duty cycle
        private void sendDutyCycleButtonClick(object sender, EventArgs e)
        {
            if (serialPort != null && serialPort.IsOpen)
            {
                string message = "f\n";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serialPort.Write(buffer, 0, buffer.Length);
                
                // Optional: Show a message or status update
                //MessageBox.Show("Sent: " + dutyCycle);
            }
            
        }

        //read raw encoder cnts
        private void readEncoderCntsClick(object sender, EventArgs e)
        {
            if(serialPort != null && serialPort.IsOpen)
            {
                string message = "a\n";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serialPort.Write(buffer, 0, buffer.Length);

              

            }
        }

        //read encoder cnts in degrees
        private void readEncoderDegreesClick(object sender, EventArgs e)
        {
            if (serialPort != null && serialPort.IsOpen)
            {
                string message = "b\n";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serialPort.Write(buffer, 0, buffer.Length);

            }
        }

        //reset encoder counts
        private void resetEncoderClick(object sender, EventArgs e)
        {
            if (serialPort != null && serialPort.IsOpen)
            {
                string message = "c\n";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serialPort.Write(buffer, 0, buffer.Length);

            }
        }

        //read current sensor adc counts(shunt voltage)
        private void readADCCountsClick(object sender, EventArgs e)
        {
            if (serialPort != null && serialPort.IsOpen)
            {
                string message = "d\n";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serialPort.Write(buffer, 0, buffer.Length);

            }

        }

        //read current sensor reading in mA
        private void readCurrentAmpsClick(object sender, EventArgs e)
        {
            if (serialPort != null && serialPort.IsOpen)
            {
                string message = "e\n";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serialPort.Write(buffer, 0, buffer.Length);

            }
        }

        private void stopBtn_Click(object sender, EventArgs e)
        {
            if (serialPort != null && serialPort.IsOpen)
            {
                string message = "p\n";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serialPort.Write(buffer, 0, buffer.Length);

            }
        }

        private void testCurrentControlBtn_Click(object sender, EventArgs e)
        {
            if (serialPort != null && serialPort.IsOpen)
            {
                string message = "k\n";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serialPort.Write(buffer, 0, buffer.Length);

            }
        }

        private void setCurrentGainsBtn_Click(object sender, EventArgs e)
        {
            if (serialPort != null && serialPort.IsOpen)
            {
                string message = "g\n";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serialPort.Write(buffer, 0, buffer.Length);

            }
        }
    }
    
}
