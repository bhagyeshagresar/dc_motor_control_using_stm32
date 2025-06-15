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
using ScottPlot;
using ScottPlot.WinForms;
using System.Threading;
using System.IO;

namespace GUI
{
    public partial class Form1 : Form
    {
        private int dutyCycle = 0;
        SerialPort serialPort;
        private int encoderCounts = 0;
        private int adcCounts = 0;
        private int currentAmps = 0;
        private int encoderDegrees = 0;
        string stm32_response = null;
        private CancellationTokenSource _cts = new CancellationTokenSource();
        public Form1()
        {
            InitializeComponent();
            InitializeSerial();
            PlotCurrentTrajectory();
            //serialPort.DataReceived += new SerialDataReceivedEventHandler(DataReceivedHandler);
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
                        currentAmpsTxtBox.Text = currentAmps.ToString();

                    }));
                }

                if (stm32_response.StartsWith("ADC_CNTS:") && int.TryParse(stm32_response.Substring(9), out adcCounts))
                {
                    // Update UI (on main thread)
                    this.Invoke(new Action(() =>
                    {
                        //this should read encoder cnts as zero
                        adcCountsTxtBox.Text = adcCounts.ToString();

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
                            statusTextBox.Text = "Duty Cycle set to:" + dutyCycle.ToString();
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

        private void PlotCurrentTrajectory()
        {
            double frequencyHz = 100;        // 100 Hz square wave
            double amplitude = 200;          // ±200 mA
            double durationMs = 40;          // Show 4 cycles (10 ms per cycle)
            double sampleRate = 10000;       // 0.1 ms resolution

            int pointCount = (int)(durationMs * sampleRate / 1000);
            double[] timeMs = new double[pointCount];
            double[] currentmA = new double[pointCount];

            for (int i = 0; i < pointCount; i++)
            {
                timeMs[i] = i * (1000.0 / sampleRate); // in ms
                double tSec = timeMs[i] / 1000.0;
                currentmA[i] = amplitude * Math.Sign(Math.Sin(2 * Math.PI * frequencyHz * tSec));
            }


            var plt = iTestPlot.Plot;
            plt.Clear();
            plt.Add.Scatter(timeMs, currentmA);
            plt.Title("Reference Current : 100 Hz Square Wave");
            plt.XLabel("Time (ms)");
            plt.YLabel("Current (mA)");

            plt.Axes.SetLimitsX(0, 40); // X axis from 0 ms to 40 ms

            iTestPlot.Refresh();

        }

    }
    
}
